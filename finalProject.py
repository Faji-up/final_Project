# IMPORTSs

from tkinter.ttk import *
import io
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
from tkinter import filedialog
import random
import sqlite3
import random
from datetime import datetime
import time
from datetime import timedelta
import sqlite3

###########
################################################################

window = Tk()
window_width = 450
window_heigth = 600
#window.maxsize(window_width, window_heigth)
#window.minsize(window_width, window_heigth)
window.title('SPARduct')

accounts_list = []
################################################################

tk_font = "Calibre"

bgcolor = "#eeeeee"
text_color = "red"
user_index = 0

######################### LISTS
user_product_listsaction_list = []
cart_list = {}
trans_code = "qwertyuiopasdfghjklzxcvbnm1234567890"
num = 0
date = datetime.now().date()
_time = time.localtime(time.time())
prd_key = 0
product_list = []
transaction_list = []

#Starting Position of uploaded products 
position_of_prdcts = 100

#Starting position of carts
position_of_cart = 100
################################################################
def open_id_image():
    global id_picture
    id_picture = filedialog.askopenfilename()

def upload_image_function():
    try:
        global product_img
        product_img = filedialog.askopenfilename()
    except Exception as e:
        messagebox.showerror("Sign in error","May kulang !\n Ayusin mo")

def on_mouse_wheel_prdcts_F(event):
    product_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

def on_mouse_wheel_cart_F(event):
    cart_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
############ ACCOUNTS
class Accounts():
    def __init__(self, id_pic, name, age, address, username, password):
        self.username = username
        self.password = password
        self.name = name
        self.address = address
        self.id_pic = id_pic
        self.age = age
        self.user_product_list = []
        self.product_indx = 0
        self.transaction_list = []

        self.my_container_of_product =[]

        self.date = datetime.now().date()

    def show_info(self):
        user_frame = LabelFrame(users_frame)
        user_frame.pack(side='left')

        user_image = Label(user_frame, image=self.id_pic)
        user_image.pack()

        user_name = Label(user_frame, text=f"Name : {self.name}")
        user_name.pack()

        user_age = Label(user_frame, text=f"Age : {self.age}")
        user_age.pack()

        user_address = Label(user_frame, text=f"Address : {self.address}")
        user_address.pack()

        user_DATE = Label(user_frame, text=f"School : {self.date}")
        user_DATE.pack()

    def get_img(self):
        return self.id_pic

    def get_date(self):
        return self.date

    def get_user_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_user_address(self):
        return self.address

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id_pic

    def add_product(self, product_img, product_name, product_price, product_stock, seller_contact):
        global prd_key
        global user_index
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        key = 0
        for x in c.fetchall():
            key = x[0]
        print("key = ", key)
        if key < prd_key:
            prd_key = key + 1
            print("prd key  change", prd_key)
        conn.commit()
        conn.close()
        print("prd before adding", prd_key)
        with open(product_img,'rb') as image_file:
            product_img = image_file.read()
        product = Products(sqlite3.Binary(product_img), product_name, product_price, product_stock, seller_contact, user_index, prd_key,
                           self.product_indx)
        product.save()

        accounts_list[user_index].user_product_list.append(product)
        prd_key += 1
        print("prd after adding ", prd_key)
        window.update()
        self.product_indx += 1

    def unshow_my_products(self):
        for items in self.user_product_list:
            items.unshow()

    def show_user_products(self):
        global user_index
        for items in self.user_product_list:
            if items == None:
                pass
            else:
                items.show_my_product()
                window.update()

    def show_cart(self):
        for key in cart_list.keys():
            if key == user_index:
                cart_list.get(key).pack()
            else:
                cart_list.get(key).pack_forget()

    def unshow_cart(self):
        for key in cart_list.keys():
            cart_list.get(key).pack_forget()



    def show_my_transaction(self, username,password):
        if username == self.username and password == self.password:
            for carts in accounts_list[user_index].transaction_list:
                    carts.pack()
        else:
            pass

    def unshow_my_transaction(self):
        for items in accounts_list:
            for carts in items.transaction_list:
                carts.pack_forget()


