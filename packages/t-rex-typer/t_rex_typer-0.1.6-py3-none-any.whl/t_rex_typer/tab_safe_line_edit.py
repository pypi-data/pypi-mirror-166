from PySide2 import QtCore, QtWidgets, QtGui


class TabSafeLineEdit(QtWidgets.QLineEdit):
    """Line edit with tab key control.

    The default QLineEdit will exit the widget when tab is pressed.
    This may be undesirable (e.g. entering steno strokes in a practice
    program changes the input focus).  This widget prevents focus from
    changing.

    """
    # Focus will leave regardless of the focusPolicy.  Tab is not
    # caught by keyPressEvent.  The documentation states,
    #
    #     "There are also some rather obscure events described in the
    #     documentation for Type. To handle these events, you need to
    #     reimplement event() directly."
    #
    # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QWidget.html?highlight=qwidget#events
    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Tab):
            self.insert("\t")
            return True
        else:
            return QtWidgets.QLineEdit.event(self, event)
