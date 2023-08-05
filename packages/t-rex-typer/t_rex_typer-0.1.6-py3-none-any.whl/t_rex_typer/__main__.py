import sys
import argparse
from t_rex_typer import settings
from t_rex_typer.main_window import MainWindow
from . import APP, IS_DEV_DEBUG


parser = argparse.ArgumentParser()
parser.add_argument("--log-level",
                    help="set log level.  Default is 'info'.  Use 'debug' for more logging.",
                    choices=['info', 'debug'], type=str)
args = parser.parse_args()


if IS_DEV_DEBUG or args.log_level == 'debug':
    log.setLevel(logging.DEBUG)
    logging.getLogger("settings").setLevel(logging.DEBUG)
    log.warning(f'RUNNING IN DEBUG MODE')

    def my_excepthook(etype, value, tb):
        print(f"", flush=True)
        import traceback
        traceback.print_exception(etype, value, tb)
        print(f"Entering post-mortem debugger...\n", flush=True)
        import pdb; pdb.pm()

    sys.excepthook = my_excepthook


main_window = MainWindow()
main_window.show()

sys.exit(APP.exec_())