class Products(Accounts):
    def __init__(self, image_of_product, product_type, product_price, product_stock, seller_contact, product_index, id_num,
                 prd_indx):
        global user_index
        global position_y
        global date
        global product_img
        super().__init__(accounts_list[user_index].get_id(),
                         accounts_list[user_index].get_user_name(),
                         accounts_list[user_index].get_age(),
                         accounts_list[user_index].get_user_address(),
                         accounts_list[user_index].get_username(),
                         accounts_list[user_index].get_password())
        # products components
        self.prd_indx = prd_indx
        convert_to_img = Image.open(io.BytesIO(image_of_product))
        covert_to_img = convert_to_img.resize((40,40))
        convert_to_img = ImageTk.PhotoImage(covert_to_img)
        self.product_image = convert_to_img
        self.image_of_product = image_of_product
        self.id_num = id_num
        self.product_type = product_type
        self.product_price = int(product_price)
        self.product_stock = int(product_stock)
        self.seller_contact = seller_contact
        self.product_index = product_index

        # time
        self.local_t = time.localtime()
        self.date_posted = datetime.now().date()
        self.time_posted = time.strftime("%H:%M:%S", self.local_t)

        # products frame, labels and buttons
        self.product_container = LabelFrame(product_frame,width=600,height=300,bg='red')
        self.product_contact_f = Label(self.product_container, text=self.seller_contact)
        self.product_contact_f.text = self.seller_contact
        self.product_quan_f = Label(self.product_container, text=str(self.product_stock))
        self.product_quan_f.text = str(self.product_stock)
        self.product_price_f = Label(self.product_container, text=self.product_price)
        self.product_price_f.text = self.product_price
        self.product_image_f = Label(self.product_container, image=self.product_image)
        self.product_image_f.text = self.product_image
        self.product_name_f = Label(self.product_container, text=self.product_type)
        self.product_dt_f = Label(self.product_container,
                                  text=f"DATE POSTED: {self.date_posted}\nTIME: {self.time_posted}")
        self.product_container.bind('<Enter>', self.wide_view)
        self.product_container.bind('<Leave>', self.small_view)
        self.view_profile = Button(self.product_container, text='view', command=self.profile_view)
        # buy button
        self.buy_button = Button(self.product_container, text='add to cart')
        self.insert_to_prdtcs_F()

        # cart frame
        self.cart_f = LabelFrame(cart_frame)

        # transaction frame
        self.transaction_f = Label(user_transaction_frame)
        # trasaction history list


        self.frame = Frame(user_frame)
        self.label = Label(self.frame, image=self.id_pic)

        self.button_exit_prof = Button(self.frame, command=self.profile_unview, text="X")

        self.info_label = Label(self.frame,
                                text=f"Name:{self.get_user_name()}\nAge:{self.get_age()}\nAddress:{self.get_user_address()}")
        self.label.pack()
        self.info_label.pack()
        self.button_exit_prof.pack()

        # myproducts frame
        self.myproduct_container = LabelFrame(user_products_frame)
        self.myproduct_image_f = Label(self.myproduct_container, image=self.product_image)
        self.my_Pinfo = Label(self.myproduct_container,
                              text=f"Type: {self.product_type} Price: {self.product_price} Stock: {self.product_stock}")
        self.selfindex = product_index
        self.remove_button = Button(self.myproduct_container, text='remove',
                                    command=lambda: self.remove_product())
        self.my_Pinfo.pack()
        self.myproduct_image_f.pack()
        self.remove_button.pack()

        # date delivever
        self.time_of_deliver = datetime.now().date().today() + timedelta(days=(int(_time.tm_wday) + 7))

    def save(self):
        global user_index
        global product_img
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()

        product = [self.image_of_product, self.product_type, self.product_price, self.product_stock,
                   self.seller_contact, self.product_index]
        c.executemany(
            "INSERT INTO  products (product_img,product_type,product_price,product_stock,seller_contact,product_index) VALUES (?,?,?,?,?,?)",
            (product,))

        conn.commit()
        conn.close()

    def get_index(self):
        return self.product_index

    def show(self):
        global product_frame
        product_frame.bind("<Key>", self.move)
        index = user_index
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()
        if self.product_stock <= 0:
            delete = f"DElETE FROM products WHERE id={self.id_num}"
            c.execute(delete)
            conn.commit()
            conn.close()
            self.product_quan_f.config(text='sold out')
            self.my_Pinfo.config(text=f"SOLD OUT")
            self.buy_button.config(state=DISABLED)
            self.product_container.pack_forget()
            self.myproduct_container.pack_forget()

        else:
            pass
        conn.commit()
        conn.close()

    def move(self, event):
        self.product_container.place(x=200, y=self.product_container.winfo_y() + 10)

        window.update()
    def insert_to_prdtcs_F(self):
        global position_of_prdcts
        self.product_image_f.pack()
        self.product_name_f.pack()
        self.product_price_f.pack()
        self.product_quan_f.pack()
        self.product_contact_f.pack()
        self.product_dt_f.pack()
        self.buy_button.config(command=lambda: self._add_tocart())
        product_frame.create_window((0, position_of_prdcts), window=self.product_container,width=window_width)

        self.product_container.bind("<Configure>", lambda e: product_frame.configure(scrollregion=product_frame.bbox("all")))
        self.product_container.bind("<MouseWheel>", on_mousewheel_prdcts_F)
        
        #increase and create new position of uploaded products by 150
        position_of_prdcts += 150
        
    def insert_to_cart_F(self):
        global position_of_each_cart
        cart_frame.create_window((0, position_of_each_cart), window=self.cart_f,width=window_width)

        self.cart_f.bind("<Configure>", lambda e: cart_frame.configure(scrollregion=cart_frame.bbox("all")))
        self.cart_f.bind("<MouseWheel>", on_mousewheel_cart_F)

        
        #self.product_container.config(width=window_width)
    
    def unshow(self):
        self.product_dt_f.pack_forget()
        self.myproduct_image_f.pack_forget()
        self.my_Pinfo.pack_forget()
        self.myproduct_container.pack_forget()
        self.remove_button.pack_forget()

    def unpack(self):
        self.product_container.pack_forget()
        self.myproduct_container.pack_forget()

    def show_my_product(self):

        if self.product_stock <= 0:
            conn = sqlite3.connect("Products.db")
            c = conn.cursor()
            delete = f"DElETE FROM products WHERE id={self.id_num}"
            c.execute(delete)
            conn.commit()
            conn.close()
            self.product_quan_f.config(text='sold out')
            self.my_Pinfo.config(text=f"SOLD OUT")
            self.buy_button.config(state=DISABLED)
            conn.commit()
            conn.close()
        else:
            self.myproduct_image_f.pack()
            self.my_Pinfo.pack()
            self.myproduct_container.pack()
            self.remove_button.pack()
    def wide_view(self, event):

        self.buy_button.pack()
        self.view_profile.pack()

    def small_view(self, event):
        self.buy_button.pack_forget()
        self.view_profile.pack_forget()

    def _add_tocart(self):

        global list_p
        global user_index
        product_frame.pack_forget()
        cart_frame.pack_forget()
        product_frame.pack_forget()
        menu_frame.pack_forget()

        buy_frame.pack()

        product_picture.config(image=self.product_image)

        amount.config(text=str('PHP' + str(self.product_price)))

        new_quan = StringVar()
        quan_menu.config(textvariable=new_quan, from_=0, to=self.product_stock)

        buy_button.config(command=lambda: self.transaction_method(new_quan.get()), text="BUY")

    def transaction_method(self, new_quan):
        global trans_code
        conn = sqlite3.connect("Products.db")
        conn2 = sqlite3.connect("Transaction.db")
        tran = conn2.cursor()
        c = conn.cursor()
        ask = messagebox.askyesno("info", "are you sure to buy this product?")
        if ask:

            code = ''
            quan = self.product_stock

            for i in range(5):
                code += str(trans_code[random.randint(0, 35)])
            self.product_stock -= int(new_quan)
            change = f"UPDATE products SET product_stock={self.product_stock} WHERE id={self.id_num}"
            c.execute(change)
            conn.commit()
            self.product_quan_f.config(text=str(self.product_stock))
            self.my_Pinfo.config(
                text=f"Type: {self.product_type} Price: {self.product_price} Stock: {self.product_stock}")

            print(self.product_stock)
            window.update()
            if self.product_stock <= 0:
                delete = f"DElETE FROM products WHERE id={self.id_num}"
                c.execute(delete)

                conn.commit()

                self.product_quan_f.config(text='sold out')
                self.my_Pinfo.config(text=f"SOLD OUT")
                self.buy_button.config(state=DISABLED)

            # save to the cart
            price = int(self.product_price)
            payment = str(int(new_quan) * price)
            product_p_c = Label(self.cart_f, image=self.product_image)
            product_info_c = Label(self.cart_f,
                                   text=f"Seller: {self.get_user_name()}\nProduct: {self.product_type}\nAmount: {self.product_price}\nQuantity: {quan}\nTransaction Code: {str(code)}\nPayment: {payment}\nDATE: {date}\nDATE OF DELIVER:{self.time_of_deliver}")

            product_p_c.pack()
            product_info_c.pack()
            cart_list.get(user_index).append(self.cart_f)

            # save the transaction
            product_p_t = Label(self.transaction_f, image=self.product_image)
            product_info_t = Label(self.transaction_f,
                                   text=f"Buyer: {accounts_list[user_index].get_user_name()}\nProduct: {self.product_type}\nTransaction Code: {str(code)}\nPayment: {payment}\nDATE OF DELIVER:{self.time_of_deliver}")
            button_paid = Button(self.transaction_f,text="paid",command=lambda : (product_info_t.config(text="paid")))
            button_paid.pack()
            product_p_t.pack()
            product_info_t.pack()
            accounts_list[self.product_index].transaction_list.append(self.transaction_f)

            # send transaction to the admin
            insert_transaction_to_tb = [self.image_of_product,self.get_user_name(),accounts_list[user_index].get_user_name(),self.product_type,int(payment),self.time_of_deliver,code,int(self.product_index),int(user_index)]
            tran.executemany("INSERT INTO transactions (product_img,seller_name,buyer_name,product_type,payment_amount,day_of_deliver,transaction_code,config_user_id,buyer_index) VALUES (?,?,?,?,?,?,?,?,?)",(insert_transaction_to_tb,))
            conn2.commit()
            transaction_list.append(
                str(f"Product:{self.product_type} | Seller:{self.get_user_name()} | Price:{self.product_price} >> Buyer:{accounts_list[user_index].get_user_name()} | Payment:{payment} | TRANSACTION CODE:{code}"))
        else:
            pass
        conn.commit()
        conn.close()
        conn2.commit()
        conn2.close()

    def profile_view(self):
        product_frame.pack_forget()
        sell_frame.pack_forget()
        cart_frame.pack_forget()
        profile_frame.pack_forget()
        menu_frame.pack_forget()

        self.frame.pack(expand=True, fill=BOTH)

    def profile_unview(self):
        self.frame.pack_forget()
        product_frame.pack(expand=True, fill=BOTH)

    def payment_frame(self):
        pass

    def get_name(self):
        return self.product_type

    def get_pro_date(self):
        return f"{self.date_posted}| {self.time_posted}"

    def get_image(self):
        return self.product_image

    def get_price(self):
        return self.product_price

    def remove_product(self):
        print("prd remove", self.id_num)
        self.myproduct_container.pack_forget()
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()
        delete = f"DElETE FROM products WHERE id={self.id_num}"
        c.execute(delete)
        remove_in_user_product_list(self.product_indx)

        conn.commit()
        conn.close()
        window.update()

    def get_address(self):
        return self.seller_address

    def get_contact(self):
        return self.seller_contact

    def get_quan(self):
        return self.product_stock

