from re import template
from flask import Flask, render_template,request,redirect,url_for
from sqlalchemy.orm import session
from sqlalchemy.sql.elements import Null
import db
from models import Carrito, Product,User,Buyed
from datetime import datetime,date,time, timedelta 

app = Flask (__name__)


@app.route ('/')
def home ():
    return render_template("login.html")

@app.route ('/signup')
def signup ():
    return render_template("signup.html")

@app.route ('/shop/<id>/<num_buyed>')
def shop (id,num_buyed):
    user= db.session.query(User).filter_by(id=int(id)).first()
    todos_los_productos = db.session.query(Product).all()
    return render_template("shop.html",lista_de_productos=todos_los_productos, user_obj=user,num_buyed=num_buyed)

@app.route ('/close_sesion/<id>', methods = ['POST'])
def close_sesion (id):
    all_users= db.session.query(User).all()
    for user in all_users:
        if user.id == int(id):
            user.num_buyed =0
            user.name_buyed =''
            db.session.query(Carrito).delete()
            db.session.commit()
            return redirect(url_for('home'))
    return('error')

@app.route('/sign_up',methods = ['POST'])
def new_client():
    user = User (
        name = request.form ['name'],  
        surnames = request.form ['surnames'], 
        sex = request.form ['cont_sex'],
        phone=request.form ['phone'],
        province = request.form ['province'],
        email=request.form ['email'],
        password=request.form ['password'],
        type = request.form ['type'],
        )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home')) 

@app.route('/login',methods = ['POST'])
def login():

    all_users= db.session.query(User).all()
    email = request.form ['email']
    password=request.form ['password']

    for user in all_users:
        if user.email == email and user.password == password: 
            todos_los_productos = db.session.query(Product).all()
            if user.type == 'Comprador': 
                return render_template('shop.html',user_obj=user,lista_de_productos =todos_los_productos)
            if user.type == 'Vendedor':
                #print('dentro del Vendedor')
                products_seller_ = db.session.query(Product).filter_by(id_suplier=int(user.id))

                dic_sold ={}
                list_sold=[]
                list_value_sold=[]
                for a in products_seller_:
                    value_sold= db.session.query(Buyed).filter_by(ref_PBuyed = a.reference)
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
                pb_seller_all = db.session.query(Buyed).all()

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
                return render_template('seller.html',user_obj=user, all_products=products_seller_, maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)
            
            if user.type == 'Administrador':

                all_users_=db.session.query(User).filter_by(type = 'Vendedor').all()
                list_num_products= []
                for user in all_users_:
                    print (user.name)
                    if user.type == 'Vendedor':
                        all_products_ = db.session.query(Product).filter_by(id_suplier = user.id).all()
                        num_products = len (all_products_)
                        list_num_products.append(num_products)

                return render_template('admin.html',obj_all_users=all_users_,num_products=list_num_products)


    return render_template('wrong_login.html')

@app.route ('/redirect_home')
def redirect_home ():
    return redirect(url_for('home')) 

@app.route ('/delete_item/<referenceC>/<userid>/<num_buyed>',methods = ['POST'])
def delete_item(referenceC,userid,num_buyed):
    remove_cuantity = db.session.query(Carrito).filter_by(referenceC=referenceC).first()
    num_buyed=int(num_buyed) - remove_cuantity.cantidadC
    db.session.query(Carrito).filter_by(referenceC=referenceC).delete()
    user= db.session.query(User).filter_by(id=int(userid)).first()

    user.num_buyed=num_buyed
    db.session.commit()
    return redirect(url_for('cesta',id=userid,num_buyed=user.num_buyed))

@app.route ('/cesta/<id>/<num_buyed>')
def cesta (id,num_buyed):
    all_products_carrito = db.session.query(Carrito).all()
    user = db.session.query(User).filter_by(id=int(id)).first()

    return render_template('cesta.html',all_products=all_products_carrito, obj_user=user,num_buyed=num_buyed)

