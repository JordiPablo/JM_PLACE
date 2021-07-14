from flask import Flask, render_template,request,redirect,url_for
from sqlalchemy.orm import session
from sqlalchemy.sql.elements import Null
import db
import controller
from db_models import Carrito, Product,User,Buyed

import model
app = Flask (__name__)


@app.route ('/')
def home ():
    return render_template("login.html")

@app.route ('/signup')
def signup ():
    return render_template("signup.html")

@app.route ('/shop/<id>/<num_buyed>')
def shop (id,num_buyed):
    user, todos_los_productos= controller.getUserAndAllProducts (id)
    return render_template("shop.html",lista_de_productos=todos_los_productos, user_obj=user,num_buyed=num_buyed)

@app.route ('/close_sesion/<id>', methods = ['POST'])
def close_sesion (id):
    controller.closeSessionByUserId(id)
    return redirect(url_for('home'))
    
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

    all_users= model.getAllUsers ()
    email = request.form ['email']
    password=request.form ['password']

    for user in all_users:
        if user.email == email and user.password == password: 
            todos_los_productos = model.getAllProducts()
            if user.type == 'Comprador': 
                return render_template('shop.html',user_obj=user,lista_de_productos =todos_los_productos)

            if user.type == 'Vendedor':
                products_seller_, maxi,list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all = controller.doVendedorLogin(user,todos_los_productos)
                return render_template('seller.html',user_obj=user, all_products=products_seller_, maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)
            
            if user.type == 'Administrador':
                all_sellers,list_num_products_seller, all_buyers,list_sold_all, list_value_sold_all,max_all = controller.doAdminLogin (user,todos_los_productos)
                return render_template('admin.html',user_obj=user,obj_all_users_sellers=all_sellers,num_products=list_num_products_seller, obj_all_users_buyers=all_buyers,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)

    return render_template('wrong_login.html')

@app.route ('/redirect_home')
def redirect_home ():
    return redirect(url_for('home')) 

@app.route ('/delete_item/<referenceC>/<userid>/<num_buyed>',methods = ['POST'])
def delete_item(referenceC,userid,num_buyed):
    userid,num_buyed = controller.deleteItem(referenceC,userid,num_buyed)
    return redirect(url_for('cesta',id=userid,num_buyed=num_buyed))

@app.route ('/cesta/<id>/<num_buyed>')
def cesta (id,num_buyed):
    all_products_carrito = model.getAllCarrito ()
    user = model.getUserById(id)

    return render_template('cesta.html',all_products=all_products_carrito, obj_user=user,num_buyed=num_buyed)

@app.route ('/confirm_buy/<id>',methods=['POST'])
def confirm_buy (id):
    user=controller.confirmBuy (id)
    return render_template('buyDone.html', user_obj=user)

@app.route ('/buy_product/<id>/<userid>/<reference>/',methods = ['POST'])
def buy_product(id,userid,reference):
    num_buyed, user,todos_los_productos= controller.buyProduct (id,userid,reference)
    return render_template('shop.html', num_buyed= num_buyed, user_obj=user,lista_de_productos =todos_los_productos)
    
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
    user = model.getUserById(iduser)
    list_products = model.getProductsBySuplierID(iduser)

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



    return render_template ("seller.html",user_obj = user, all_products= list_products, maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)

@app.route ('/modify_product/<product_id>/<user_id>/<admin_user>',methods=['POST'])
def modify_product (product_id,user_id,admin_user=None):
    product = model.getProductById(product_id) 
    user = model.getUserById(user_id)

    return render_template("modify_product.html",product_obj=product,user_obj=user,admin_user=admin_user)

@app.route ('/delete_product/<product_id>/<user_id>', methods=['POST'])
def delte_product (product_id,user_id):
    admin_id=request.args.get('admin_id')
    user,list_products,maxi, list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all = controller.deleteProduct (product_id,user_id)
    if admin_id == None:
        return render_template('seller.html',user_obj=user,all_products=list_products,maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)
    if admin_id != None:
        return render_template ('admin_seller.html',obj_user=user,all_products=list_products,admin_id=admin_id)


@app.route ('/confirm_modify/<product_id>/<user_id>', methods = ['POST'])
def confirm_modify (product_id,user_id):
    product = model.getProductById(product_id) 
    product.name = request.form ['new_name']
    product.description = request.form ['new_description']
    product.reference = request.form ['new_ref']
    product.numItems = request.form ['new_NumItem']
    product.warehouse_place = request.form ['new_warehouse_place']
    db.session.commit()
    admin_id=request.args.get('admin_id')

    user,list_products,maxi, list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all = controller.confirmModify(user_id)

    if admin_id == None:
        return render_template('seller.html',user_obj=user,all_products=list_products,maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)
    if admin_id != None:
        return render_template ('admin_seller.html',obj_user=user,all_products=list_products,admin_id=admin_id)


@app.route ('/see_sellers/<user_id>/<admin_id>', methods=['POST'])
def see_sellers (user_id,admin_id):
    user = model.getUserById(user_id)
    list_products = model.getAllProductsBySuplierId (user_id)
    return render_template ('admin_seller.html',obj_user=user,all_products=list_products,admin_id=admin_id)


@app.route ('/modify_seller/<user_id>/<admin_id>', methods=['POST'])
def modify_seller (user_id,admin_id):
    user = model.getUserById(user_id)
    return render_template ('modify_seller.html',obj_user=user,admin_id=admin_id)

@app.route ('/confirm_modfy_seller/<user_id>/<admin_id>/<user_type>', methods=['POST'])
def confirm_modfy_seller (user_id,admin_id,user_type):
    user = model.getUserById(user_id)

    user.name = request.form ['new_name']
    user.surnames = request.form ['new_surnames']
    user.sex = request.form ['new_sex']
    user.phone = request.form ['new_phone']
    user.province = request.form ['new_province']
    user.email = request.form ['new_email']
    user.password = request.form ['new_password']
    user.type = user_type
    db.session.commit()

    user = model.getUserById(user_id)
    list_products = model.getAllProductsBySuplierId (user_id)
    
    return render_template ('admin_seller.html',obj_user=user,all_products=list_products,admin_id=admin_id)

@app.route ('/delete_user/<user_id>/<admin_id>', methods=['POST'])
def delete_user (user_id,admin_id):
    user,all_sellers,list_num_products_seller, all_buyers,list_sold_all, list_value_sold_all,max_all = controller.deleteUser(user_id,admin_id)
    return render_template('admin.html',user_obj=user,obj_all_users_sellers=all_sellers,num_products=list_num_products_seller, obj_all_users_buyers=all_buyers,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)

@app.route ('/modify_buyer/<user_id>/<admin_id>', methods=['POST'])
def modify_buyer (user_id,admin_id):
    user = model.getUserById(user_id)
    return render_template ('admin_buyer.html',obj_user=user,admin_id=admin_id)


""" Inizialice backend, to start the web"""
if __name__=='__main__':
    db.Base.metadata.create_all(db.engine)
    app.run (debug=True)