################################################################
def save_product(product_imagee, product_name, product_price, product_quan, seller_contact):
    global product_frame
    global num
    global product_img
    global product_list
    if (
            product_validation(product_imagee, product_name, product_price, product_quan, seller_contact)):
        img = Image.open(product_img)
        img = img.resize((40, 40))
        img = ImageTk.PhotoImage(img)
        accounts_list[user_index].add_product(product_imagee,
                                              product_name,
                                              product_price,
                                              product_quan,
                                              seller_contact,
                                              )

        prd = Label(inven_frame, image=img,
                    text=f"Seller:{accounts_list[user_index].get_user_name()} Type:{product_name} Price:{product_price} Stock:{product_quan}",
                    compound="left")
        prd.image = img
        product_list.append(prd)
        num += 1
        upload_name_of_product.delete(0, END)
        upload_price.delete(0, END)
        upload_stock.delete(0, END)
        upload_contact.delete(0, END)

    else:
        return messagebox.showerror('error', 'error')


def product_validation(product_img, product_type, product_price, product_stock, seller_con):
    if product_img == None and product_type == "" and product_price == '' and product_stock == '' and seller_con == '':
        return False
    else:
        return True


def remove_in_user_product_list(indexx):
    print("remove index", indexx)

    accounts_list[user_index].user_product_list.remove(accounts_list[user_index].user_product_list[indexx])
    for item in accounts_list[user_index].user_product_list:
        if len(accounts_list[user_index].user_product_list) == 0:
            pass
        else:
            item.product_indx -= 1
    print("new len of list", len(accounts_list[user_index].user_product_list))
    window.update()


#######################  SAVE ACCOUNT

def save_account(id_pic, name,address, username, password):
    global sign_in_username
    global accounts_list
    global age
    try:
        if sign_in_validation(id_pic, name,address, username, password):
            conn = sqlite3.connect('Accounts.db')
            c = conn.cursor()

            img = Image.open(id_pic)
            img = img.resize((60, 60))
            img = ImageTk.PhotoImage(img)
            account = Accounts(id_pic, name, address, username, password)
            accounts_list.append(account)
            with open(id_pic, 'rb') as image_file:
                id_picture = image_file.read()
                c.execute("INSERT INTO accounts (id_pic,name,age,address,username,password) VALUES (?,?,?,?,?,?)",
                          (sqlite3.Binary(id_picture), name,  address, username, password))
            conn.commit()
            conn.close()
            sign_in_username.delete(0, END)
            age.delete(0, END)
            sign_user_address.delete(0, END)
            sign_in_password.delete(0, END)
            confirm_pass.delete(0, END)
            show_log_in_frame()
        else:
            show_sign_in_frame()
    except Exception as e:
        messagebox.showerror("Sign in error","May kulang !\n Ayusin mo")

def sign_in_validation(id_pic, name,address, username, password):
    if not (
            id_pic == None or name == ''  or address == '' or username == ''):
        if password == confirm_pass.get():
            return True
    else:
        return False


#######################  ADMIN

def admin():
    global product_list

    log_in_canvas.pack_forget()
    admin_frame.pack(expand=True, fill=BOTH)

    conn = sqlite3.connect('Accounts.db')
    c = conn.cursor()

    c.execute("SELECT * FROM accounts ")
    for acc in c.fetchall():
        imga = Image.open(io.BytesIO(acc[1]))
        imga = imga.resize((60, 60))
        imgs = ImageTk.PhotoImage(imga)
        container = LabelFrame(users_frame)
        pro_img = Label(container, image=imgs)
        pro_img.image = imgs
        infos = Label(container, text=f"NO# {acc[0]} Name: {acc[2]} Age: {acc[3]} Address: {acc[4]}")
        container.pack()
        pro_img.pack()
        infos.pack()

    # user_infos = Label(users_frame,text=f"Name: {ac[1]}\nAge: {ac[2]}\nAddress: {ac[3]}")
    # user_infos.pack()
    conn.commit()
    conn.close()
    for products in product_list:
        products.pack()
    #product_list[0].pack()
    for items in transaction_list:
        Label(admin_tran_frame, text=items).pack()


def users(event):
    admin_menu_frame.pack_forget()
    inven_frame.pack_forget()
    admin_tran_frame.pack_forget()

    users_frame.pack(expand=True, fill=BOTH)

def inventory(event):
    admin_menu_frame.pack_forget()
    users_frame.pack_forget()
    admin_tran_frame.pack_forget()

    inven_frame.pack(expand=True, fill=BOTH)

def admin_log_out():
    pass

def admin_menu(event):
    users_frame.pack_forget()
    inven_frame.pack_forget()
    admin_tran_frame.pack_forget()

    admin_menu_frame.pack(expand=True, fill=BOTH)


def admin_tran(event):
    users_frame.pack_forget()
    inven_frame.pack_forget()
    admin_menu_frame.pack_forget()

    admin_tran_frame.pack(expand=True, fill=BOTH)


#######################   USERS


def user():
    window.update()


