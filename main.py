from kivy.config import Config
Config.set('graphics', "width", 450)
Config.set('graphics', "height", 600)
Config.write()

from kivy.app import App
from kivymd.app import MDApp
from kivy.lang.builder import Builder
import sqlite3
import datetime
from datetime import date

#импорт классов для layout
from kivy.uix.boxlayout import BoxLayout
#импорт классов для виджетов
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield.textfield import MDTextField
from kivy.properties import ObjectProperty # создает ссылку на объект python
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import pandas as pd


#Доп классы для создания определенных виджетов
class Calendar(Screen): #календарь
    pass            
class NewEvent(Screen): #новое событие
    pass
class Cows(Screen): #коровы
    pass
class NewCows(Screen): #новые коровы
    pass
class Page_of_cow(Screen):
    pass
class EditCows(Screen): #изменение характеристик коровы
    pass
class MilkYield_main(Screen): #удои
    pass
class MilkYield_by_cows(Screen): 
    pass
class WindowManager(ScreenManager):
    pass


#Создание основного класса приложения
class MainApp(MDApp):
    def on_save1(self, instance, value, date_range):
        self.root.get_screen('calendar').ids.dateintext1.text="с "+str(date_range[0])+" по "+str(date_range[-1])
        print (date_range[0], "   ", date_range[-1])
        sqlite_select_query = f"""SELECT * FROM event ORDER BY date_of_event DESC ;""" #WHERE {date_range[0]} <= date_of_event <= {date_range[-1]} 
        cur.execute(sqlite_select_query)
        row_data_for_table1 = cur.fetchall()
        print(row_data_for_table1)
        row_data_for_table2=[]
        for row in row_data_for_table1:
            if str(row[0])>=str(date_range[0]) and str(row[0])<=str(date_range[-1]):
                print(row[0],"подходит")
                row_data_for_table2.append(row)
        print(row_data_for_table2)
        self.data_tables.row_data=row_data_for_table2

    def on_cancel1(self, instance, value):
        pass   
    def show_date_picker_for_calendar(self): #выбор даты в окне "Календарь"
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save1, on_cancel=self.on_cancel1)
        date_dialog.open()
        
