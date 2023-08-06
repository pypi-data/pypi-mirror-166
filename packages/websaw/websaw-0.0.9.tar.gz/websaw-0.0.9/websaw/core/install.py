import sys
import os
import click
import uuid
import zipfile

from .globs import current_config, DefaultConfig
from .loggers import error_logger
from .utils import MetaPathRouter


_ASSETS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../assets")
)


def _process_apps_folder(apps_folder, confirmed=False):
    if not os.path.exists(apps_folder):
        if confirmed or click.confirm(f"Create missing folder {apps_folder}?"):
            os.makedirs(apps_folder)
            confirmed = True
        else:
            click.echo("Command aborted")
            sys.exit(0)

    _process_init_missing(apps_folder, confirmed)


def _process_init_missing(apps_folder, confirmed=False):
    init_py = os.path.join(apps_folder, "__init__.py")
    if not os.path.exists(init_py):
        if confirmed or click.confirm(f"Create missing init file {init_py}?"):
            with open(init_py, "wb"):
                pass
        else:
            click.echo("Command aborted")
            sys.exit(0)


def _get_session_secret(service_folder):
    if not os.path.exists(service_folder):
        os.mkdir(service_folder)
    session_secret_filename = os.path.join(
        service_folder, "session.secret"
    )
    if not os.path.exists(session_secret_filename):
        with open(session_secret_filename, "w") as fp:
            fp.write(str(uuid.uuid4()))
    with open(session_secret_filename) as fp:
        session_secret = fp.read()
    return session_secret


def install_args(kwargs, reinstall_apps=False):

    # DefaultConfig is a factory and returns instance of ombott.common_helpers.NameSpace
    config: DefaultConfig = DefaultConfig(kwargs)

    apps_folder = config.apps_folder = os.path.abspath(config.apps_folder)
    config.service_folder = os.path.join(apps_folder, config.service_folder)
    config.password_file = os.path.abspath(config.password_file)

    for key, val in config.items():
        os.environ[f"WEBSAW_{key.upper()}"] = str(val)

    yes_to_all = kwargs.get("yes", False)

    # If the apps folder does not exist create it and populate it
    _process_apps_folder(apps_folder, confirmed=yes_to_all)

    # ensure service stuff
    config.session_secret = _get_session_secret(config.service_folder)

    # ensure that "import apps.someapp" works
    apps_folder_parent, apps_folder_name = os.path.split(apps_folder)
    if apps_folder_parent not in sys.path:
        sys.path.insert(0, apps_folder_parent)
    if apps_folder_name != "apps":
        MetaPathRouter(apps_folder_name)

    error_logger.initialize()
    current_config.__dict__.update(config.__dict__)


def reinstall_apps(apps_folder, confirmed):
    assets_dir = _ASSETS_DIR
    # Reinstall apps from zipped ones in assets
    if os.path.exists(assets_dir):
        apps = os.listdir(assets_dir)
        for filename in apps:
            zip_filename = os.path.join(assets_dir, filename)
            # These filenames do not necessarily exist if one has
            # downloaded from source and deleted them.
            app_name = filename.split(".")[-2]
            target_dir = os.path.join(apps_folder, app_name)
            if not os.path.exists(target_dir):
                if confirmed or click.confirm(f"Create app {app_name}?"):
                    click.echo(f"[ ] Unzipping app {filename}")
                    with zipfile.ZipFile(zip_filename, "r") as zip_file:
                        os.makedirs(target_dir)
                        zip_file.extractall(target_dir)
                        click.echo("\x1b[A[X]")
