from kivy.app import App
from kivymd.app import MDApp
from kivy.lang.builder import Builder

#импорт классов для layout
from kivy.uix.boxlayout import BoxLayout
#импорт классов для виджетов
from kivy.uix.label import Label
from kivy.properties import ObjectProperty # создает ссылку на объект python
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.pickers import MDDatePicker

#Доп классы для создания определеленных виджетов
class Calendar(Screen):
    pass
class Cows(Screen):
    pass
class MilkYield(Screen):
    pass
class WindowManager(ScreenManager):
    pass

#Создание основного класса приложения
class MainApp(MDApp):
    def on_save(self, instance, value, date_range):
        link_to_calendar = self.root.get_screen('calendar')
        link_to_calendar.ids.text_input.text=str(value) 
    def on_cancel(self, instance, value):
        pass   
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def build(self):
        Builder.load_file('main.kv') #явное обращение к файлу .kv
         

#Начало выполнения кода        
if __name__ == '__main__':
    app = MainApp()
    app.run()
    
