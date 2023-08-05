import os
import logging
from t_rex_typer import SETTINGS


log = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)


def load(sync=True):
    SETTINGS.read(sync=sync)
    log.info(f"Loaded settings: {SETTINGS.config_file}")


def save(sync=True):
    SETTINGS.write(sync=sync)
    log.info(f"Saved settings: {SETTINGS.config_file}")


def init(main_window, settings_window):

    SETTINGS.add_setting(
        "main_window_geometry",
        default=main_window.saveGeometry(),
        setter =main_window._set_geometry,
        getter =main_window._get_geometry)

    SETTINGS.add_setting(
        "main_window_size",
        default=[640, 480],
        setter =main_window._set_size,
        getter =main_window._get_size)

    SETTINGS.add_setting(
        "main_window_pos",
        default=main_window.pos(),
        setter =main_window._set_pos,
        getter =main_window._get_pos)

    SETTINGS.add_setting(
        "main_window_maximized",
        default=False,
        setter =main_window._set_maximized,
        getter =main_window._get_maximized)

    SETTINGS.add_setting(
        "main_window_splitter_h_state",
        default=main_window.splitter_h.saveState(),
        setter=main_window._set_splitter_h_state,
        getter=main_window._get_splitter_h_state)

    SETTINGS.add_setting(
        "main_window_splitter_v_state",
        default=main_window.splitter_v.saveState(),
        setter=main_window._set_splitter_v_state,
        getter=main_window._get_splitter_v_state)

    SETTINGS.add_setting(
        "wpm_threshold",
        default=30,
        setter=settings_window.wpm_threshold_spinbox.setValue,
        getter=settings_window.wpm_threshold_spinbox.value)

    SETTINGS.add_setting(
        "lesson_directory",
        default=os.path.expanduser("~"),
        setter=settings_window.lesson_directory_line_edit.setText,
        getter=settings_window.lesson_directory_line_edit.text)

    SETTINGS.add_setting(
        "dictionary_directory",
        default=os.path.expanduser("~"),
        setter=settings_window.dictionary_directory_line_edit.setText,
        getter=settings_window.dictionary_directory_line_edit.text)
