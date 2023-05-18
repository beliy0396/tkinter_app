import ttkbootstrap as ttk
import sqlite3
import pandas as pd
from tkinter import *

class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = ttk.Frame(root, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)


        self.catalog_img = ttk.PhotoImage(file='img/catalog.png')
        btn_goods_or_services = ttk.Menubutton(toolbar, text='Категория',
                                     bootstyle="dark menubutton",
                                     image=self.catalog_img)
        btn_goods_or_services.grid()
        btn_goods_or_services.menu = Menu(btn_goods_or_services, tearoff=0)
        btn_goods_or_services["menu"] = btn_goods_or_services.menu

        goods = IntVar()
        services = IntVar()

        btn_goods_or_services.menu.add_checkbutton(label="Товары",
                                                   variable=goods,
                                                   command=self.open_goods_catalog)
        btn_goods_or_services.menu.add_checkbutton(label="Услуги",
                                                   variable=services,
                                                   command=self.open_services_catalog)
        btn_goods_or_services.pack(side=ttk.LEFT, padx=35, pady=5)

        self.new_img = ttk.PhotoImage(file='img/new.png')
        btn_add_record = ttk.Button(toolbar, text='Добавить запись',
                                               bootstyle="dark",
                                               image=self.new_img,
                                               command=self.open_add_record)
        btn_add_record.pack(side=ttk.LEFT, padx=35, pady=5)


    def open_goods_catalog(self):
        GoodsCatalog()

    def open_services_catalog(self):
        ServicesCatalog()

    def open_add_record(self):
        AddRecord()

class AddRecord(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add_record()
        self.db = db

    def init_add_record(self):
        self.title('Добавление новой записи')
        self.geometry('1320x820')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        combobox_values_type = ['Товар', 'Услуга']

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.Y)

        self.button_add = ttk.Button(toolbar, text='Добавить', command=self.get_data, bootstyle="dark")
        self.button_add.pack(pady=15)

        label_type = ttk.Label(toolbar, text='Тип')
        label_type.pack(side=ttk.LEFT, padx=10, pady=5)

        self.combobox_type = ttk.Combobox(toolbar, values=combobox_values_type, bootstyle="dark")
        self.combobox_type.pack(side=ttk.LEFT, padx=15, pady=5)

        label_articul = ttk.Label(toolbar, text='Артикул')
        label_articul.pack(side=ttk.LEFT, padx=10, pady=5)

        self.entry_articul = ttk.Entry(toolbar, bootstyle="success")
        self.entry_articul.pack(side=ttk.LEFT, padx=15, pady=5)

        label_title = ttk.Label(toolbar, text='Название')
        label_title.pack(side=ttk.LEFT, padx=10, pady=5)

        self.entry_title = ttk.Entry(toolbar, bootstyle="success")
        self.entry_title.pack(side=ttk.LEFT, padx=15, pady=5)

        label_description = ttk.Label(toolbar, text='Описание')
        label_description.pack(side=ttk.LEFT, padx=10, pady=5)

        self.entry_description = ttk.Entry(toolbar, bootstyle="success")
        self.entry_description.pack(side=ttk.LEFT, padx=15, pady=5)
        combobox_values_category = []
        self.combobox_type.bind("<<ComboboxSelected>>", self.change_combobox_category)

        label_category = ttk.Label(toolbar, text='Категория')
        label_category.pack(side=ttk.LEFT, padx=10, pady=5)

        self.combobox_category = ttk.Combobox(toolbar, values=combobox_values_category, bootstyle="dark")
        self.combobox_category.pack(side=ttk.LEFT, padx=15, pady=5)

        label_price = ttk.Label(toolbar, text='Цена')
        label_price.pack(side=ttk.LEFT, padx=10, pady=5)

        self.entry_price = ttk.Entry(toolbar, bootstyle="success")
        self.entry_price.pack(side=ttk.LEFT, pady=5)

    def change_combobox_category(self, *args):
        if self.combobox_type.get() == 'Товар':
            combobox_values_category = ['Смартфоны', 'Ноутбуки', 'Наушники']
        else:
            combobox_values_category = ['Комплект приложений', 'Наклейка стекла на смартфон', 'Создание учётной записи']
        self.combobox_category.config(values=combobox_values_category)

    def get_data(self):
        if self.combobox_type.get() == 'Товар':
            table = 'goods'
        else:
            table = 'services'
        articul = self.entry_articul.get()
        title = self.entry_title.get()
        description = self.entry_description.get()
        category = self.combobox_category.get()
        price = self.entry_price.get()
        self.db.insert_record(table, articul, title, description, category, price)

