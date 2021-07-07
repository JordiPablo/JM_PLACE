
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
