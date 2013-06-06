#!/usr/bin/python
# ­*­ coding: utf­8 ­*­

from PySide import QtGui, QtCore

import controller
from form import Ui_Form

class Form(QtGui.QDialog):

    def __init__(self, parent=None, name=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui =  Ui_Form()
        self.ui.setupUi(self)
        brands = controller.get_brands()
        for brand in brands:
            self.ui.brand.addItem(brand["name"], brand["id_brand"])
        if name is None:
            self.ui.btn_add.clicked.connect(self.add)
        else:
            self.setWindowTitle(u"Editar producto")
            self.name = name
            product_data = controller.get_product(name)
            self.ui.name.setText(product_data["prod"])
            self.ui.desc.setText(product_data["description"])
            self.ui.color.setText(product_data["color"])
            self.ui.price.setValue(product_data["price"])
            self.ui.brand.currentText()
            self.ui.btn_add.clicked.connect(self.edit)
        self.ui.btn_cancel.clicked.connect(self.cancel)


    def add(self):
        #Take the values from the ui form and add the new product
        name = self.ui.name.text()
        description = self.ui.desc.text()
        color = self.ui.color.text()
        price = self.ui.price.value()
        brand = self.ui.brand.currentText()
        id_brand = controller.get_id_brand(brand)
        result = controller.add_product(name, description, color, price, id_brand)
        if result:
            self.reject()
        else:
            self.ui.message.setText("Hubo un problema al intentar agregar el producto")


    def edit(self):
        #Take the values form a product, then save the edited values
        id_product = controller.get_id_product(self.name)
        name = self.ui.name.text()
        description = self.ui.desc.text()
        color = self.ui.color.text()
        price = self.ui.price.value()
        brand = self.ui.brand.currentText()
        id_brand = controller.get_id_brand(brand)
        result = controller.edit_product(id_product, name, description, color, price, id_brand)
        if result:
            self.reject()
        else:
            self.ui.message.setText("Hubo un problema al intentar editar el producto")


    def cancel(self):
        #Cancel the operation on the ui form
        self.reject()