class GoodsCatalog(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_goods_catalog()
        self.db = db
        self.view_goods_table()

    def init_goods_catalog(self):
        self.title('Каталог товаров')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        label_filter = ttk.Label(toolbar, text='Фильтр:')
        label_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        combobox_values = ['Смартфоны', 'Ноутбуки', 'Наушники']
        self.combobox_filter = ttk.Combobox(toolbar, values=combobox_values, bootstyle="dark")
        self.combobox_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_filter = ttk.Button(toolbar, text='Поиск по фильтру', command=self.view_goods_filter, bootstyle="dark")
        button_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_drop_filter = ttk.Button(toolbar, text='Сбросить фильтр', command=self.view_goods_table, bootstyle="dark")
        button_drop_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_to_excel = ttk.Button(toolbar, text='Выгрузить в Excel', command=self.data_to_excel, bootstyle="dark")
        button_to_excel.pack(side=ttk.LEFT, padx=35, pady=5)

        self.tree = ttk.Treeview(self, columns=('id', 'articul', 'title', 'description', 'category', 'price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('articul', width=150, anchor=ttk.CENTER)
        self.tree.column('title', width=250, anchor=ttk.CENTER)
        self.tree.column('description', width=300, anchor=ttk.CENTER)
        self.tree.column('category', width=100, anchor=ttk.CENTER)
        self.tree.column('price', width=200, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('articul', text='Артикул')
        self.tree.heading('title', text='Название')
        self.tree.heading('description', text='Описание')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')
        self.tree.pack()


    def data_to_excel(self):
        row_list = []
        columns = ('id', 'articul', 'title', 'description', 'category', 'price')
        for row in self.tree.get_children():
            row_list.append(self.tree.item(row)["values"])
        df_tree = pd.DataFrame(row_list, columns=columns)
        df_tree.to_excel('data.xlsx')

    def view_goods_table(self):
        self.db.cur.execute(
            '''SELECT * FROM goods'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_goods_filter(self, *args):
        value = self.combobox_filter.get()
        self.db.cur.execute(
            f'''SELECT * FROM goods WHERE category = "{value}"'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]



class ServicesCatalog(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_services_catalog()
        self.db = db
        self.view_services_table()


    def init_services_catalog(self):
        self.title('Каталог услуг')
        self.geometry('1000x400+400+300')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        combobox_values = ['Комплект приложений', 'Наклейка стекла на смартфон', 'Создание учётной записи']
        self.combobox_filter = ttk.Combobox(toolbar, values=combobox_values)
        self.combobox_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_filter = ttk.Button(toolbar, text='Поиск по фильтру', command=self.view_services_filter, bootstyle="dark")
        button_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_drop_filter = ttk.Button(toolbar, text='Сбросить фильтр', command=self.view_services_table, bootstyle="dark")
        button_drop_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_to_excel = ttk.Button(toolbar, text='Выгрузить в Excel', command=self.data_to_excel, bootstyle="dark")
        button_to_excel.pack(side=ttk.LEFT, padx=35, pady=5)

        self.tree = ttk.Treeview(self, columns=('id', 'articul', 'title', 'description', 'category', 'price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('articul', width=150, anchor=ttk.CENTER)
        self.tree.column('title', width=250, anchor=ttk.CENTER)
        self.tree.column('description', width=300, anchor=ttk.CENTER)
        self.tree.column('category', width=100, anchor=ttk.CENTER)
        self.tree.column('price', width=200, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('articul', text='Артикул')
        self.tree.heading('title', text='Название')
        self.tree.heading('description', text='Описание')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')
        self.tree.pack()

    def data_to_excel(self):
        row_list = []
        columns = ('id', 'articul', 'title', 'description', 'category', 'price')
        for row in self.tree.get_children():
            row_list.append(self.tree.item(row)["values"])
        df_tree = pd.DataFrame(row_list, columns=columns)
        df_tree.to_excel('data.xlsx')

    def view_services_table(self):
        self.db.cur.execute(
            '''SELECT * FROM services'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_services_filter(self, *args):
        value = self.combobox_filter.get()
        self.db.cur.execute(
            f'''SELECT * FROM services WHERE category = "{value}"'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db/db.db')
        self.cur = self.conn.cursor()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS goods(id integer primary key, articul text, title text, description text, category text, price text)'''
        )
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS services(id integer primary key, articul text, title text, description text, category text, price text)'''
        )
        self.conn.commit()

    def insert_record(self, table, articul, title, description, category, price):
        self.cur.execute(
            f'''INSERT INTO {table}(articul, title, description, category, price) VALUES('{articul}', '{title}', '{description}', '{category}', '{price}')'''
        )
        self.conn.commit()


if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    db = DB()
    app = Main(root)
    app.pack()
    root.title('OOO')
    root.iconbitmap('')
    root.geometry('350x500')
    root.resizable(False, False)
    root.mainloop()