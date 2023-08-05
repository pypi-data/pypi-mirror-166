import os
import sys
import logging
import pkgutil
import nostalgic
from PySide2 import QtCore, QtWidgets, QtGui

log = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)

BLACK = QtGui.QColor(0, 0, 0)
GRAY  = QtGui.QColor(190, 190, 190)

IS_DEV_DEBUG = True if os.getenv('DEV_DEBUG') in ['1', 'true', 'True'] else False

APP = QtWidgets.QApplication([])
APPLICATION_NAME       = "T-Rex Typer"
APPLICATION_ICON_BYTES = pkgutil.get_data(__name__, "resources/trex_w_board_48.png")
APPLICATION_PIXMAP     = QtGui.QPixmap()
APPLICATION_PIXMAP.loadFromData(APPLICATION_ICON_BYTES)
APPLICATION_ICON       = QtGui.QIcon(APPLICATION_PIXMAP)
APP.setWindowIcon(APPLICATION_ICON)

SETTING_FILE_NAME = f".config/{APPLICATION_NAME}"

if sys.platform == "linux":
    SETTINGS_PATH = os.path.join(os.path.expanduser("~"),  SETTING_FILE_NAME)

SETTINGS = nostalgic.Configuration(os.path.join(SETTINGS_PATH, f"{APPLICATION_NAME}.ini"))