#процедуры создания нового события
    def on_save2(self, instance, value, date_range):
        self.root.get_screen("newevent").ids.dateintext2.text=str(value)
        global date_save
        date_save=value
    def on_cancel2(self, instance, value):
        pass      
    
    def show_date_picker_for_newevent(self):     #выбор даты в окне "Создание нового событие"
        date_dialog2 = MDDatePicker()
        date_dialog2.bind(on_save=self.on_save2, on_cancel=self.on_cancel2)
        date_dialog2.open()
    def save_event_def(self): #Сохранение нового события в БД
        dt=date_save
        cname=chosen_cowname
        desc=self.root.get_screen("newevent").ids.description.text
        query="INSERT INTO event VALUES(?, ?, ?);"
        cur.execute(query, (dt,cname,desc))
        bd.commit()
        #обновляем таблицу
        sqlite_select_query = f"""SELECT * FROM event ORDER BY date_of_event DESC ;""" #WHERE {date_range[0]} <= date_of_event <= {date_range[-1]} 
        cur.execute(sqlite_select_query)
        row_data_for_table = cur.fetchall()
        self.data_tables.row_data=row_data_for_table
        self.root.get_screen('calendar').ids.dateintext1.text="Весь период"
        self.root.current = 'calendar'
    
     #процедуры добавления новой коровы   
    def on_save_for_newcow1(self, instance, value, date_range):
        self.root.get_screen("newcows").ids.dateintext3.text=str(value)
        self.root.get_screen("editcows").ids.dateintext32.text=str(value)
        
    def on_cancel_for_newcow1(self, instance, value):
        pass      
    def show_date_picker_for_newcow1 (self):     #выбор даты в окне "Создание нового событие"
        date_dialog2 = MDDatePicker()
        date_dialog2.bind(on_save=self.on_save_for_newcow1, on_cancel=self.on_cancel_for_newcow1)
        date_dialog2.open()
    
    def on_save_for_newcow2(self, instance, value, date_range):
        self.root.get_screen("newcows").ids.dateintext4.text=str(value)
        self.root.get_screen("editcows").ids.dateintext42.text=str(value)
    def on_cancel_for_newcow2(self, instance, value):
        pass      
    def show_date_picker_for_newcow2 (self):     #выбор даты в окне "Создание нового событие"
        date_dialog2 = MDDatePicker()
        date_dialog2.bind(on_save=self.on_save_for_newcow2, on_cancel=self.on_cancel_for_newcow2)
        date_dialog2.open()
    
    def on_save_for_newcow3(self, instance, value, date_range):
        self.root.get_screen("newcows").ids.dateintext5.text=str(value)
        self.root.get_screen("newcows").ids.dateintext6.text=str(value+datetime.timedelta(days=3))
        self.root.get_screen("editcows").ids.dateintext52.text=str(value)
        self.root.get_screen("editcows").ids.dateintext62.text=str(value+datetime.timedelta(days=3))
    def on_cancel_for_newcow3(self, instance, value):
        pass      
    def show_date_picker_for_newcow3 (self):     #выбор даты в окне "Создание нового событие"
        date_dialog2 = MDDatePicker()
        date_dialog2.bind(on_save=self.on_save_for_newcow3, on_cancel=self.on_cancel_for_newcow3)
        date_dialog2.open()
    
    
    
    def save_cow_def(self): #Сохранение новой коровы
        cowname=self.root.get_screen("newcows").ids.cowname.text
        status=self.root.get_screen("newcows").ids.status.text
        d1=self.root.get_screen("newcows").ids.dateintext3.text
        d2=self.root.get_screen("newcows").ids.dateintext4.text
        d3=self.root.get_screen("newcows").ids.dateintext5.text
        d4=self.root.get_screen("newcows").ids.dateintext6.text
        query="INSERT INTO cows VALUES(?, ?, ?,?,?,?);"
        cur.execute(query, (cowname,status,d1,d2,d3,d4))
        bd.commit()
        #обновляем таблицу
        sqlite_select_query3 = """SELECT cowname,status FROM cows;""" 
        cur.execute(sqlite_select_query3)
        row_data_for_listofcow = cur.fetchall()
        self.listofcow.row_data=row_data_for_listofcow
        self.root.current = 'cows'


        #Вывод всей таблицы event в терминал, включая добавленную строку
        sqlite_select_query = """SELECT * from event"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        print("Всего строк:  ", len(records))
        print("Вывод каждой строки")
        for row in records:
            print (row)
        
    def dropdown(self):
        #выборка кличек из БД
        sqlite_select_query = """SELECT cowname from cows"""
        cur.execute(sqlite_select_query)
        items = cur.fetchall()
        self.cownames_list=[
            {"viewclass":"OneLineListItem", 
            "text":str(i)[2:-3],
            "on_release": lambda x=i : self.set_item(x)} for i in items]
        self.data_cownames = MDDropdownMenu(
            caller = self.root.get_screen('newevent').ids.cownames_DropdownMenu, 
            items = self.cownames_list,
            width_mult= 5)
        self.data_cownames.open()
    def set_item(self,text_item):
        self.root.get_screen('newevent').ids.choosingname.text=str(text_item)[2:-3]
        global chosen_cowname
        chosen_cowname = str(text_item)[2:-3]
        self.data_cownames.dismiss()

    #таблица характеристик коровы для окна pageofcow
    def show_cow_characteristic(self,cname):
        self.root.current = "pageofcow"
        sqlite_select_query = """SELECT * FROM cows WHERE cowname = ?;""" 
        cur.execute(sqlite_select_query,[cname])
        one_row_data= cur.fetchall()[0]
        list_of_characteristic=["имя коровы","статус","дата рождения","дата последнего отёла","дата осеменения коровы","предполагаемая дата отела"]
        row_data_for_cows_data=[]
        for i in range(6):
            row=[list_of_characteristic[i],one_row_data[i]]
            row_data_for_cows_data.append(row)
        self.data_CowCharacteristic.row_data=row_data_for_cows_data
        self.root.get_screen('pageofcow').ids.currentcow.text="Просмотр коровы: "+cname
        
    #функция нажатия на строку списка коров
    def on_row_press(self, instance_table, instance_row):
        #index = instance_row.index
        #cols_num = len(instance_table. column_data)
        #row_num = int(index/cols_num)
        start_index,end_index=instance_row.table.recycle_data[instance_row.index]["range"]
        cname=instance_row.table.recycle_data[start_index]["text"]
        self.show_cow_characteristic(cname)    

    def editingcow(self): #предзаполнение полей для последующего измения
        self.root.current = 'editcows'
        cname=self.root.get_screen("pageofcow").ids.currentcow.text[17:]
        sqlite_select_query = """SELECT * FROM cows WHERE cowname = ?;""" 
        cur.execute(sqlite_select_query,[cname])
        one_row_data= cur.fetchall()[0]
        self.root.get_screen("editcows").ids.cowname2.text=one_row_data[0]
        self.root.get_screen("editcows").ids.status2.text=one_row_data[1]
        self.root.get_screen("editcows").ids.dateintext32.text=one_row_data[2]
        self.root.get_screen("editcows").ids.dateintext42.text=one_row_data[3]
        self.root.get_screen("editcows").ids.dateintext52.text=one_row_data[4]
        self.root.get_screen("editcows").ids.dateintext62.text=one_row_data[5]
        
    def save_cow_def_afterediting(self): #Сохранение изменений коровы
        cowname=self.root.get_screen("editcows").ids.cowname2.text
        status=self.root.get_screen("editcows").ids.status2.text
        d1=self.root.get_screen("editcows").ids.dateintext32.text
        d2=self.root.get_screen("editcows").ids.dateintext42.text
        d3=self.root.get_screen("editcows").ids.dateintext52.text
        d4=self.root.get_screen("editcows").ids.dateintext62.text
        cname=self.root.get_screen("pageofcow").ids.currentcow.text[17:]
        query="""UPDATE cows 
                SET 
                cowname=?,
                status=?,
                date_of_birth=?,
                date_of_last_calving=?,
                date_of_insemination=?,
                date_of_expectrd_calving=?
                WHERE cowname=?;"""
        cur.execute(query, [cowname,status,d1,d2,d3,d4,cname])
        bd.commit()
        #обновляем таблицу коров
        sqlite_select_query3 = """SELECT cowname,status FROM cows;""" 
        cur.execute(sqlite_select_query3)
        row_data_for_listofcow = cur.fetchall()
        self.listofcow.row_data=row_data_for_listofcow
        self.root.current = 'cows'    

    def on_save3(self, instance, value, date_range):
        self.root.get_screen('milkyield').ids.dateintext7.text=str(value)
        sqlite_select_query = f"""SELECT * FROM yields WHERE date_of_milking=?  ;""" 
        cur.execute(sqlite_select_query,[value])
        row_data_for_table = cur.fetchall()
        print(row_data_for_table)
        sum_morning=0
        sum_afternoon=0
        sum_evening=0
        for row in row_data_for_table:
            if row[1]=="утро":
                sum_morning+=row[3]
            elif row[1]=="день":
                sum_afternoon+=row[3]
            elif row[1]=="вечер":
                sum_evening+=row[3]
        self.root.get_screen('milkyield').ids.morning_milk.text=str(sum_morning)
        self.root.get_screen('milkyield').ids.afternoon_milk.text=str(sum_afternoon)
        self.root.get_screen('milkyield').ids.evening_milk.text=str(sum_evening)
    def on_cancel3(self, instance, value):
        pass   
    def show_date_picker_for_milk(self): #выбор даты в окне "Удои"
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save3, on_cancel=self.on_cancel3)
        date_dialog.open()

    #функция открытия удоев по коровам
    def open_milkyield_by_cows(self,period):
        self.root.get_screen('milkyield_by_cows').ids.cows_and_milk.clear_widgets()
        self.root.current = "milkyield_by_cows"
        global period_of_day
        period_of_day=period
        sqlite_select_query = """SELECT cowname from cows"""  #выгрузка списка коров
        cur.execute(sqlite_select_query)
        list_of_cows = cur.fetchall()
        date_of_milking=self.root.get_screen('milkyield').ids.dateintext7.text
        self.root.get_screen('milkyield_by_cows').ids.date_of_milking.text=date_of_milking
        self.root.get_screen('milkyield_by_cows').ids.period_of_day.text=period_of_day
        for cow in list_of_cows: #выгрузка удоев на определенную дату и время суток по каждой корове
            one_yield=0
            cowname=cow[0]
            sqlite_select_query = f"""SELECT * FROM yields WHERE date_of_milking=? AND period_of_day=? AND cowname=?;""" 
            cur.execute(sqlite_select_query,[date_of_milking,period_of_day,cowname])
            data_query=cur.fetchall()
            if data_query!=[]:
                one_yield = data_query[0][3]
            NewBoxLayout=BoxLayout(orientation="horizontal")
            NewCow=MDLabel(text=cowname)#создаем виджеты
            NewYield=MDTextField(text=str(one_yield))
            NewBoxLayout.add_widget(NewCow)
            NewBoxLayout.add_widget(NewYield)
            self.root.get_screen('milkyield_by_cows').ids.cows_and_milk.add_widget(NewBoxLayout)


    def save_yield(self):
        date_of_milking=self.root.get_screen('milkyield').ids.dateintext7.text
        sqlite_select_query ="""SELECT * FROM yields WHERE date_of_milking=? AND period_of_day=?;""" 
        cur.execute(sqlite_select_query,[date_of_milking,period_of_day])
        data_query=cur.fetchall()
        for i in self.root.get_screen('milkyield_by_cows').ids.cows_and_milk.children:
            cname=i.children[1].text
            one_yield=float(i.children[0].text)
            check=0
            for oldyield in data_query:
                if oldyield[2]==cname :
                    #обновляем данные, отмечаем изменение в check и выходим из цикла
                    query="""UPDATE yields
                            SET volume=?
                            WHERE
                            date_of_milking=? AND
                            period_of_day=? AND
                            cowname=?;"""
                    cur.execute(query, [one_yield,date_of_milking,period_of_day,cname])
                    bd.commit()
                    check=1
                    break
            if check==0 and one_yield!=0:
                #добавляем новую запись в БД
                query="""INSERT INTO yields VALUES(
                        ?,
                        ?,
                        ?,
                        ?);"""
                cur.execute(query, [date_of_milking,period_of_day,cname,one_yield])
                bd.commit()
                #Наконец обновим окно удоев по дате (MilkYield_main)
                sqlite_select_query = f"""SELECT * FROM yields WHERE date_of_milking=?  ;""" 
                cur.execute(sqlite_select_query,[date_of_milking])
                row_data_for_table = cur.fetchall()
                sum_morning=0
                sum_afternoon=0
                sum_evening=0
                for row in row_data_for_table:
                    if row[1]=="утро":
                        sum_morning+=row[3]
                    elif row[1]=="день":
                        sum_afternoon+=row[3]
                    elif row[1]=="вечер":
                        sum_evening+=row[3]
                self.root.get_screen('milkyield').ids.morning_milk.text=str(sum_morning)
                self.root.get_screen('milkyield').ids.afternoon_milk.text=str(sum_afternoon)
                self.root.get_screen('milkyield').ids.evening_milk.text=str(sum_evening)
        self.open_milkyield_by_cows(period_of_day)

    def download_yield(self):
        columns=['Дата', 'Период дня', 'Кличка', 'Удой']
        sqlite_select_query = """SELECT * FROM yields;""" 
        cur.execute(sqlite_select_query)
        row_data_for_table = cur.fetchall()
        df = pd.DataFrame(row_data_for_table, columns=columns)
        df.to_csv(r'C:/Users/katya/Documents/MyProject/MyProject/yield.csv')

    def build(self):
        root = Builder.load_file('main.kv') #явное обращение к файлу .kv
        #Проведем начальные приготовления
            #подготовка таблицы для окна "Calendar"
        sqlite_select_query = """SELECT * FROM event ORDER BY date_of_event DESC ;""" #WHERE DATE_OF_EVENT > currentday
        cur.execute(sqlite_select_query)
        row_data_for_table = cur.fetchall()

        self.data_tables = MDDataTable(
            use_pagination=True,
            size_hint=(1,1),
            column_data=[
                ("Дата", dp(25)),
                ("Кличка", dp(20)),
                ("Описание события", dp(60))],
            row_data=row_data_for_table)
        root.get_screen('calendar').ids.table.add_widget(self.data_tables)
        root.get_screen('calendar').ids.dateintext1.text="Весь период"
            #подготовка таблицы списка коров
        sqlite_select_query2 = """SELECT cowname,status FROM cows;""" #WHERE DATE_OF_EVENT > currentday
        cur.execute(sqlite_select_query2)
        row_data_for_listofcow = cur.fetchall()
            #подготовка списка коров
        self.listofcow = MDDataTable(
            use_pagination=True,
            size_hint=(1,1),
            column_data=[
                ("Кличка", dp(30)),
                ("Статус", dp(40))],
            row_data=row_data_for_listofcow)
        root.get_screen('cows').ids.table.add_widget(self.listofcow)
        self.listofcow.bind(on_row_press=self.on_row_press)
        #предзаполение для окна Новой коровы
        root.get_screen('newcows').ids.dateintext3.text="<Дата рождения коровы>"
        root.get_screen('newcows').ids.dateintext4.text="<Дата последнего отела>"
        root.get_screen('newcows').ids.dateintext5.text="<Дата осеменения коровы>"
        root.get_screen('newcows').ids.dateintext6.text="<Предполагаемая дата отела коровы>"

        #подготовка таблицы характеристик коровы
        self.data_CowCharacteristic = MDDataTable(
            use_pagination=True,
            size_hint=(1,1),
            column_data=[
                ("Характеристика", dp(30)),
                ("Значение", dp(40))],
            row_data=[])
        root.get_screen('pageofcow').ids.table3.add_widget(self.data_CowCharacteristic)

        #подготовка удоев для окна "Удои"
        current_date=str(date.today())
        root.get_screen("milkyield").ids.dateintext7.text=current_date
        sqlite_select_query3 = """SELECT * FROM yields WHERE date_of_milking=?;""" 
        cur.execute(sqlite_select_query3,[current_date])
        row_data_for_table3 = cur.fetchall()
        sum_morning=0
        sum_afternoon=0
        sum_evening=0
        for row in row_data_for_table3:
            if row[1]=="утро":
                sum_morning+=row[3]
            elif row[1]=="день":
                sum_afternoon+=row[3]
            elif row[1]=="вечер":
                sum_evening+=row[3]
        root.get_screen('milkyield').ids.morning_milk.text=str(sum_morning)
        root.get_screen('milkyield').ids.afternoon_milk.text=str(sum_afternoon)
        root.get_screen('milkyield').ids.evening_milk.text=str(sum_evening)

        return root 
        
        
#Начало выполнения кода        
if __name__ == '__main__':
    #Создание БД
    bd=sqlite3.connect("BDForDoyka.db")
    cur=bd.cursor()
    cur.execute( 
        """ CREATE TABLE IF NOT EXISTS event(
            date_of_event date,
            cowname text,
            description text)
            """ )
    cur.execute( 
        """CREATE TABLE IF NOT EXISTS cows(
            cowname text,
            status text,
            date_of_birth date,
            date_of_last_calving date,
            date_of_insemination date,
            date_of_expectrd_calving date)
            """ )
    cur.execute( 
        """CREATE TABLE IF NOT EXISTS yields(
            date_of_milking date,
            period_of_day text,
            cowname text,
            volume float)
        """ )
    #cur.execute( 
    #    """DROP TABLE yields""" )
    bd.commit()
    MainApp().run() 
    bd.close()



