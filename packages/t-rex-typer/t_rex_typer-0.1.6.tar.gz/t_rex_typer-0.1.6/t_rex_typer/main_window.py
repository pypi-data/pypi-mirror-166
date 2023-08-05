import os
import sys
import json
import time
import base64
import tempfile

import logging
log = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)

from PySide2 import QtCore, QtWidgets, QtGui

from tests.dialog_action import DialogAction

from t_rex_typer import settings
from t_rex_typer.translation_dict import TranslationDict
from t_rex_typer.tab_safe_line_edit import TabSafeLineEdit
from t_rex_typer.text_label import TextLabel

from t_rex_typer import IS_DEV_DEBUG, APPLICATION_NAME, APPLICATION_PIXMAP, SETTINGS, BLACK, GRAY


IN_TESTING = False


class RunState:
    COMPLETE   = 'complete'
    PRACTICING = 'practicing'
    READY      = 'ready'


class SettingsWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumWidth(600)

        self._modified = False
        self.setWindowTitle(f'Settings')
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.init_widgets()
        self.init_layout()

    def init_widgets(self):

        # wpm threshold
        self.wpm_threshold_label = QtWidgets.QLabel("WPM Miss Threshold:")
        self.wpm_threshold_label.setToolTip("Count multi-strokes slower than this as a miss")
        self.wpm_threshold_spinbox = QtWidgets.QSpinBox()
        self.wpm_threshold_spinbox.setToolTip("Words per minute")
        self.wpm_threshold_spinbox.setRange(0, 400)
        self.wpm_threshold_spinbox.valueChanged.connect(self.on_change)

        # dictionary directory
        self.dictionary_directory_label = QtWidgets.QLabel("Dictionary Directory:")
        self.dictionary_directory_label.setToolTip("Plover dictionary directory")
        self.dictionary_directory_line_edit = QtWidgets.QLineEdit()
        self.dictionary_directory_line_edit.textChanged.connect(self.on_change)

        # lesson directory
        self.lesson_directory_label = QtWidgets.QLabel("Lesson Directory:")
        self.lesson_directory_label.setToolTip("Lesson directory")
        self.lesson_directory_line_edit = QtWidgets.QLineEdit()
        self.lesson_directory_line_edit.textChanged.connect(self.on_change)

        # restore defaults
        self.restore_defaults_link = QtWidgets.QLabel('<a href=".">Restore defaults</a>')
        self.restore_defaults_link.setToolTip("Restore default settings")
        self.restore_defaults_link.linkActivated.connect(self.on_restore_defaults_link_activated)

        # button box
        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel |
            QtWidgets.QDialogButtonBox.Apply)

        self.ok_button = self.button_box.buttons()[0]
        self.ok_button.setToolTip("Save changes and close window")
        self.ok_button.setEnabled(False)
        self.button_box.accepted.connect(self.on_ok_clicked)

        self.cancel_button = self.button_box.buttons()[1]
        self.cancel_button.setToolTip("Close window without applying changes")
        self.button_box.rejected.connect(self.close)

        self.apply_button = self.button_box.buttons()[2]
        self.apply_button.setToolTip("Save changes")
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.apply_settings)

    def init_layout(self):
        self.form_layout = QtWidgets.QFormLayout()

        # form
        self.form_layout.addRow(
            self.wpm_threshold_label,
            self.wpm_threshold_spinbox)
        self.form_layout.addRow(
            self.lesson_directory_label,
            self.lesson_directory_line_edit)
        self.form_layout.addRow(
            self.dictionary_directory_label,
            self.dictionary_directory_line_edit)

        # restore defaults
        self.restore_defaults_layout = QtWidgets.QHBoxLayout()
        self.restore_defaults_layout.addWidget(QtWidgets.QWidget(), stretch=1)
        self.restore_defaults_layout.addWidget(self.restore_defaults_link)

        # button box
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(QtWidgets.QWidget(), stretch=1)
        self.button_layout.addWidget(self.button_box)

        # layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(QtWidgets.QWidget(), stretch=1)
        self.layout.addLayout(self.restore_defaults_layout)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def _set_modified(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"'modified' must be bool type: '{value}'")

        self._modified = value
        if self._modified:
            self.apply_button.setEnabled(True)
            self.ok_button.setEnabled(True)
            self.setWindowTitle(f"Settings*")
        else:
            self.apply_button.setEnabled(False)
            self.ok_button.setEnabled(False)
            self.setWindowTitle(f"Settings")

    def _get_modified(self):
        return self._modified

    modified = property(_get_modified, _set_modified)

    def on_change(self, *args):
        self.modified = True

    def restore_defaults(self):
        non_application_keys = [k for k in SETTINGS._settings.keys() if k[:12] != 'main_window_']
        SETTINGS.set(keys=non_application_keys, use_defaults=True)

    def apply_settings(self):
        SETTINGS.write()
        self.modified = False
        log.info(f"Saved settings: {SETTINGS.config_file}")

    def on_restore_defaults_link_activated(self):
        self.restore_defaults()

    def on_ok_clicked(self):
        self.apply_settings()
        self.close()


class AboutWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f'About {APPLICATION_NAME}')
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.init_widgets()
        self.init_layout()

    def init_widgets(self):
        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setPixmap(APPLICATION_PIXMAP)

        self.body_title = QtWidgets.QLabel(f'<h1>About</h1>')

        body_text = (
            f'<p>The {APPLICATION_NAME} is made by Matt Trzcinski.</p>'
            f'<hr>'
            f'<p>'
            f'<a href="https://icons8.com/icon/5vV_csnCe5Q2/kawaii-dinosaur">kawaii-dinosaur</a> and '
            f'<a href="https://icons8.com/icon/87796/keyboard">keyboard</a> by <a href="https://icons8.com">Icons8</a>.'
            f'</p>'
        )

        self.body = QtWidgets.QLabel(body_text)
        self.body.setOpenExternalLinks(True)
        self.body.setTextInteractionFlags(
            self.body.textInteractionFlags() | QtCore.Qt.TextSelectableByMouse)
        self.body.linkHovered.connect(self.on_link_hovered)

    def init_layout(self): # pragma: no cover
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.addWidget(self.icon_label)
        self.title_layout.addWidget(self.body_title)
        self.title_layout.addWidget(QtWidgets.QWidget(), stretch=1)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.title_layout)
        self.layout.addWidget(self.body, stretch=1)
        self.setLayout(self.layout)

    def on_link_hovered(self, link):
        if link:
            pos = QtGui.QCursor.pos() if not IN_TESTING else QtCore.QPoint(42, 42)
            QtWidgets.QToolTip.showText(pos, link)
        else:
            QtWidgets.QToolTip.hideText()

    def closeEvent(self, event):
        self.hide()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APPLICATION_NAME)
        self.setWindowFlags(
            QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowMinMaxButtonsHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        self._dictionary = {}
        self._lesson_file = None
        self._run_state = RunState.READY

        self.text_raw     = ''
        self.split_raw    = ()
        self.split_live   = []
        self.current_unit = ''

        self.missed         = 0
        self._last_time     = 0
        self._is_maybe_miss = False
        self._is_miss       = False

        self.init_widgets()
        self.init_layout()

        settings.init(self, self.settings_window)
        settings.load(sync=True)

        # Debug
        if IS_DEV_DEBUG:  # pragma: no cover
            # self.line_edit.setFocus()
            # SETTINGS.dictionary_directory = "/home/ahab/Projects/t_rex_typer/scratch/"
            # SETTINGS.lesson_directory     = "/home/ahab/Projects/t_rex_typer/scratch/"
            # self.on_settings_action_triggered()
            pass
        else:
            self.text_edit.setFocus()

    ##############
    # Properties #
    ##############

    def _get_lesson_file(self):
        return self._lesson_file

    def _set_lesson_file(self, value):
        self._lesson_file = value
        log.info(f"Set lesson file to: {self._lesson_file}")
        if self._lesson_file:
            self.save_action.setEnabled(True)
            log.debug(f"Enabled save_action")
        else:
            self.save_action.setEnabled(False)
            log.debug(f"Disabled save_action")

    lesson_file = property(_get_lesson_file, _set_lesson_file)

    def _set_run_state(self, value):
        self._run_state = value
        log.debug(f"{self._run_state=}")

    def _get_run_state(self):
        return self._run_state

    run_state = property(_get_run_state, _set_run_state)

    def init_widgets(self):

        ########
        # menu #
        ########

        self.open_action = QtWidgets.QAction('&Open', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('Open..')
        self.open_action.triggered.connect(self.on_open_action_triggered)

        self.save_action = QtWidgets.QAction('&Save', self)
        self.save_action.setEnabled(False)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('Save')
        self.save_action.triggered.connect(self.on_save_action_triggered)

        self.save_as_action = QtWidgets.QAction('Save &As..', self)
        self.save_as_action.setToolTip('Save As')
        self.save_as_action.setEnabled(False)
        self.save_as_action.triggered.connect(self.on_save_as_action_triggered)

        self.load_dictionary_action = QtWidgets.QAction('Load Dictionary...', self)
        self.load_dictionary_action.setToolTip('Load and replace the current dictionary')
        self.load_dictionary_action.triggered.connect(self.on_load_dictionary_triggered)

        self.settings_action = QtWidgets.QAction('&Settings...', self)
        self.settings_action.setToolTip("Open Settings Window")
        self.settings_action.triggered.connect(self.on_settings_action_triggered)

        self.exit_action = QtWidgets.QAction('&Exit', self)

        if IS_DEV_DEBUG:  # pragma: no cover
            self.exit_action.setShortcut("Escape")

        self.exit_action.setToolTip('Exit application')
        self.exit_action.triggered.connect(self.close)

        self.about_action = QtWidgets.QAction('&About', self)
        self.about_action.triggered.connect(self.on_about_action_triggered)

        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.setToolTipsVisible(True)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.load_dictionary_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.help_menu = self.menu_bar.addMenu('&Help')
        self.help_menu.setToolTipsVisible(True)
        self.help_menu.addAction(self.about_action)

        ############
        # Non-menu #
        ############

        # no parent so that a separate window is used
        self.about_window = AboutWindow()
        self.settings_window = SettingsWindow()

        # Text label
        self.text_label = TextLabel()

        # Line edit
        self.line_edit = TabSafeLineEdit()
        self.line_edit.setEnabled(False)

        # setText doesn't trigger edited signal (only changed signal)
        self.line_edit.textEdited.connect(self.on_line_edit_text_edited)

#         # Steno label
#         self.steno_label = QtWidgets.QLabel('')

        # Text edit
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlaceholderText('Put practice words here...')
        self.text_edit.textChanged.connect(self.on_text_edit_changed)

        # start
        self.restart_button = QtWidgets.QPushButton("Restart")
        self.restart_button.pressed.connect(self.on_restart_button_pressed)

#         if IS_DEV_DEBUG:
#             text = ("It's the case that every effort has been made to 'replicate' this text as"
#                     "faithfully as possible, including inconsistencies in spelling"
#                     "and hyphenation.  Some corrections of spelling and punctuation"
#                     "have been made. They are listed at the end of the text.")

#             text = "this is a test"

#             self.text_edit.setText(text)

    def init_layout(self):

        self.setGeometry(300, 300, 800, 400)

        # Frame top left
        self.ftl_layout = QtWidgets.QVBoxLayout()
        self.ftl_layout.setContentsMargins(2, 2, 2, 2)
        self.ftl_layout.addWidget(QtWidgets.QWidget(), stretch=1)
        self.ftl_layout.addWidget(self.text_label)

        self.frame_top_left = QtWidgets.QFrame()
        self.frame_top_left.setLayout(self.ftl_layout)

        # Frame middle left
        self.fml_layout = QtWidgets.QVBoxLayout()
        self.fml_layout.setContentsMargins(2, 2, 2, 2)
        self.fml_layout.addWidget(self.line_edit)
        # self.fml_layout.addWidget(self.steno_label)
        self.fml_layout.addWidget(QtWidgets.QWidget(), stretch=1)

        self.frame_middle_left = QtWidgets.QFrame()
        self.frame_middle_left.setLayout(self.fml_layout)

        # Frame bottom left
        self.fbl_layout = QtWidgets.QVBoxLayout()
        self.fbl_layout.setContentsMargins(2, 2, 2, 2)
        self.fbl_layout.addWidget(self.text_edit)

        self.frame_bottom_left = QtWidgets.QFrame()
        self.frame_bottom_left.setLayout(self.fbl_layout)

        # Frame left
        self.fl_layout = QtWidgets.QVBoxLayout()
        self.fl_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_left = QtWidgets.QFrame()
        self.frame_left.setLayout(self.fl_layout)
        self.frame_left.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)

        # Frame right
        self.fr_layout = QtWidgets.QVBoxLayout()
        self.fr_layout.setContentsMargins(0, 0, 0, 0)
        self.fr_layout.addWidget(self.restart_button)

        self.frame_right = QtWidgets.QFrame()
        self.frame_right.setLayout(self.fr_layout)
        self.frame_right.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)

        # Place frames in splitters
        self.splitter_h = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter_v = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter_h.addWidget(self.frame_top_left)
        self.splitter_h.addWidget(self.frame_middle_left)
        self.splitter_h.addWidget(self.frame_bottom_left)
        self.fl_layout.addWidget(self.splitter_h)

        self.splitter_v.addWidget(self.frame_left)
        self.splitter_v.addWidget(self.frame_right)

        # Central widget
        self.central_layout = QtWidgets.QHBoxLayout()
        self.central_layout.setContentsMargins(5, 5, 5, 5)
        self.central_layout.addWidget(self.splitter_v)
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    ############
    # Settings #
    ############
    def _set_geometry(self, value):
        # settings are written to disk as text, geometry is a byte array
        geometry_bytes = base64.b64decode(value)
        self.restoreGeometry(geometry_bytes)

    def _get_geometry(self):
        # settings are written to disk as text, geometry is a byte array
        geometry_ascii = base64.b64encode(bytes(self.saveGeometry())).decode('ascii')
        json_encoded = json.dumps(geometry_ascii)
        return json_encoded

    def _set_size(self, value):
        if value:
            self.resize(*value)

    def _get_size(self):
        # Must return a serializable value
        return self.size().toTuple()

    def _set_pos(self, value):
        if value:
            self.move(*value)

    def _get_pos(self):
        # Must return a serializable value
        return self.pos().toTuple()

    def _set_maximized(self, value):
        if value:
            self.showMaximized()

    def _get_maximized(self):
        return self.isMaximized()

    def _set_splitter_h_state(self, value):
        state_bytes = base64.b64decode(value)
        self.splitter_h.restoreState(state_bytes)

    def _get_splitter_h_state(self):
        # settings are written to disk as text, state is a byte array
        state_ascii = base64.b64encode(bytes(self.splitter_h.saveState())).decode('ascii')
        json_encoded = json.dumps(state_ascii)
        return json_encoded

    def _set_splitter_v_state(self, value):
        # settings are written to disk as text, state is a byte array
        state_bytes = base64.b64decode(value)
        self.splitter_v.restoreState(state_bytes)

    def _get_splitter_v_state(self):
        # settings are written to disk as text, state must be a byte array
        state_ascii = base64.b64encode(bytes(self.splitter_v.saveState())).decode('ascii')
        json_encoded = json.dumps(state_ascii)
        return json_encoded

    ###################
    # General methods #
    ###################
    def set_window_title(self, string=''):
        if string:
            self.setWindowTitle(f'{APPLICATION_NAME} - ' + str(string))
        else:
            self.setWindowTitle(f'{APPLICATION_NAME}')

    def on_open_action_triggered(self):
        if IN_TESTING == DialogAction.Selected:
            filename = f"{tempfile.gettempdir()}/test_on_open.txt"
        elif IN_TESTING == DialogAction.Canceled:
            filename = ''
        else:  # pragma: no cover
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                caption='Open Lesson File',
                dir=SETTINGS.lesson_directory,
                filter='Text Files (*.txt);;All (*.*)')

        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()

                self.text_edit.setPlainText(content)
                self.lesson_file = filename
                SETTINGS.lesson_directory = os.path.dirname(filename)
                self.set_window_title(self.lesson_file)
            except Exception as err:
                self.message_box = QtWidgets.QMessageBox()
                self.message_box.setWindowTitle(f"{APPLICATION_NAME[:-4]}error")
                self.message_box.setIcon(QtWidgets.QMessageBox.Warning)
                informative_text = "Address the error below and try again."
                detailed_text = str(err)
                log.info(f"Could not open file: {filename}")
                log.error(detailed_text)
                self.message_box.setText(f"Could not open file:\n\n{filename}")
                self.message_box.setInformativeText(informative_text)
                self.message_box.setDetailedText(detailed_text)
                if not IN_TESTING:
                    self.message_box.show()  # pragma: no cover

    def _save_file(self, filename):
        text = self.text_edit.toPlainText()
        try:
            with open(filename, 'w') as f:
                f.write(text)
        except Exception as err:
            self.message_box = QtWidgets.QMessageBox()
            self.message_box.setWindowTitle(f"{APPLICATION_NAME[:-4]}error")
            self.message_box.setIcon(QtWidgets.QMessageBox.Warning)
            text = "Could not save file."
            log.info(text)
            informative_text = "Address the error below and try again."
            detailed_text = str(err)
            log.error(detailed_text)
            self.message_box.setText(text)
            self.message_box.setInformativeText(informative_text)
            self.message_box.setDetailedText(detailed_text)
            if not IN_TESTING:
                self.message_box.show()  # pragma: no cover

        log.info(f"Saved: {filename}")
        self.set_window_title(filename)
        self.text_edit.document().setModified(False)

    def on_save_action_triggered(self):
        self._save_file(self.lesson_file)

    def on_save_as_action_triggered(self):
        if IN_TESTING == DialogAction.Selected:
            filename =  f"{tempfile.gettempdir()}/test_on_save_as.txt"
        elif IN_TESTING == DialogAction.Canceled:
            filename = ''
        else:  # pragma: no cover
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                caption="Save As..",
                dir=SETTINGS.lesson_directory,
                filter="Text files (*.txt);;All files (*.*)")

        if filename:
            self._save_file(filename)
            self.lesson_file = filename

    def on_load_dictionary_triggered(self):
        if IN_TESTING == DialogAction.Selected:
            filenames =  [f"{tempfile.gettempdir()}/test_on_load_dictionary_triggereded.json", ]
        elif IN_TESTING == DialogAction.Canceled:
            filenames = []
        else:  # pragma: no cover
            filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                caption='Open one or more Plover dictionary files',
                dir=SETTINGS.dictionary_directory,
                filter='JSON Files (*.json);;All (*.*)')

        if filenames:
            self._dictionary = TranslationDict.load(filenames)
            log.debug(f"Loaded dictionaries: {filenames}")

    def on_settings_action_triggered(self):
        non_application_keys = [k for k in SETTINGS._settings.keys() if k[:12] != 'main_window_']
        SETTINGS.set(non_application_keys)
        self.settings_window.modified = False

        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def on_about_action_triggered(self):
        self.about_window.show()
        self.about_window.raise_()
        self.about_window.activateWindow()

    def _reset(self):
        self.text_label.clear()
        self.line_edit.clear()
        self.missed = 0
        self._last_time = 0

        if self.split_raw:
            self.split_live   = list(self.split_raw)
            self.current_unit = self.split_raw[0]

            cursor = self.text_label.textCursor()
            cursor.setPosition(0)
            text_format = cursor.charFormat()
            text_format.setForeground(QtGui.QBrush(BLACK))
            text_format.setFontUnderline(True)
            cursor.insertText(self.current_unit, text_format)
            text_format.setFontUnderline(False)
            cursor.insertText(' '+' '.join(self.split_raw[1:]), text_format)
            cursor.setPosition(0)
            self.text_label.setTextCursor(cursor)

            self.line_edit.setEnabled(True)

        self.run_state = RunState.READY

    def on_text_edit_changed(self):
        title = ''
        if self.lesson_file:
            title += self.lesson_file

        if self.text_edit.document().isModified():
            title += '*'

        self.set_window_title(title)

        self.save_as_action.setEnabled(True)

        self.text_raw   = self.text_edit.toPlainText()
        self.split_raw = tuple(TranslationDict.split_into_strokable_units(self.text_raw))

        self._reset()

    def on_restart_button_pressed(self):
        self._reset()

    def on_line_edit_text_edited(self, content):
        # get time between strokes asap
        delta = abs(time.time()-self._last_time)

        if self.run_state == RunState.COMPLETE:
            return
        elif self.run_state != RunState.PRACTICING:
            self.run_state = RunState.PRACTICING

        # Accuracy measured on a per unit basis.  Without stroke information,
        # it's impossible to know whether text is a misstroke or simply part
        # of a multi-stroke phrase—Plover may delete entire words as part of a
        # multi-stroke sequence (e.g. "LEBG/TOR"->"lecture"->"elector").
        # Assuming the average word length in English is 5 characters, time in
        # seconds between characters /dt/ expressed in words given per minute
        # /w/ is dt = 12/w.  So, 0.4s is 30wpm.  SETTINGS.time_between_strokes
        # represents the minimum acceptable speed.
        time_between_strokes = 0.001 if IN_TESTING else 12 / SETTINGS.wpm_threshold
        if not self._is_miss and self._is_maybe_miss and delta > time_between_strokes:
            # since self._is_maybe_miss only gets set once per unit, each
            # unit has a maximum of 1 possible miss
            self.missed += 1
            self._is_miss = True

        # in steno, there are different ways to write something like a
        # double quote.  One stroke puts a space first to manage
        # sentence spacing.  Another puts a space after.  A leading
        # space would mess with the trimmed_content comparison if we
        # didn't trim.
        trimmed_content = content.strip()

        # position is "between" characters; index is "on" characters
        line_edit_cursor_position = self.line_edit.cursorPosition()
        line_edit_cursor_index = self.line_edit.cursorPosition() - 1

        cursor = QtGui.QTextCursor(self.text_label.document())
        text_format = cursor.charFormat()

        if trimmed_content:

            # match; advance or finish
            if trimmed_content == self.current_unit:
                self.split_live.pop(0)
                self.line_edit.clear()
                self.text_label.clear()

                self._is_maybe_miss = False
                self._is_miss       = False

                # advance to next unit
                if self.split_live:
                    self.current_unit = self.split_live[0]

                    text_format.setForeground(QtGui.QBrush(BLACK))
                    text_format.setFontUnderline(True)
                    cursor.setCharFormat(text_format)
                    cursor.insertText(self.current_unit)
                    text_format.setFontUnderline(False)
                    cursor.setCharFormat(text_format)
                    cursor.insertText(' '+' '.join(self.split_live[1:]))

                # finish
                else:
                    self.run_state = RunState.COMPLETE
                    total_number_units = len(self.split_raw)
                    if total_number_units > 0:
                        correct = (total_number_units - self.missed)
                        accuracy = correct / total_number_units
                        cursor.insertText(f"CONGRATS! Missed: {self.missed} Accuracy: {accuracy*100:.0f}%")
                    self.line_edit.setEnabled(False)

            # contents don't match current unit
            else:
                if len(trimmed_content) > len(self.current_unit):
                    self._is_maybe_miss = True

                cursor.setPosition(1)

                for i, c in enumerate(self.current_unit):
                    color = BLACK

                    if i < len(trimmed_content):
                        if trimmed_content[i] == c:
                            color = GRAY
                            pass
                        else:
                            # contents have non-matching char
                            self._is_maybe_miss = True

                    cursor.deletePreviousChar()
                    text_format.setForeground(QtGui.QBrush(color))
                    cursor.insertText(c, text_format)
                    cursor.setPosition(cursor.position()+1)

        # no content–user deleted all input.
        else:
            # already started and then returned to position 0
            self._is_maybe_miss = True

            # recolor first char
            cursor.setPosition(1)
            cursor.deletePreviousChar()
            text_format.setForeground(QtGui.QBrush(BLACK))
            cursor.insertText(self.current_unit[0], text_format)

        # doesn't penalize user for our processing time; do last
        self._last_time = time.time()

    def closeEvent(self, event):
        # must save before objects (like the SettingsWindow) are
        # destroyed
        settings.save(sync=True)

        # since MainWindow is not parent, must close manually
        self.about_window.close()
        del self.about_window

        self.settings_window.close()
        del self.settings_window

        event.accept()
