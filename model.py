
import db
from db_models import Carrito, Product,User,Buyed

""" User queries"""
def getUserById (userid):
    return db.session.query(User).filter_by(id=int(userid)).first()
    

def getAllUsers ():
    return db.session.query(User).all()

def getAllUserByType (userType):
    return db.session.query(User).filter_by(type = userType).all()

def deleteUserById (userid):
    db.session.query(User).filter_by(id=int(userid)).delete()
    db.session.commit()

""" Product queries"""

def getAllProducts ():
    return db.session.query(Product).all()

def getProductById(productId):
    return db.session.query(Product).filter_by(id=int(productId)).first()

def getProductsBySuplierID (suplierId):
    return db.session.query(Product).filter_by(id_suplier=int(suplierId))

def getAllProductsBySuplierId (suplierId):
    return db.session.query(Product).filter_by(id_suplier = suplierId).all()

def deleteProductById (productId):
    db.session.query(Product).filter_by(id=int(productId)).delete()
    db.session.commit()

"""Buyed queries"""

def getBuyedByReference (reference):
    return db.session.query(Buyed).filter_by(ref_PBuyed = reference)

def getAllBuyed ():
    return db.session.query(Buyed).all()

"""Carrito queries"""

def getCarritoByReference (reference):
    return db.session.query(Carrito).filter_by(referenceC=reference).first()

def getAllCarrito ():
    return db.session.query(Carrito).all()

def deleteCarritoByReference (reference):
    return db.session.query(Carrito).filter_by(referenceC=reference).delete()


def delAllCarrito ():
    db.session.query(Carrito).delete()