def home():
    global cart_list
    log_in_canvas.pack_forget()
    user_frame.pack(fill=BOTH, expand=True)
    for items in range(len(accounts_list)):
        accounts_list[items].show_products()


    # display user data such as cart,products and transaction hirtory
    for item in accounts_list[user_index].user_product_list:
        item.show_my_transaction(item.get_username(),item.get_password())

    for item in accounts_list[user_index].user_product_list:
        item.show_user_products()

    accounts_list[user_index].show_user_products()


def show_products(event):
    global products
    sell_frame.pack_forget()
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    #for x in accounts_list[user_index].user_product_list:
     #   x.product_container.pack()


    product_frame.pack(expand=True, fill=BOTH)


def myproducts(event):
    global cart_list
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_transaction_frame.pack_forget()
    sell_frame.pack_forget()
    for item in accounts_list[user_index].user_product_list:
        item.show_user_products()

    for items in accounts_list:
        if items == accounts_list[user_index] and len(accounts_list[user_index].user_product_list) != 0:
            items.show_user_products()
            window.update()
        else:
            items.unshow_my_products()
    user_products_frame.pack(expand=True, fill=BOTH)
def mytransaction(event):
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    sell_frame.pack_forget()

    for item in accounts_list[user_index].user_product_list:
        item.show_my_transaction(item.get_username(),item.get_password())


    user_transaction_frame.pack(expand=True, fill=BOTH)

def back_to_log_com():
    sign_in_canvas.pack_forget()
    log_in_canvas.pack(fill=BOTH,expand=True)

def add_product(event):
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    sell_frame.pack(expand=True, fill=BOTH)


def remove_product():
    pass


def menu(event):
    user_products_frame.pack_forget()
    cart_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    sell_frame.pack_forget()
    buy_frame.pack_forget()
    user_transaction_frame.pack_forget()

    menu_frame.pack(expand=True, fill=BOTH)


def cart(event):
    sell_frame.pack_forget()
    profile_frame.pack_forget()
    product_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    for key in cart_list.keys():
        if key == user_index:
            for cart in cart_list.get(key):
                cart.pack()
        else:
            for cart in cart_list.get(key):
                cart.pack_forget()
    cart_frame.pack(expand=True, fill=BOTH)


def profile(event):
    global user_index
    global accounts_list
    menu_frame.pack_forget()
    sell_frame.pack_forget()
    cart_frame.pack_forget()
    product_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()

    profile_frame.pack(expand=True, fill=BOTH)
    profile_pic.config(image=accounts_list[user_index].get_img())
    profile_NAME.config(text=accounts_list[user_index].get_user_name())
    profile_ADDRES.config(text=accounts_list[user_index].get_user_address())
    profile_AGE.config(text=accounts_list[user_index].get_age())
#scroll the products

