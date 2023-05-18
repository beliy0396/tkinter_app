import ttkbootstrap as ttk
from tkinter import *
import sqlite3

class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = ttk.Frame(root, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)


        self.catalog_img = ttk.PhotoImage(file='img/img.png')
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




    def open_goods_catalog(self):
        GoodsCatalog()

    def open_services_catalog(self):
        ServicesCatalog()


class GoodsCatalog(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_goods_catalog()
        self.db = db
        self.view_goods_table()

    def init_goods_catalog(self):
        self.title('Каталог товаров')
        self.geometry('1220x820')
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

        button_filter = ttk.Button(toolbar, text='Поиск по фильтру', command=self.get_combobox, bootstyle="dark")
        button_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_drop_filter = ttk.Button(toolbar, text='Сбросить фильтр', command=self.view_goods_table, bootstyle="dark")
        button_drop_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        self.tree = ttk.Treeview(self, columns=('id', 'articul', 'title', 'description', 'category', 'price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=150, anchor=ttk.CENTER)
        self.tree.column('articul', width=150, anchor=ttk.CENTER)
        self.tree.column('title', width=250, anchor=ttk.CENTER)
        self.tree.column('description', width=250, anchor=ttk.CENTER)
        self.tree.column('category', width=250, anchor=ttk.CENTER)
        self.tree.column('price', width=150, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('articul', text='Артикул')
        self.tree.heading('title', text='Название')
        self.tree.heading('description', text='Описание')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')
        self.tree.pack()


    def get_combobox(self):
        value = self.combobox_filter.get()
        self.view_goods_filter(value)

    def view_goods_table(self):
        self.db.cur.execute(
            '''SELECT * FROM goods'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_goods_filter(self, value):
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
        self.geometry('1220x820+400+300')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        combobox_values = ['Комплект приложений', 'Наклейка стекла на смартфон', 'Создание учётной записи']
        self.combobox_filter = ttk.Combobox(self, values=combobox_values)
        self.combobox_filter.pack(pady=10)

        button_filter = ttk.Button(self, text='Поиск по фильтру', command=self.get_combobox)
        button_filter.pack(pady=10)

        button_drop_filter = ttk.Button(self, text='Сбросить фильтр', command=self.view_services_table())
        button_drop_filter.pack(pady=10)


        self.tree = ttk.Treeview(self, columns=('id', 'articul', 'title', 'description', 'category', 'price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=150, anchor=ttk.CENTER)
        self.tree.column('articul', width=150, anchor=ttk.CENTER)
        self.tree.column('title', width=250, anchor=ttk.CENTER)
        self.tree.column('description', width=250, anchor=ttk.CENTER)
        self.tree.column('category', width=250, anchor=ttk.CENTER)
        self.tree.column('price', width=150, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('articul', text='Артикул')
        self.tree.heading('title', text='Название')
        self.tree.heading('description', text='Описание')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')
        self.tree.pack()

    def get_combobox(self):
        value = self.combobox_filter.get()
        self.view_services_filter(value)

    def view_services_table(self):
        self.db.cur.execute(
            '''SELECT * FROM services'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_services_filter(self, value):
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

if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    db = DB()
    app = Main(root)
    app.pack()
    root.title('OOO')
    root.iconbitmap('')
    root.geometry('920x220')
    root.resizable(True, True)
    root.mainloop()
