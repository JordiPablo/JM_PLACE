import db
import model
from db_models import Carrito, Product,User,Buyed
from datetime import datetime,date,time, timedelta 


def closeSessionByUserId (userid):
    user= model.getUserById(userid)
    user.num_buyed =0
    user.name_buyed =''
    model.delAllCarrito ()
    db.session.commit()

def getUserAndAllProducts (userid):
    user= model.getUserById(userid)
    todos_los_productos = model.getAllProducts()
    return user,todos_los_productos

def doVendedorLogin (user,todos_los_productos):
    #print('dentro del Vendedor')
    products_seller_ = model.getProductsBySuplierID(user.id)
    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in products_seller_:
        value_sold= model.getBuyedByReference (a.reference)
        if a.name not in dic_sold:
            dic_sold [a.name]=0
        if value_sold == None:
            dic_sold[a.name]= 0                    
        else:
            for i in value_sold:
                dic_sold [a.name] += i.cuantity_PBuyed
        
    for name, value in dic_sold.items ():
        list_sold.append(name)
        list_value_sold.append(int(value))
    
    if list_value_sold==[]: #si la lista esta vacia te da un error a la hora de generar la grafica
        list_value_sold =[0] # intorducimos un valor para que no de errores
    maxi=max(list_value_sold)

    dic_sold_all ={}
    list_sold_all=[]
    list_value_sold_all=[] 
    pb_seller_all = model.getAllBuyed ()

    for product in todos_los_productos: #declarada al inicio
        if product.name not in dic_sold_all:
            dic_sold_all[product.name]=0
        for pb in pb_seller_all:
            if product.reference == pb.ref_PBuyed:
                dic_sold_all [product.name] += pb.cuantity_PBuyed

    for name_all, value_all in dic_sold_all.items ():
        list_sold_all.append(name_all)
        list_value_sold_all.append(int(value_all))

    if list_value_sold_all==[]: 
        list_value_sold_all =[0] 
    
    max_all= max (list_value_sold_all)
    return products_seller_, maxi,list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all



def doAdminLogin (user,todos_los_productos):
        all_sellers = model.getAllUserByType('Vendedor')
        list_num_products_seller= []
        for user1 in all_sellers:
            
            if user1.type == 'Vendedor':
                all_products_ = model.getAllProductsBySuplierId (user1.id) 
                num_products = len (all_products_)
                list_num_products_seller.append(num_products)

        all_buyers= model.getAllUserByType('Comprador')
        list_num_products_buyers= []
        for user_buyer in all_buyers:
            
            if user_buyer.type == 'Comprador':
                all_products_ = model.getAllProductsBySuplierId (user.id)
                num_products = len (all_products_)
                list_num_products_buyers.append(num_products) 
        
        dic_sold_all ={}
        list_sold_all=[]
        list_value_sold_all=[] 
        pb_seller_all = model.getAllBuyed ()

        for product in todos_los_productos: #declarada al inicio
            if product.name not in dic_sold_all:
                dic_sold_all[product.name]=0
            for pb in pb_seller_all:
                if product.reference == pb.ref_PBuyed:
                    dic_sold_all [product.name] += pb.cuantity_PBuyed

        for name_all, value_all in dic_sold_all.items ():
            list_sold_all.append(name_all)
            list_value_sold_all.append(int(value_all))

        if list_value_sold_all==[]: 
            list_value_sold_all =[0] 
        
        max_all= max (list_value_sold_all)
        print (list_value_sold_all)
        return all_sellers,list_num_products_seller, all_buyers,list_sold_all, list_value_sold_all,max_all

def deleteItem (referenceC,userid,num_buyed):
    remove_cuantity = model.getCarritoByReference (referenceC)
    num_buyed=int(num_buyed) - remove_cuantity.cantidadC
    model.deleteCarritoByReference (referenceC)        
    user= model.getUserById(userid)
    user.num_buyed=num_buyed
    db.session.commit()
    return userid,user.num_buyed

def confirmBuy (id):
    all_products_carrito = model.getAllCarrito ()
    count =0 #contador de productos comprados por el usuario
    for products in all_products_carrito:
        count +=1 
        item_bought = Buyed (
            ref_PBuyed = products.referenceC,
            cuantity_PBuyed =products.cantidadC,
            data = datetime.now()
        )
        db.session.add(item_bought)
    
    model.delAllCarrito()
    user = model.getUserById(id)
    user.num_buyed = 0
    user.total_buyed +=count
    db.session.commit()
    return user

def buyProduct (id,userid,reference):
    product = model.getProductById(id) 
    product.numItems -= 1
    if product.numItems < 0:
        product.numItems = 0
    
    element_cesta = model.getCarritoByReference (reference)

    if element_cesta == None:
        carrito = Carrito(
        referenceC = product.reference,
        nameC = product.name, 
        priceC= product.price,
        cantidadC= 1  
        )
        db.session.add(carrito)
        db.session.commit()

    else:
        element_cesta.cantidadC +=1
        db.session.commit()

    all_users= model.getAllUsers ()
    for user in all_users:
        if user.id ==int(userid):
            todos_los_productos = model.getAllProducts()
            user.num_buyed+=1
            db.session.commit()

    return user.num_buyed, user,todos_los_productos

def deleteProduct(product_id,user_id):
    
    model.deleteProductById (product_id)
    list_products = model.getProductsBySuplierID(user_id)
    user = model.getUserById(user_id)

    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in list_products:
        value_sold= model.getBuyedByReference (a.reference)
        if a.name not in dic_sold:
            dic_sold [a.name]=0

        if value_sold == None:
            dic_sold[a.name]= 0                    
        else:
            for i in value_sold:
                dic_sold [a.name] += i.cuantity_PBuyed
        print (dic_sold)

    for name, value in dic_sold.items ():
        list_sold.append(name)
        list_value_sold.append(int(value))
    
    if list_value_sold==[]: 
        list_value_sold =[0]

    maxi=max(list_value_sold)

    dic_sold_all ={}
    list_sold_all=[]
    list_value_sold_all=[]
    
    pb_seller_all = model.getAllBuyed ()
    todos_los_productos = model.getAllProducts()
    for product in todos_los_productos: #declarada al inicio
        if product.name not in dic_sold_all:
            dic_sold_all[product.name]=0
        for pb in pb_seller_all:
            if product.reference == pb.ref_PBuyed:
                dic_sold_all [product.name] += pb.cuantity_PBuyed


    for name_all, value_all in dic_sold_all.items ():
        list_sold_all.append(name_all)
        list_value_sold_all.append(int(value_all))

    if list_value_sold_all==[]: 
        list_value_sold_all =[0] 
    
    max_all= max (list_value_sold_all)
    return user,list_products,maxi, list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all