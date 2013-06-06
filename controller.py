# -*- coding: utf-8 -*-
import sqlite3


def add_product(prod, description, color, price, brand):
    #Add a new product to the table 'product' on the database
    success = False
    con = connect()
    c = con.cursor()
    values = [prod, description, color, price, brand]
    query = "INSERT INTO product (prod, description, color, price, fk_id_brand) VALUES(?,?,?,?,?)"
    try:
        result = c.execute(query, values)
        success = True
        con.commit()
    except sqlite3.Error as e:
        success = False
        print "Error: ", e.args[0]
    con.close()
    return success


def connect():
    #Connect with the database
    con = sqlite3.connect("data.db")
    con.row_factory = sqlite3.Row
    return con


def delete(prod):
    #Delete a product by selecting a row on the QTableView
    exito = False
    con = connect()
    c = con.cursor()
    query = "DELETE FROM product WHERE prod = ?"
    try:
        result = c.execute(query, [prod])
        con.commit()
        exito = True
    except sqlite3.Error as e:
        exito = False
        print "Error:", e.args[0]
    con.close()
    return exito


def edit_product(id_product, prod, description, color, price, brand):
    #Edit a product by selecting a row on the QTableView
    success = False
    con = connect()
    c = con.cursor()
    values = [prod, description, color, price, brand, id_product]
    query = """UPDATE product SET prod = ?, description = ?,
            color = ?, price = ?, fk_id_brand = ? WHERE id_product = ?"""
    try:
        result = c.execute(query, values)
        success = True
        con.commit()
    except sqlite3.Error as e:
        success = False
        print "Error: ", e.args[0]
    con.close()
    return success


def get_brands():
    #Get all brands names on the database
    con = connect()
    c = con.cursor()
    query = """SELECT id_brand, name FROM brand"""
    result = c.execute(query)
    brands = result.fetchall()
    con.close()
    return brands


def get_id_brand(brand):
    #Get the id of the brand on the database table 'brand'
    con = connect()
    c = con.cursor()
    query = """SELECT id_brand FROM brand WHERE name = ?"""
    c.execute(query, [brand])
    id_brand = c.fetchone()
    result = id_brand[0]
    con.close()
    return result


def get_id_product(prod):
    #Get the id of the product of the table 'product on the database'
    con = connect()
    c = con.cursor()
    query = """SELECT id_product FROM product WHERE prod = ?"""
    c.execute(query, [prod])
    id_product = c.fetchone()
    result = id_product[0]
    con.close()
    return result


def get_product(prod):
    #Get a product in the table 'product'
    con = connect()
    c = con.cursor()
    query = "SELECT * FROM product WHERE prod = ?"
    result = c.execute(query, [prod])
    product = result.fetchone()
    con.close()
    return product


def get_products():
    #Get all products in the table 'product'
    con = connect()
    c = con.cursor()
    query = """SELECT a.id_product, a.prod, a.description, a.price, a.color, b.name as 'brands'
            FROM product a, brand b WHERE a.fk_id_brand = b.id_brand"""
    result = c.execute(query)
    products = result.fetchall()
    con.close()
    return products


def get_products_by_brand(id_brand):
    #Get all the products with the same brand
    con = connect()
    c = con.cursor()
    query = """SELECT a.id_product, a.prod, a.description, a.price, a.color, b.name as 'brands'
            FROM product a, brand b WHERE a.fk_id_brand = b.id_brand
            AND a.fk_id_brand = ?"""
    result = c.execute(query, [id_brand])
    products = result.fetchall()
    con.close()
    return products

    
def get_products_name():
    #Get the name of the all products on table 'product'
    con = connect()
    c = con.cursor()
    query = """SELECT * FROM product"""
    result = c.execute(query)
    products = result.fetchall()
    wordlist = []
    for row in range(len(products)):
        for word in range(1,5):
            wordlist.append(str(products[row][word]))
    brands = get_brands()
    con.close()
    return wordlist


def search_product(word):
    #Search the word in the tables and return the product with this word
    #on the table
    con = connect()
    c = con.cursor()
    query = """SELECT a.id_product, a.prod, a.description, a.price, a.color, b.name as 'brands'
            FROM product a, brand b WHERE a.fk_id_brand = b.id_brand
            AND (a.prod LIKE '%'||?||'%' OR a.description LIKE '%'||?||'%' OR a.color
                LIKE '%'||?||'%' OR a.price LIKE '%'||?||'%')"""

    result = c.execute(query, [word, word, word, word])
    products = result.fetchall()
    con.close()
    return products


if __name__ == "__main__":

    products = get_product()
    for product in products:
        print product['prod']