@app.route ('/confirm_buy/<id>',methods=['POST'])
def confirm_buy (id):
    all_products_carrito = db.session.query(Carrito).all()
    for products in all_products_carrito:
        item_bought = Buyed (
            ref_PBuyed = products.referenceC,
            cuantity_PBuyed =products.cantidadC,
            data = datetime.now()
        )
        db.session.add(item_bought)
    
    db.session.query(Carrito).delete()
    user = db.session.query(User).filter_by(id=int(id)).first()
    user.num_buyed = 0
    db.session.commit()
    return render_template('buyDone.html', user_obj=user)

@app.route ('/buy_product/<id>/<userid>/<reference>/',methods = ['POST'])
def buy_product(id,userid,reference):

    product = db.session.query(Product).filter_by(id=int(id)).first() 
    product.numItems -= 1
    if product.numItems < 0:
        product.numItems = 0
    
    element_cesta = db.session.query(Carrito).filter_by(referenceC = reference).first()

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

    all_users= db.session.query(User).all()
    for user in all_users:
        if user.id ==int(userid):
            todos_los_productos = db.session.query(Product).all()
            user.num_buyed+=1
            db.session.commit()

            return render_template('shop.html', num_buyed= user.num_buyed, user_obj=user,lista_de_productos =todos_los_productos)
    return ('Error al comprar')

@app.route('/add_product/<iduser>',methods = ['POST'])
def add_product (iduser):
    product = Product (
    reference = request.form ['reference'], 
    name = request.form ['name'],  
    price = request.form ['price'],
    numItems=request.form ['numItems'],
    warehouse_place = request.form ['warehouse_place'],
    description=request.form ['description'],
    id_suplier=iduser
    )
    db.session.add(product)
    db.session.commit()
    user = db.session.query(User).filter_by(id=int(iduser)).first()
    list_products = db.session.query(Product).filter_by(id_suplier=int(iduser))

    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in list_products:
        value_sold= db.session.query(Buyed).filter_by(ref_PBuyed = a.reference)
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
    
    pb_seller_all = db.session.query(Buyed).all()
    todos_los_productos = db.session.query(Product).all()
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



    return render_template ("seller.html",user_obj = user, all_products= list_products, maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)

@app.route ('/modify_product/<product_id>/<user_id>',methods=['POST'])
def modify_product (product_id,user_id):
    product = db.session.query(Product).filter_by(id=int(product_id)).first()
    user = db.session.query(User).filter_by(id=int(user_id)).first()

    return render_template("modify_product.html",product_obj=product,user_obj=user)

@app.route ('/delete_product/<product_id>/<user_id>', methods=['POST'])
def delte_product (product_id,user_id):
    print(product_id)
    print (user_id)
    db.session.query(Product).filter_by(id=int(product_id)).delete()
    db.session.commit()
    list_products = db.session.query(Product).filter_by(id_suplier=int(user_id))
    user = db.session.query(User).filter_by(id=int(user_id)).first()

    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in list_products:
        value_sold= db.session.query(Buyed).filter_by(ref_PBuyed = a.reference)
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
    
    pb_seller_all = db.session.query(Buyed).all()
    todos_los_productos = db.session.query(Product).all()
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
    return render_template('seller.html',user_obj=user,all_products=list_products,maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)


@app.route ('/confirm_modify/<product_id>/<user_id>', methods = ['POST'])
def confirm_modify (product_id,user_id):
    product = db.session.query(Product).filter_by(id=int(product_id)).first()
    product.name = request.form ['new_name']
    product.description = request.form ['new_description']
    product.reference = request.form ['new_ref']
    product.numItems = request.form ['new_NumItem']
    product.warehouse_place = request.form ['new_warehouse_place']
    db.session.commit()
    list_products = db.session.query(Product).filter_by(id_suplier=int(user_id))
    user = db.session.query(User).filter_by(id=int(user_id)).first()

    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in list_products:
        value_sold= db.session.query(Buyed).filter_by(ref_PBuyed = a.reference)
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
    
    pb_seller_all = db.session.query(Buyed).all()
    todos_los_productos = db.session.query(Product).all()
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
    return render_template('seller.html',user_obj=user,all_products=list_products,maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)



if __name__=='__main__':
    db.Base.metadata.create_all(db.engine)
    app.run (debug=True)