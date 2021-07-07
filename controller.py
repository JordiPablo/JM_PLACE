import db
import model
from db_models import Carrito, Product,User,Buyed


def closeSessionByUserId (userid):
    user= model.getUserById(userid)
    user.num_buyed =0
    user.name_buyed =''
    db.session.query(Carrito).delete()
    db.session.commit()

def getUserAndAllProducts (userid):
    user= model.getUserById(userid)
    todos_los_productos = db.session.query(Product).all()
    return user,todos_los_productos