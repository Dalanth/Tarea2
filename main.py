#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PySide import QtGui, QtCore
import controller
from mainwindow import Ui_MainWindow
import view_form


class Main(QtGui.QWidget): #Main UI screen

    def __init__(self):
    #Sets up the UI
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_products_by_search()
        self.load_brands()
        self.load_products()
        self.show()
        self.set_listeners()


    def delete(self):
    #Calls on controller to delete a product row on the database
        model = self.ui.table.model()
        index = self.ui.table.currentIndex()
        if index.row() == -1: #No row selected
            self.ui.errorMessageDialog = QtGui.QMessageBox.information(self, 'Error',
                                            u"Debe seleccionar la fila que desea eliminar",
                                            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False
        else:
            self.ui.confirmMessage = QtGui.QMessageBox.question(self, 'Borrar producto',
                                    u"Está seguro que desea eliminar el producto seleccionado?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if self.ui.confirmMessage == QtGui.QMessageBox.Yes:#Prompts the user for confirmation
                product = model.index(index.row(), 0, QtCore.QModelIndex()).data()
                if (controller.delete(product)):
                    self.load_products()
                    self.ui.msgBox = QtGui.QMessageBox.information(self, u'Atención',
                                    u"El registro fue eliminado con éxito")
                    return True
                else:
                    self.ui.errorMessageDialog = QtGui.QMessageBox.information(self, 'Error',
                                            u"Error al eliminar el registro",
                                            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                    return False


    def load_brands(self):
    #Loads Brands from the database for the combobox
        brands = controller.get_brands()
        self.ui.selectBrand.addItem("Todos", -1)
        for brand in brands: #Add Brands to the ComboBox
            self.ui.selectBrand.addItem(brand["name"], brand["id_brand"])
        self.ui.selectBrand.setEditable(False)


    def load_products(self, products=None):
    #Loads Products from database for display
        if products is None:
            products = controller.get_products()
        self.model = QtGui.QStandardItemModel(len(products), 4)
        
        self.model.setHorizontalHeaderItem(0, QtGui.QStandardItem(u"Producto"))
        self.model.setHorizontalHeaderItem(1, QtGui.QStandardItem(u"Descripción"))
        self.model.setHorizontalHeaderItem(2, QtGui.QStandardItem(u"Color"))
        self.model.setHorizontalHeaderItem(3, QtGui.QStandardItem(u"Precio"))
        self.model.setHorizontalHeaderItem(4, QtGui.QStandardItem(u"Marca"))

        r = 0
        for row in products:
            index = self.model.index(r, 0, QtCore.QModelIndex())
            self.model.setData(index, row['prod'])
            index = self.model.index(r, 1, QtCore.QModelIndex())
            self.model.setData(index, row['description'])
            index = self.model.index(r, 2, QtCore.QModelIndex())
            self.model.setData(index, row['color'])
            index = self.model.index(r, 3, QtCore.QModelIndex())
            self.model.setData(index, row['price'])
            index = self.model.index(r, 4, QtCore.QModelIndex())
            self.model.setData(index, row['brands'])
            r = r+1

        self.ui.table.setModel(self.model)
        self.ui.table.setColumnWidth(0, 120)
        self.ui.table.setColumnWidth(1, 300)
        self.ui.table.setColumnWidth(2, 145)
        self.ui.table.setColumnWidth(3, 110)
        self.ui.table.setColumnWidth(4, 110)


    def load_products_by_brand(self):
    #Sets up the search by brand with a ComboBox
        id_brand = self.ui.selectBrand.itemData(self.ui.selectBrand.currentIndex())
        if id_brand == -1: #if option selected is "todos" loads all products
            products = controller.get_products()
        else: #loads products by brands
            products = controller.get_products_by_brand(id_brand)
        self.load_products(products)


    def load_products_by_search(self):
    #Sets up the Search Bar for a word search
        word = self.ui.search_box.text()
        productlist = controller.get_products_name()
        products = controller.search_product(word)
        self.load_products(products)
        completer = QtGui.QCompleter(productlist , self)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.ui.search_box.setCompleter(completer)


    def set_listeners(self):
    #Sets up button listeners
        self.ui.selectBrand.activated[int].connect(self.load_products_by_brand)
        self.ui.search_box.textChanged.connect(self.load_products_by_search) 
        self.ui.btn_delete.clicked.connect(self.delete)
        self.ui.btn_new.clicked.connect(self.show_add_form)
        self.ui.btn_edit.clicked.connect(self.show_edit_form)


    def show_add_form(self):
    #Displays the add products screen
        form = view_form.Form(self)
        form.rejected.connect(self.load_products)
        form.exec_()


    def show_edit_form(self):
    #Displays the edit products screen
        model = self.ui.table.model()
        index = self.ui.table.currentIndex()
        if index.row() == -1: ##No row selected
            self.ui.msgBox = QtGui.QMessageBox.information(self, u'Error',
                                    u"Debe seleccionar la fila que desea editar")
            return False
        else:
            product = model.index(index.row(), 0, QtCore.QModelIndex()).data()
            form = view_form.Form(self, product)
            form.rejected.connect(self.load_products)
            form.exec_()


def run():
#Starts UI loop
    app = QtGui.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()



