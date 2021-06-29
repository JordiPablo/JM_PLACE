
# from os import name !! quitar sino da backs
from sqlalchemy.sql.expression import column
import db
from sqlalchemy import Column, Integer, String, Boolean

class User (db.Base):
    __tablename__ ='Users'

    id = Column (Integer,primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False) 
    surnames = Column(String(50), nullable=False)
    sex = Column(String)
    phone = Column (String (50))
    province = Column (String(100))
    email = Column(String(50), nullable=False)
    password = Column (String(8))
    type = Column (String(50))
    name_buyed= Column (String(50))
    num_buyed = Column (Integer)


    def __init__ (self,name,surnames,sex,phone,province,email,password,type,name_buyed='',num_buyed=0):
        self.name = name
        self.surnames = surnames
        self.sex = sex
        self.phone = phone
        self.province = province
        self.email = email
        self.password = password
        self.type = type # could be suplier, client,admin
        self.name_buyed = name_buyed #nombre producto comprado
        self.num_buyed=num_buyed #cantidad producto comprado

class Product (db.Base): ############# OJOOOOO FALTARIA FOTOOO###########

    __tablename__='Products'

    id = Column (Integer,primary_key=True,autoincrement=True)
    reference = Column (String)
    name = Column(String(100), nullable=False) 
    price = Column (Integer) 
    description = Column(String(50), nullable=False)
    numItems = Column(Integer)
    warehouse_place = Column (String(50))
    id_suplier = Column (Integer)
     
    def __init__ (self,reference,name,price,description,numItems,warehouse_place,id_suplier):
        self.reference = reference
        self.name = name
        self.price = price
        self.description = description
        self.numItems = numItems
        self.warehouse_place = warehouse_place
        self.id_suplier = id_suplier 

class Carrito (db.Base): ############# OJOOOOO FALTARIA FOTOOO###########

    __tablename__='Carrito'

    idC = Column (Integer,primary_key=True,autoincrement=True)
    referenceC= Column (String(50))
    nameC = Column (String(50))
    priceC = Column(Integer)
    cantidadC = Column (Integer)

    def __init__ (self,referenceC='',nameC='',priceC=int,cantidadC=int):
        self.referenceC=referenceC
        self.nameC=nameC
        self.priceC=priceC
        self.cantidadC=cantidadC

class Buyed (db.Base): ############# OJOOOOO FALTARIA FOTOOO###########

    __tablename__='elements_bought'
    id = Column (Integer,primary_key=True,autoincrement=True)
    ref_PBuyed = Column (String (1000))
    data= Column (String(100))
    cuantity_PBuyed = Column (Integer)


    def __init__ (self,ref_PBuyed,data,cuantity_PBuyed):
        self.ref_PBuyed = ref_PBuyed
        self.data = data
        self.cuantity_PBuyed =cuantity_PBuyed


