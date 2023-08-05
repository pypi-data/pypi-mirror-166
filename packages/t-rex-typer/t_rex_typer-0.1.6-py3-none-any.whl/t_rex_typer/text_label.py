from PySide2 import QtCore, QtWidgets, QtGui


class TextLabel(QtWidgets.QTextEdit):
    """Faux label with object oriented color control.

    This widget is a QTextEdit styled to look like a QLabel.  QLabels
    handle color only through markup which complicates text
    manipulation.  QTextEdits provide cursors which can style text
    using object properties.

    Parameters
    ----------
    text : str

      Text to display.

    parent : QWidget, optional

      Parent widget.  Default is None.

    """

    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

        self.setReadOnly(True)

        if parent:
            color = parent.palette().window().color()
        else:
            # the default light gray
            color = QtWidgets.QWidget().palette().window().color()

        p =  self.viewport().palette()
        p.setColor(QtGui.QPalette.Base, color)
        self.viewport().setPalette(p)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.document().setDocumentMargin(0)

        # NOTE: Implementing as a size hint may make this widget more
        # generally useable.
        font_metrics = QtGui.QFontMetrics(self.font())
        self.setFixedHeight(font_metrics.height())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = QtWidgets.QWidget()
    widget.resize(300, 300)
    pal    = widget.palette()
    pal.setColor(QtGui.QPalette.Window, QtCore.Qt.red)
    widget.setPalette(pal)

    widget = None
    label = TextLabel(text="this is a really long line that should be cut off.", parent=widget)
    label_color = label.viewport().palette().window().color()

    # widget.show()
    label.show()

    app.exec_()