def on_mousewheel(event):
    product_frame.yview_scroll(-1 * (event.delta // 120), "units")

def change_bg_color():
    log_in_canvas.itemconfig(switch,image=moon_img)
    log_in_canvas.config(bg='#414a4c')

    log_in_canvas.tag_bind(switch,"<Button>",lambda event: change_to_light())
def change_to_light():
    log_in_canvas.itemconfig(switch, image=sun_img)
    log_in_canvas.config(bg=bgcolor)
    log_in_canvas.tag_bind(switch, "<Button>", lambda event: change_bg_color())

def user_log_out(event):
    cart_frame.pack_forget()
    user_frame.pack_forget()
    for items in accounts_list:
        items.unshow_my_products()
        items.unshow_my_transaction()
    welcome()


def about():
    pass


################################################################
# center the window
def center_window(window, width, height, ):
    screen_width = window.winfo_screenwidth()
    screen_heigth = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_heigth - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


################################################################
def restore_db_to_list():
    global accounts_list
    global num
    global prd_key
    global product_list
    global cart_list

    products_list = []

    conn = sqlite3.connect("Accounts.db")
    conn2 = sqlite3.connect("Products.db")
    conn3 = sqlite3.connect("Transaction.db")

    c = conn.cursor()
    c2 = conn2.cursor()
    c3 = conn3.cursor()
    # c2.execute("CREATE TABLE IF NOT EXISTS products (product_img BLOB,product_type text,product_price INTEGER,product_stock INTEGER,product_index INTEGER)")
    c.execute("SELECT * FROM accounts")
    c2.execute("SELECT * FROM products")


    index = 0
    #RESTORE ACCOUNTS FROM THE DATABASE ACCOUNTS TO LIST OF ACCOUNTS
    for acc in c.fetchall():
        img = Image.open(io.BytesIO(acc[1]))
        img = img.resize((60, 60))
        img = ImageTk.PhotoImage(img)
        account = Accounts(img, acc[2], acc[3], acc[4], acc[5], acc[6])
        accounts_list.append(account)
        print("name user:",accounts_list[index].get_user_name())
        index += 1
    print("account len is ",len(accounts_list))
    products_restore = c2.fetchall()

    #RESTORE PRODUCTS FROM DATABASE PRODUCTS TO ITS OWNERS
    for acc_index in range(len(accounts_list)):

        print("len(",acc_index,")")
        for prod in products_restore:
            print("prod[6]",int(prod[6]),"=",acc_index)
            if prod[6] == acc_index:
                print("prod[6]", int(prod[6]))
                img = Image.open(io.BytesIO(prod[1]))
                img = img.resize((60, 60))
                img = ImageTk.PhotoImage(img)
                product = Products(prod[1], prod[2], prod[3], prod[4], prod[5], acc_index, prod[0], accounts_list[acc_index].product_indx)
                prd = Label(inven_frame, image=img,
                                          text=f"Seller:{accounts_list[acc_index].get_user_name()} Type:{prod[2]} Price:{prod[3]} Stock:{prod[4]}",
                                          compound="left")
                prd.image = img

                product_list.append(prd)
                print(prod[0])
                accounts_list[acc_index].user_product_list.append(product)

                accounts_list[acc_index].product_indx += 1
                print("prd number before", prd_key)
                if prod[0] > prd_key:
                    prd_key = prod[0]
                    print("prd number after", prd_key)


            conn.commit()
    prd_key += 1
    print("prd last ", prd_key)

    #RESTORE TRANSACTION LIST
    for user_id in range(len(accounts_list)):
        c3.execute("SELECT * FROM transactions")
        for _tran in c3.fetchall():
            if _tran[8] == user_id:
                print(_tran[8], 'tran' , user_index)
                transaction_container = LabelFrame(user_transaction_frame)
                tran_img = Image.open(io.BytesIO(_tran[1]))
                tran_img = tran_img.resize((40,40))
                tran_img = ImageTk.PhotoImage(tran_img)
                product_p_t = Label(transaction_container, image=tran_img)
                product_p_t.image = tran_img
                product_info_t = Label(transaction_container,
                                       text=f"Buyer: {_tran[3]}\nProduct: {_tran[4]}\nTransaction Code: {_tran[7]}\nPayment: {_tran[5]}\nDATE OF DELIVER:{_tran[6]}")
                button_paid = Button(transaction_container, text="paid",
                                     command=lambda: product_info_t.config(text="paid"))
                button_paid.pack()
                product_p_t.pack()
                product_info_t.pack()
                accounts_list[user_id].transaction_list.append(transaction_container)
                print('gwrtygwhg')

    #RESTORE USER CART FROM DB
    for user_id in range(len(accounts_list)):
        c3.execute("SELECT * FROM transactions")
        cart_list.update({user_id:[]})
        for _tran in c3.fetchall():
            if _tran[9] == user_id:
                print("9:", _tran[9], "user_id = ", user_id)

                cart_img = Image.open(io.BytesIO(_tran[1]))
                cart_img = cart_img.resize((40, 40))
                cart_img = ImageTk.PhotoImage(cart_img)
                cart_user_frame = LabelFrame(cart_frame)

                product_p_c = Label(cart_user_frame, image=cart_img)
                product_p_c.image = cart_img
                product_info_c = Label(cart_user_frame,
                                       text=f"Seller: {_tran[2]}\nProduct: {_tran[4]}\nTransaction Code: {_tran[7]}\nPayment: {_tran[5]}\nDATE OF DELIVER:{_tran[6]}")

                product_p_c.pack()
                product_info_c.pack()
                cart_list.get(user_id).append(cart_user_frame)
                print("name",_tran[9])


    conn2.close()
    conn3.close()
    conn.close()


def welcome():
    home_canvas.pack(expand=True, fill=BOTH)


###############################################################


################################################################

def log_in_validation():
    global user_index
    conn = sqlite3.connect('Accounts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    if log_in_username.get() == "admin" and log_in_password.get() == 'admin':
        log_in_password.delete(0, END)
        log_in_username.delete(0, END)
        admin()
    else:
        for acc in c.fetchall():
            if log_in_username.get() == acc[5] and log_in_password.get() == acc[6]:
                user_index = acc[0] - 1
                log_in_password.delete(0, END)
                log_in_username.delete(0, END)
                home()
                break

    conn.commit()
    conn.close()

###############################################################
def write_text(index):
    if index <= len(tagline):
        partial_text = tagline[:index]
        home_canvas.itemconfig(bsu_tagline,text=partial_text)

        home_canvas.after(40,write_text,index+1)


def enter_txt_U():
    log_in_canvas.itemconfig(usr_name_line, fill="black",width=1)
    window.update()

    log_in_canvas.itemconfig(usr_p_line, fill="#F3F2ED", width=1)
    window.update()

    print('wrht')
def leave_txt_U():
    pass

def enter_txt_P():
    log_in_canvas.itemconfig(usr_name_line, fill="#F3F2ED", width=1)
    window.update()

    log_in_canvas.itemconfig(usr_p_line, fill="black", width=1)
    window.update()
################################################################

def show_password():
    print("aeg")
    log_in_password.config(show='')
    log_in_password.show = ""
    log_in_canvas.itemconfig(pass_btn_config,image=hide_pass_img)
    log_in_canvas.tag_unbind(pass_btn_config, "<Button>")
    log_in_canvas.tag_bind(pass_btn_config, "<Button>", lambda event: hide_password())
    window.update()

################################################################

def hide_password():
    log_in_password.config(show='*')
    log_in_password.show = "*"
    log_in_canvas.itemconfig(pass_btn_config,image=show_pass_img)
    log_in_canvas.tag_unbind(pass_btn_config, "<Button>")
    log_in_canvas.tag_bind(pass_btn_config, "<Button>",lambda event: show_password())
    window.update()
################################################################
def show_log_in_frame():
    sign_in_canvas.pack_forget()

    home_canvas.pack_forget()

    log_in_canvas.pack(expand=True, fill=BOTH)


################################################################

def show_sign_in_frame():
    log_in_canvas.pack_forget()
    sign_in_canvas.pack(expand=True, fill=BOTH)


################################################################

def line_move_to_home(event):
    line.place(x=window_width-428,y=27)



def line_move_to_menu(event):
    line.place(x=window_width - 49, y=27)

def line_move_to_prof(event):
    line.place(x=window_width - 138, y=27)

def line_move_to_search(event):
    line.place(x=window_width - 338, y=27)

def line_move_to_cart(event):
    line.place(x=window_width - 238, y=27)
############ center the window
center_window(window, window_width, window_heigth)
########################## BSU LOGO

logo_big = Image.open('images/logo.png')
logo_big = logo_big.resize((100, 100))
logo_big = ImageTk.PhotoImage(logo_big)

logo_med = Image.open('images/logo.png')
logo_med = logo_med.resize((80, 80))
logo_med = ImageTk.PhotoImage(logo_med)

logo_small = Image.open('images/logo.png')
logo_small = logo_small.resize((50, 50))
logo_small = ImageTk.PhotoImage(logo_small)

user_logo = Image.open('images/user.png')
user_logo = user_logo.resize((25, 20))
user_logo = ImageTk.PhotoImage(user_logo)

search_logo = Image.open('images/search logo.png')
search_logo = search_logo.resize((25, 20))
search_logo = ImageTk.PhotoImage(search_logo)

menu_logo = Image.open('images/menu-burger.png')
menu_logo = menu_logo.resize((25, 20))
menu_logo = ImageTk.PhotoImage(menu_logo)

product_logo = Image.open('images/shopping-cart (1).png')
product_logo = product_logo.resize((25, 20))
product_logo = ImageTk.PhotoImage(product_logo)


home_logo = Image.open('images/home.png')
home_logo = home_logo.resize((25, 20))
home_logo = ImageTk.PhotoImage(home_logo)


sign_outl = Image.open('images/sign-out.png')
sign_outl = sign_outl.resize((25, 20))
sign_outl = ImageTk.PhotoImage(sign_outl)


line_logo = Image.open('images/line.png')
line_logo = line_logo.resize((25, 1))
line_logo = ImageTk.PhotoImage(line_logo)

bg_img = Image.open('images/homebg.jpg')
bg_img = bg_img.resize((window_width, 700))
bg_img = ImageTk.PhotoImage(bg_img)

bg_2 = Image.open('images/bg2.png')
bg_2 = bg_2.resize((window_width, 700))
bg_2 = ImageTk.PhotoImage(bg_2)


########################## ADMIN WINDOW

admin_frame = Canvas(window)
############

admin_label = Label(admin_frame, text="Admin", font=(tk_font, 10), bg=bgcolor)
admin_label.pack(fill=BOTH)

############

admin_frames_but = LabelFrame(admin_frame,
                              bg=bgcolor,
                              highlightcolor='black',
                              highlightthickness=1,
                              highlightbackground='black'
                              )
admin_frames_but.pack(fill=X)

#
inventory_frame_but = Label(admin_frames_but,
                            text='Inventory',
                            width=15
                            )
inventory_frame_but.pack(side='left')
inventory_frame_but.bind('<Button>', inventory)

#
users_frame_but = Label(admin_frames_but,
                        text='Users',
                        width=15
                        )
users_frame_but.pack(side='left')
users_frame_but.bind('<Button>', users)
#
admin_tran_frame_but = Label(admin_frames_but,
                             text='Transaction',
                             width=15
                             )
admin_tran_frame_but.pack(side='left')
admin_tran_frame_but.bind('<Button>', admin_tran)

#
admin_menu_frame_but = Label(admin_frames_but,
                             text='Menu',
                             width=23
                             )
admin_menu_frame_but.pack(side='right')
admin_menu_frame_but.bind('<Button>', admin_menu)

########################## INVENTORY WINDOW FRAME

inven_frame = Canvas(admin_frame, bg='red')

########################## USERS WINDOW FRAME

users_frame = Canvas(admin_frame, bg='blue')

########################## ADMIN MENU WINDOW FRAME

admin_menu_frame = Canvas(admin_frame, bg='green')

########################### ADMIN TRANSACTION WINDOW FRAME

admin_tran_frame = Canvas(admin_frame, bg='black')
###################################################################################### USER WINDOW FRAME


user_frame = Canvas(window, bg=bgcolor)

bottom_can_bar = Canvas(user_frame,width=window_width,height=35,bg='white')
bottom_can_bar.pack(side="bottom")
################################################################
user_bg_img = Image.open('images/log-in-bg.png')
user_bg_img = user_bg_img.resize((window_width,window_heigth))
user_bg_img = ImageTk.PhotoImage(user_bg_img)

#sign_in_canvas.create_image(250, 250, image=bg_img)

user_frame.create_image(227,300,image=user_bg_img)
####################################

bottom_bar_img = Image.open('images/bottom-bar.png')
bottom_bar_img = bottom_bar_img.resize((window_width,40))
bottom_bar_img = ImageTk.PhotoImage(bottom_bar_img)

user_frame.create_image(227,window_heigth-20,image=bottom_bar_img)

####################################

menu_button_c = bottom_can_bar.create_image(window_width-35,18,image=menu_logo)
bottom_can_bar.tag_bind(menu_button_c,"<Enter>",line_move_to_menu)
bottom_can_bar.tag_bind(menu_button_c,"<Button>",menu)

prof_button_c = bottom_can_bar.create_image(window_width-125,18,image=user_logo)
bottom_can_bar.tag_bind(prof_button_c,"<Enter>",line_move_to_prof)
bottom_can_bar.tag_bind(prof_button_c,"<Button>",profile)

cart_button_c = bottom_can_bar.create_image(window_width-225,18,image=product_logo)
bottom_can_bar.tag_bind(cart_button_c,"<Enter>",line_move_to_cart)
bottom_can_bar.tag_bind(cart_button_c,"<Button>",cart)

search_button_c = bottom_can_bar.create_image(window_width-325,18,image=search_logo)
bottom_can_bar.tag_bind(search_button_c,"<Enter>",line_move_to_search)

home_button_c = bottom_can_bar.create_image(window_width-415,18,image=home_logo)
bottom_can_bar.tag_bind(home_button_c,"<Enter>",line_move_to_home)
bottom_can_bar.tag_bind(home_button_c,"<Button>",show_products)

line = Label(bottom_can_bar,image=line_logo,bg="black",highlightcolor="black",highlightbackground="black",highlightthickness=0)

####################################

############


#
########################## buy frame

buy_frame = Canvas(user_frame)
label = Label(buy_frame, text='BUY')
label.pack(side=TOP)

product_picture = Label(buy_frame)
product_picture.pack(side=TOP)

amount = Label(buy_frame)
amount.pack(side=LEFT)

new_quan = StringVar()
quan_menu = Spinbox(buy_frame)
quan_menu.pack(side=RIGHT)

buy_button = Button(buy_frame)
buy_button.pack(side=BOTTOM)

########################## MENU WINDOW FRAME

menu_frame = Canvas(user_frame, bg='black')
bg_menu = Label(menu_frame, image=bg_img)
bg_menu.pack(expand=True, fill=BOTH)

menu = Frame(bg_menu, width=200)
menu.pack(side='right', fill=Y)

log_out = Label(menu, text="Log out")
log_out.pack()
log_out.bind('<Button>', user_log_out)

########################## ADD PRODUCT WINDOW FRAME

sell_frame = Canvas(user_frame, bg='yellow')

upload_image = Button(sell_frame, command=lambda: upload_image_function(), text="Product image")
upload_image.pack()

upload_name_of_product = Entry(sell_frame)
upload_name_of_product.pack()

upload_price = Entry(sell_frame
                     )
upload_price.pack()

upload_stock = Entry(sell_frame)
upload_stock.pack()

upload_contact = Entry(sell_frame)
upload_contact.pack()

upload_product = Button(sell_frame,
                        command=lambda: save_product(product_img, upload_name_of_product.get(), upload_price.get(),
                                                     upload_stock.get(), upload_contact.get()), text="Uplaod")
upload_product.pack()
########################## CART WINDOW FRAME

cart_frame_bg = Image.open('images/bg_ulit.jpg')
cart_frame_bg = cart_frame_bg.resize((470,610))
cart_frame_bg = ImageTk.PhotoImage(cart_frame_bg)

cart_frame = Canvas(user_frame)
cart_frame.create_image(220,256 , image = cart_frame_bg)

########################## PROFILE WINDOW FRAME

profile_frame = Canvas(user_frame,
                      bg=bgcolor,

                      )

prof_background_img = Image.open('images/profbg.jpg')
prof_background_img = prof_background_img.resize((470,610))
prof_background_img = ImageTk.PhotoImage(prof_background_img)

profile_frame.create_image(220,256,image=prof_background_img)
#bg_prof = Label(profile_frame, image=bg_2)
#bg_prof.pack()

profile_outine = Frame(profile_frame,
                       highlightcolor='black',
                       highlightthickness=1,
                       highlightbackground='black',
                       pady=50,
                       padx=100,
                       bg=bgcolor
                       )
profile_outine.place(x=60, y=20)
profile_pic = Label(profile_outine,
                    highlightcolor='black',
                    highlightthickness=1,
                    highlightbackground='black',
                    borderwidth=2
                    )
profile_pic.pack()

seperator = Label(profile_outine, text="______________________________", bg=bgcolor)
seperator.pack()

profile_name_L = Label(profile_outine,
                       text='NAME',
                       font=(tk_font, 8, 'bold'),
                       bg=bgcolor)
profile_NAME = Label(profile_outine,
                     bg=bgcolor,
                     font=(tk_font, 18, 'bold')
                     )
profile_name_L.pack()
profile_NAME.pack()

profile_age_L = Label(profile_outine,
                      text='AGE',
                      font=(tk_font, 8, 'bold'),
                      bg=bgcolor)
profile_AGE = Label(profile_outine,
                    bg=bgcolor,
                    font=(tk_font, 18, 'bold')
                    )
profile_age_L.pack()
profile_AGE.pack()

profile_address_L = Label(profile_outine,
                          text='ADDRESS',
                          font=(tk_font, 8, 'bold'),
                          bg=bgcolor)
profile_ADDRES = Label(profile_outine,
                       bg=bgcolor,
                       font=(tk_font, 18, 'bold')
                       )
profile_address_L.pack()
profile_ADDRES.pack()

########################## PRODUCTS WINDOW FRAME
product_frame_bg = Image.open('images/bgnanaman.jpg')
product_frame_bg = product_frame_bg.resize((470,610))
product_frame_bg = ImageTk.PhotoImage(product_frame_bg)

product_frame = Canvas(user_frame, scrollregion=(0, 0, 400, 400))
# Bind mouse wheel event to the canvas
#product_frame.bind("<MouseWheel>", on_mouse_wheel)

#product_frame.create_image(220,256 , image = product_frame_bg)
background_of_prod_frame = Label(product_frame,image=product_frame_bg)


product_frame.bind("<Configure>", lambda e: product_frame.configure(scrollregion=product_frame.bbox("all")))
product_frame.bind("<MouseWheel>", on_mousewheel)

########################## USER PRODUCTS WINDOW FRAME

user_products_frame = Canvas(user_frame, bg='orange')
########################## USER transaction WINDOW FRAME
user_transaction_frame_bg = Image.open('images/bg_ulit.jpg')
user_transaction_frame_bg = user_transaction_frame_bg.resize((470,610))
user_transaction_frame_bg = ImageTk.PhotoImage(user_transaction_frame_bg)

user_transaction_frame = Canvas(user_frame)
user_transaction_frame.create_image(220,256 , image = user_transaction_frame_bg)

user_transaction_frame = Canvas(user_frame)

########################## SIGN UP WINDOW FRAME

sign_in_canvas = Canvas(window,bg=bgcolor)
#########


sign_txt_bx = Image.open('images/txt-box.png')
sign_txt_bx = sign_txt_bx.resize((300, 70))
sign_txt_bx = ImageTk.PhotoImage(sign_txt_bx)

sign_img_bx = Image.open('images/txt-box.png')
sign_img_bx = sign_img_bx.resize((100, 50))
sign_img_bx = ImageTk.PhotoImage(sign_img_bx)


back_to_img = Image.open('images/back-arrow.png')
back_to_img = back_to_img.resize((30, 30))
back_to_img = ImageTk.PhotoImage(back_to_img)

sign_to_img = Image.open('images/sign-in.png')
sign_to_img = sign_to_img.resize((160, 80))
sign_to_img = ImageTk.PhotoImage(sign_to_img)


sign_bg_img = Image.open('images/new-.jpg')
sign_bg_img = sign_bg_img.resize((window_width,window_heigth))
sign_bg_img = ImageTk.PhotoImage(sign_bg_img)


sign_out_img = Image.open('images/sign-out.png')
sign_out_img = sign_out_img.resize((725, 616))
sign_out_img = ImageTk.PhotoImage(sign_out_img)

#sign_in_canvas.create_image(250, 250, image=bg_img)

sign_in_canvas.create_image(227,300,image=sign_bg_img)

back_to_log = sign_in_canvas.create_image(20,20,image=back_to_img)
sign_in_canvas.tag_bind(back_to_log,"<Button>",lambda event:back_to_log_com())
########


########

#outline = sign_in_canvas.create_image(230,300,image=sign_out_img)
#############

######## create logo in log in box
sign_in_canvas.create_image(220,90,image=logo_med)

######## create log in text
sign_in_canvas.create_text(220,155,text="Sign up",font=("Segoe UI Black",24,"bold"))

######## create username label
sign_in_canvas.create_text(120,210,text="Name",font=("Calibre",8,"bold"))
######## create username label
sign_in_canvas.create_text(130,260,text="Address",font=("Calibre",8,"bold"))
######## create username label
sign_in_canvas.create_text(130,310,text="Username",font=("Calibre",8,"bold"))
######## create username label
sign_in_canvas.create_text(130,360,text="Password",font=("Calibre",8,"bold"))
######## create username label
sign_in_canvas.create_text(155,410,text="Confirm Password",font=("Calibre",8,"bold"))

#############

name_txt_box = sign_in_canvas.create_image(220,220,image=sign_txt_bx)

address_txt_box = sign_in_canvas.create_image(220,270,image=sign_txt_bx)

username_txt_box = sign_in_canvas.create_image(220,320,image=sign_txt_bx)

password_txt_box = sign_in_canvas.create_image(220,370,image=sign_txt_bx)

confirm_txt_box = sign_in_canvas.create_image(220,420,image=sign_txt_bx)

img_box = sign_in_canvas.create_image(220,460,image=sign_img_bx)
sign_in_canvas.tag_bind(img_box,"<Button>",lambda event: open_id_image())
############
# logo
#sign_in_canvas.create_image(220,50,image=logo_med)

# sign label
#sign_in_canvas.create_text(220,90,text="Sign in",font=(tk_font,20,"bold"))

# insert user profile

insert_id = Button(sign_in_canvas, text="Upload id",
                   bg='red',
                   font=(tk_font, 8),
                   command=lambda: open_id_image())
#insert_id.place(x=80,y=150)




######## create name entry
sign_user_name = Entry(sign_in_canvas,
                        width=33,
                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0)
######## display the name entry
sign_user_name.place(x=111,y=227)

######## bind the username entry,this binding appear the line inside of entry box if the cursor enter
#sign_user_name_label.bind("<Enter>",lambda event:enter_txt_U())

######## create line inside of entry box
usr_name_line_S = sign_in_canvas.create_line(111,246,340,246,fill="black",width=1)

######## bind the username entry,this binding appear the line inside of entry box if the cursor enter
#sign_user_name_label.bind("<Enter>",lambda event:enter_txt_U())

#create sign address entry
sign_user_address = Entry(sign_in_canvas,
                        width=33,
                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0)
sign_user_address.place(x=111,y=276)

######## create line inside of entry box
address_line_S = sign_in_canvas.create_line(111,295,340,295,fill="black",width=1)

######## create sign user username entry
sign_in_username = Entry(sign_in_canvas,
                        width=33,
                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0)
sign_in_username.place(x=111,y=327)

######## create line inside of entry box
username_line_S = sign_in_canvas.create_line(111,346,340,346,fill="black",width=1)

####### create sign user password entry
sign_in_password = Entry(sign_in_canvas,
                        width=33,
                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0)
sign_in_password.place(x=111,y=376)

######## create line inside of entry box
pass_line_S = sign_in_canvas.create_line(111,395,340,395,fill="black",width=1)

# confirm pass word label / input

# sign confirm password entry
confirm_pass = Entry(sign_in_canvas,
                        width=33,
                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0,
                        show="*")
confirm_pass.place(x=111,y=427)

######## create line inside of entry box
confirm_line_S = sign_in_canvas.create_line(111,446,340,446,fill="black",width=1)


# create sign in button
sign_in_button = sign_in_canvas.create_image(230,530,image=sign_to_img)
sign_in_canvas.tag_bind(sign_in_button,"<Button>",lambda event: save_account(id_picture, sign_user_name.get(),sign_user_address.get(),
sign_in_username.get(), sign_in_password.get()))

#try:    # sign_buttton = Button(outline,
#bg=text_color,image=sign_to_img,
#command=lambda: save_account(id_picture, sign_user_name.get(), age.get(), sign_user_address.get(),
#sign_in_username.get(), sign_in_password.get()),
         #                 font=(tk_font, 10),
         #                 width=10)
#    sign_buttton.pack()
#except Exception as e:
 #   messagebox.showerror("Sign in error", "May kulang !\n Ayusin mo")




########################## LOG IN  PRODUCT WINDOW FRAME
#create window for log in
log_in_canvas = Canvas(window)
#########

crt_acc_btn = Image.open('images/crt_acc.png')
crt_acc_btn = crt_acc_btn.resize((230, 60))
crt_acc_btn = ImageTk.PhotoImage(crt_acc_btn)

log_outl = Image.open('images/log_out.png')
log_outl = log_outl.resize((430, 460))
log_outl = ImageTk.PhotoImage(log_outl)


txt_bx = Image.open('images/txt-box.png')
txt_bx = txt_bx.resize((300, 70))
txt_bx = ImageTk.PhotoImage(txt_bx)


log_btn = Image.open('images/log-in.png')
log_btn = log_btn.resize((170, 70))
log_btn = ImageTk.PhotoImage(log_btn)


log_in_b = Image.open('images/log in.png')
log_in_b = log_in_b.resize((60, 20))
log_in_b = ImageTk.PhotoImage(log_in_b)

sign_in_b = Image.open('images/signin.png')
sign_in_b = sign_in_b.resize((60, 20))
sign_in_b = ImageTk.PhotoImage(sign_in_b)


moon_img = Image.open('images/switch (1).png')
moon_img = moon_img.resize((40, 40))
moon_img = ImageTk.PhotoImage(moon_img)


sun_img = Image.open('images/switch.png')
sun_img = sun_img.resize((40, 40))
sun_img = ImageTk.PhotoImage(sun_img)


log_bg_img = Image.open('images/new-.jpg')
log_bg_img = log_bg_img.resize((window_width, window_heigth))
log_bg_img = ImageTk.PhotoImage(log_bg_img)

show_pass_img = Image.open('images/eye2.png')
show_pass_img = show_pass_img.resize((20, 15))
show_pass_img = ImageTk.PhotoImage(show_pass_img)


hide_pass_img = Image.open('images/eye2.png')
hide_pass_img = hide_pass_img.resize((20, 15))
hide_pass_img = ImageTk.PhotoImage(hide_pass_img)

######## background
log_in_canvas.create_image(223, 300, image=log_bg_img)
###########
######## password show config
pass_btn_config = log_in_canvas.create_image(370, 325, image=show_pass_img)
log_in_canvas.tag_bind(pass_btn_config,"<Button>",lambda event: show_password())


switch= log_in_canvas.create_image(25,25,image=sun_img)

log_in_canvas.tag_bind(switch,"<Button>",lambda event: change_bg_color())

######## log in box background
#log_in_canvas.create_image(227,300,image=log_outl)

######## create logo in log in box
log_in_canvas.create_image(220,120,image=logo_med)

######## create log in text
log_in_canvas.create_text(220,185,text="Log in",font=("Segoe UI Black",24,"bold"))

######## create entry box
txt_boxU = log_in_canvas.create_image(220,260,image=txt_bx)
txt_boxP = log_in_canvas.create_image(220,310,image=txt_bx)

######## create username label
username_txt = log_in_canvas.create_text(130,250,text="Username",font=("Calibre",8,"bold"))

######## create password label
password_txt = log_in_canvas.create_text(130,300,text="Password",font=("Calibre",8,"bold"))

######## create button for log in
btn_log_in = log_in_canvas.create_image(225,390,image=log_btn)
log_in_canvas.tag_bind(btn_log_in,"<Button>",lambda event:log_in_validation())

######## create button for create account
log_in_canvas.create_text(225,430,text="Don't have an account?")
btn_crt_acc = log_in_canvas.create_image(233,470,image=crt_acc_btn)
log_in_canvas.tag_bind(btn_crt_acc,"<Button>",lambda event:show_sign_in_frame())

############
######## create username entry
log_in_username = Entry(log_in_canvas,
                        width=33,

                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0)
######## display the username entry
log_in_username.place(x=111,y=267)
######## create show and hide password button
######## bind the username entry,this binding appear the line inside of entry box if the cursor enter
log_in_username.bind("<Enter>",lambda event:enter_txt_U())

######## create line inside of entry box
usr_name_line = log_in_canvas.create_line(111,286,340,286,fill="#F3F2ED",width=1)

######### create password entry
log_in_password = Entry(log_in_canvas,
                        width=33,
                        show="*",
                        bg="#F3F2ED",
                        font=(tk_font, 10),
                        bd=0)

######## display the password entry
log_in_password.place(x=111,y=315)

######## create line inside of entry box
usr_p_line = log_in_canvas.create_line(111,336,340,336,fill="#F3F2ED",width=1)

######## bind the password entry,this binding appear the line inside of entry box if the cursor enter
log_in_password.bind("<Enter>",lambda event:enter_txt_P())



########################## WELCOCME HOME WINDOW FRAME

con = Image.open('images/icons8-log-in-50.png')
con = ImageTk.PhotoImage(con)

logo_spar = Image.open('images/logo_spar.png')
logo_spar = logo_spar.resize((400, 380))
logo_spar = ImageTk.PhotoImage(logo_spar)

get_start_img = Image.open('images/getstartedbtn.png')
get_start_img = get_start_img.resize((120, 60))
get_start_img = ImageTk.PhotoImage(get_start_img)


wel_bg = Image.open('images/new-.jpg')
wel_bg = wel_bg.resize((700, 700))
wel_bg = ImageTk.PhotoImage(wel_bg)

myLogo = Image.open('images/sa.png')
myLogo = myLogo.resize((170, 170))
myLogo = ImageTk.PhotoImage(myLogo)

spar_logo = Image.open('images/spartan.png')
spar_logo = spar_logo.resize((80, 80))
spar_logo = ImageTk.PhotoImage(spar_logo)
#########

home_canvas = Canvas(window, bg=bgcolor)

home_canvas.create_image(110, 250, image=wel_bg)
home_canvas.create_image(230, 220, image=myLogo)
#home_canvas.create_image(220,100,image=spar_logo)

tagline = f"           A  BatState-U shop that\nleads innovation and transform lives"
bsu_tagline = home_canvas.create_text(230,330,text="",font=("Bahnschrift Light Condensed",17),fill="black")
write_text(1)
home_canvas.create_image(30, 30,
                         image=logo_small)
#home_canvas.create_image(230, 120, image=logo_spar)
#########
#home_con_button = Button(home_canvas,
                      #   image=con,
                       #  font=(tk_font, 13, "bold"),
                       #  bg='red',
                       #  command=show_log_in_frame, relief=GROOVE)
#home_con_button.place(x=220, y=515)
get_started_button = home_canvas.create_image(225,495,image=get_start_img)

home_canvas.tag_bind(get_started_button,"<Button>",lambda event: show_log_in_frame())
################################################################

if __name__ == '__main__':
    s = ttk.Style()
    s.theme_use('clam')
    restore_db_to_list()
    welcome()

window.mainloop()
