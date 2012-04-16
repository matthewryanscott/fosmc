import sys

from PySide import QtGui


def main():
	app = QtGui.QApplication(sys.argv)
	window = QtGui.QWidget()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
