import sys
from PySide import *
from form import Ui_Form

class Form(QtGui.QWidget):
	def __init__(self):
		super(Form, self).__init__()
		self.ui =  Ui_Form()
		self.ui.setupUi(self)
		self.show()

def run():
    app = QtGui.QApplication(sys.argv)
    main = Form()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
