
"------------الكود الشامل-----------"

"""from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import pyodbc
from datetime import datetime
import sys
import arabic_reshaper
from kivy.uix.stacklayout import StackLayout
from bidi.algorithm import get_display


Window.clearcolor = (50/255.0, 0, 0, 2)
Window.size = (400, 500)

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.build()
        self.failed_attempts = 0
    def build(self):
        layout = GridLayout(cols=1, padding=10, spacing=10)
        self.username = TextInput(hint_text='Username', size_hint=(0.01, 0.01))
        self.password = TextInput(hint_text='Password', password=True, size_hint=(0.01, 0.01))
        login_button = Button(text='Login', size_hint=(0.01, 0.01), on_press=self.login)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        self.add_widget(layout)

    def login(self, instance):
        # هنا يمكنك إضافة التحقق من اسم المستخدم وكلمة المرور
          conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=DESKTOP-P7EOFIG\\SQLEXPRESS;"
                              "DATABASE=Intelligence;"
                              "Trusted_Connection=yes;")
          cursor = conn.cursor()
          user = self.username.text
          pas = self.password.text
          if not self.username.text or not self.password.text:
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='Wrong, fill in the fields '))
            close_btn = Button(text='Close')
            content.add_widget(close_btn)

            popup = Popup(title='Wrong',
                          content=content,
                          size_hint=(0.6, 0.4))
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            user = self.username.text=""
            pas = self.password.text=""
          else:
            
            cursor.execute("SELECT name, password FROM enter WHERE name=? AND password=?", (user, pas))
            result = cursor.fetchall()
            if result:
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text='Successfully logged in'))
                close_btn = Button(text='Close')
                content.add_widget(close_btn)

                popup = Popup(title='clarification',
                              content=content,
                              size_hint=(0.6, 0.4))
                close_btn.bind(on_press=popup.dismiss)
                popup.open()
                self.manager.current = 'employee'
                user = self.username.text=""
                pas = self.password.text=""
            else:
                self.failed_attempts += 1
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text='Invalid username or password'))
                close_btn = Button(text='Close')
                content.add_widget(close_btn)

                popup = Popup(title='Error',
                              content=content,
                              size_hint=(0.6, 0.4))
                close_btn.bind(on_press=popup.dismiss)
                popup.open()
                user = self.username.text=""
                pas = self.password.text=""
                if self.failed_attempts >= 3:
                    sys.exit()
class CalculatorPage(Screen):
    def __init__(self, **kwargs):
        super(CalculatorPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        self.title = 'Calculator'
        layout = GridLayout(cols=4, padding=10, spacing=10)
        self.result = TextInput(font_size=32, readonly=True, halign='right', multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.result)
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
            '%'
        ]
        
        for button in buttons:
            layout.add_widget(Button(text=button, on_press=self.on_button_press, size_hint=(0.25, 0.2)))
        
        self.add_widget(layout)

    def on_button_press(self, instance):
        if instance.text == '%':
            self.manager.current = 'login'
        elif instance.text == 'C':
            self.result.text = ''
        elif instance.text == '=':
            try:
                self.result.text = str(eval(self.result.text))
            except Exception:
                self.result.text = 'Error'
        else:
            self.result.text += instance.text

class EmployeePage(Screen):
    def __init__(self, **kwargs):
        super(EmployeePage, self).__init__(**kwargs)
        self.build()

    def build(self):
        self.title = 'Employ'
        lay = GridLayout(cols=1, padding=10, spacing=10)
        self.ima = Image(source='1.jpg', size_hint=(3, 0.8))
        self.l1 = Label(text='Field monitoring', size_hint=(1, 0.2), font_size='18', font_name='Roboto-Bold')
        self.id = TextInput(hint_text='Customer Number', size_hint=(1, 0.2))
        self.id2 = TextInput(hint_text='Code Personal ', size_hint=(1, 0.2))
        self.dd = TextInput(hint_text='Date', size_hint=(1, 0.2), readonly=True)
        self.dd.text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.info_claa = TextInput(hint_text='Information classification', size_hint=(1, 0.2))
        self.stat = TextInput(hint_text='Statement', size_hint=(1, 0.3))
        self.lo = TextInput(hint_text='location', size_hint=(1, 0.2))
        self.tr_au = TextInput(hint_text='Number of telegram', size_hint=(1, 0.2))
        sub = Button(text='Add employee', size_hint=(1, 0.2), on_press=self.sub)
        view_button = Button(text='View Data', size_hint=(1, 0.2), on_press=self.view_data)
        lay.add_widget(self.ima)
        lay.add_widget(self.l1)
        lay.add_widget(self.id)
        lay.add_widget(self.id2)
        lay.add_widget(self.tr_au)
        lay.add_widget(self.dd)
        lay.add_widget(self.info_claa)
        lay.add_widget(self.stat)
        lay.add_widget(self.lo)
        lay.add_widget(sub)
        lay.add_widget(view_button)
        self.add_widget(lay)

    def sub(self, instance):
        d = self.id.text
        de = self.dd.text
        inf = self.info_claa.text
        st = self.stat.text
        l = self.lo.text
        tr = self.tr_au.text
        code_op=self.id2.text
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=DESKTOP-P7EOFIG\\SQLEXPRESS;"
                              "DATABASE=Intelligence;"
                              "Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("insert into feild (num_cust,date,class,statmen,num_address,target,code_op) values (?,?,?,?,?,?,?)", (d, de, inf, st, l, tr,code_op))
        conn.commit()
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Added Successfully'))
        close_btn = Button(text='Close')
        content.add_widget(close_btn)

        popup = Popup(title='insert',
                      content=content,
                      size_hint=(0.6, 0.4))

        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        self.id.text = ""
        inf = self.info_claa.text = ""
        st = self.stat.text = ""
        l = self.lo.text = ""
        tr = self.tr_au.text = ""
        code_op=self.id2.text=""
        conn.close()

    def view_data(self, instance):
        self.manager.current = 'viewdata'

class ViewDataPage(Screen):
    def __init__(self, **kwargs):
        super(ViewDataPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        # حاوية عامة لتوسيط المحتوى
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=(50, 100, 50, 100))

        # استخدام GridLayout لتنسيق البيانات كجدول
        table_layout = GridLayout(cols=len(self.get_headers()), spacing=10, size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        # إضافة العناوين كصف أول
        headers = self.get_headers()
        for header in headers:
            reshaped_header = arabic_reshaper.reshape(header)
            bidi_header = get_display(reshaped_header)
            table_layout.add_widget(Label(text=bidi_header, size_hint=(None, None), size=(150, 50), 
                                          font_name='NotoSansArabic-Regular.ttf', bold=True))

        # جلب البيانات من قاعدة البيانات وإضافتها
        data = self.get_data()
        for row in data:
            for cell in row:
                text = str(cell)
                if any('\u0600' <= char <= '\u06FF' for char in text):  # التحقق من وجود نص عربي
                    reshaped_text = arabic_reshaper.reshape(text)
                    bidi_text = get_display(reshaped_text)
                    table_layout.add_widget(Label(text=bidi_text, size_hint=(None, None), size=(150, 40), 
                                                  font_name='NotoSansArabic-Regular.ttf'))
                else:
                    table_layout.add_widget(Label(text=text, size_hint=(None, None), size=(150, 40), 
                                                  font_name='NotoSansArabic-Regular.ttf'))

        # إضافة ScrollView لتمكين التمرير
        scroll_view = ScrollView(size_hint=(1, None), size=(800, 600))
        scroll_view.add_widget(table_layout)

        # إضافة التمرير إلى الحاوية الرئيسية
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def get_headers(self):
        # العناوين المستخدمة في الجدول
        return ['رقم البرقية', 'عنوان التوجية', 'تاريخ التوجية', 'هدف التوجية', 'المخاطر', 'الموقع', 'مدة التوجية']

    def get_data(self):
        # جلب البيانات من قاعدة البيانات
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=DESKTOP-P7EOFIG\\SQLEXPRESS;"
                              "DATABASE=Intelligence;"
                              "Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("SELECT num_guid, subject_guid, date_guid, gold_guid, risk_guld, num_address, time_guld FROM guld")
        data = cursor.fetchall()
        conn.close()
        return data


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorPage(name='calculator'))
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(EmployeePage(name='employee'))
        sm.add_widget(ViewDataPage(name='viewdata'))
        return sm

if __name__ == '__main__':
    MyApp().run()
"""
"================================================="
'''from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
import pyodbc
import arabic_reshaper
from bidi.algorithm import get_display

class ViewDataPage(Screen):
    def __init__(self, **kwargs):
        super(ViewDataPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        layout = GridLayout(cols=7, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Adding headers
        headers = ['ID', 'Name', 'Location', 'Number of Persons', 'Image', 'Target', 'IDs']
        for header in headers:
            layout.add_widget(Label(text=header, size_hint_y=None, height=100, font_name='NotoSansArabic-Regular.ttf'))

        # Connecting to the database and fetching data
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=DESKTOP-P7EOFIG\\SQLEXPRESS;"
                              "DATABASE=Intelligence;"
                              "Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("SELECT num_cust, date, class, statment, loaction, target, id FROM field")
        data = cursor.fetchall()
        conn.close()

        # Adding data rows
        for row in data:
            for cell in row:
                reshaped_text = arabic_reshaper.reshape(str(cell))
                bidi_text = get_display(reshaped_text)
                layout.add_widget(Label(text=bidi_text, size_hint_y=None, height=40, font_name='NotoSansArabic-Regular.ttf'))

        root = ScrollView(size_hint=(1, None), size=(550, 700))  # تعديل العرض إلى 550 بكسل
        root.add_widget(layout)
        self.add_widget(root)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ViewDataPage(name='viewdata'))
        return sm

if __name__ == '__main__':
    MyApp().run()
'''
"========================"
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
import pyodbc

class ViewDataPage(Screen):
    def __init__(self, **kwargs):
        super(ViewDataPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        layout = GridLayout(cols=7, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Adding headers
        headers = ['ID', 'Name', 'Location', 'Number of Persons', 'Image', 'Target', 'IDs']
        for header in headers:
            layout.add_widget(Label(text=header, size_hint_y=None, height=100, font_name='NotoSansArabic-Regular.ttf'))

        # Connecting to the database and fetching data
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=DESKTOP-P7EOFIG\\SQLEXPRESS;"
                              "DATABASE=Intelligence;"
                              "Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("SELECT num_cust, date, class, statment, loaction, target, id FROM field")
        data = cursor.fetchall()
        conn.close()

        # Adding data rows
        for row in data:
            for cell in row:
                layout.add_widget(Label(text=str(cell), size_hint_y=None, height=40, font_name='NotoSansArabic-Regular.ttf'))

        root = ScrollView(size_hint=(1, None), size=(550, 700))  # تعديل العرض إلى 550 بكسل
        root.add_widget(layout)
        self.add_widget(root)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ViewDataPage(name='viewdata'))
        return sm

if __name__ == '__main__':
    MyApp().run()
'''

"=============="
'''from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
import pyodbc
import arabic_reshaper
from bidi.algorithm import get_display

class ViewDataPage(Screen):
    def __init__(self, **kwargs):
        super(ViewDataPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        layout = GridLayout(cols=7, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Adding headers
        headers = ['الرقم', 'الاسم', 'الموقع', 'الفئة', 'صورة', 'الإجراءات المستهدفة', 'رقم الترقيم']
        for header in headers:
            reshaped_header = arabic_reshaper.reshape(header)
            bidi_header = get_display(reshaped_header)
            layout.add_widget(Label(text=bidi_header, size_hint_y=None, height=100, font_name='NotoSansArabic-Regular.ttf'))

        # Connecting to the database and fetching data
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=DESKTOP-P7EOFIG\\SQLEXPRESS;"
                              "DATABASE=Intelligence;"
                              "Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("SELECT num_cust, date, class, statment, loaction, target, id FROM field")
        data = cursor.fetchall()
        conn.close()

        # Adding data rows
        for row in data:
            for cell in row:
                text = str(cell)
                if any('\u0600' <= char <= '\u06FF' for char in text):  # Check if the text contains Arabic characters
                    reshaped_text = arabic_reshaper.reshape(text)
                    bidi_text = get_display(reshaped_text)
                    layout.add_widget(Label(text=bidi_text, size_hint_y=None, height=40, font_name='NotoSansArabic-Regular.ttf'))
                else:
                    layout.add_widget(Label(text=text, size_hint_y=None, height=40, font_name='NotoSansArabic-Regular.ttf'))

        root = ScrollView(size_hint=(1, None), size=(550, 700))  # تعديل العرض إلى 550 بكسل
        root.add_widget(layout)
        self.add_widget(root)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ViewDataPage(name='viewdata'))
        return sm

if __name__ == '__main__':
    MyApp().run()
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import pyodbc
from datetime import datetime
import sys
import arabic_reshaper
from kivy.uix.stacklayout import StackLayout
from bidi.algorithm import get_display
import time
import os
import sys
from kivy.core.text import LabelBase

Window.clearcolor = (50/255.0, 0, 0, 2)
Window.size = (400, 500)


# تسجيل خط يدعم اللغة العربية


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.build()
        self.failed_attempts = 0
        self.block_file = "login_block.txt"

    def build(self):
        layout = GridLayout(cols=1, padding=10, spacing=10)
        self.username = TextInput(hint_text='username', size_hint=(0.01, 0.01))
        self.password = TextInput(hint_text='password', password=True, size_hint=(0.01, 0.01))
        login_button = Button(text='login', size_hint=(0.01, 0.01), on_press=self.login)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        self.add_widget(layout)

    def login(self, instance):
        # تحقق من الحظر
        if os.path.exists(self.block_file):
            with open(self.block_file, "r") as f:
                block_time = float(f.read())
            elapsed = time.time() - block_time
            if elapsed < 120:  # دقيقتان
                self.show_popup("🚫 Blocked", f"System is blocked for {int(120 - elapsed)} seconds")
                return
            else:
                os.remove(self.block_file)
                self.failed_attempts = 0

        user = self.username.text.strip()
        pas = self.password.text.strip()

        if not user or not pas:
            self.show_popup("⚠️ Warning", "Please enter both username and password.")
            return

        login_data = {'user': user, 'pass': pas}
        url = "https://flask-api-4-1sxj.onrender.com/login"
        
        try:
            response = requests.post(url, json=login_data)
        except Exception as e:
            self.show_popup("❌ Network Error", f"Unable to reach server:\n{str(e)}")
            return

        if response.status_code == 200:
            self.show_popup("✅ Success", "Successfully logged in.")
            self.manager.current = 'employee'
            self.failed_attempts = 0
            if os.path.exists(self.block_file):
                os.remove(self.block_file)
            return
        else:
            self.failed_attempts += 1
            try:
                msg = response.json().get("message", "Invalid login.")
            except Exception:
                msg = response.text
            self.show_popup("❌ Wrong", f"{msg} ({self.failed_attempts}/3)")

            if self.failed_attempts >= 3:
                with open(self.block_file, "w") as f:
                    f.write(str(time.time()))
                self.show_popup("🚫 Block", "System is blocked for 2 minutes.")
                return


    def show_popup(self, title, message):
        content = GridLayout(cols=1)
        content.add_widget(Label(text=message))
        close_button = Button(text="Close")
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class CalculatorPage(Screen):
    def __init__(self, **kwargs):
        super(CalculatorPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        self.title = 'Calculator'
        layout = GridLayout(cols=4, padding=10, spacing=10)
        self.result = TextInput(font_size=32, readonly=True, halign='right', multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.result)
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
            'MC','%','MR'
        ]
        
        for button in buttons:
            layout.add_widget(Button(text=button, on_press=self.on_button_press, size_hint=(0.25, 0.2)))
        
        self.add_widget(layout)

    def on_button_press(self, instance):
        if instance.text == '%':
            self.manager.current = 'login'
        elif instance.text == 'C':
            self.result.text = ''
        elif instance.text == '=':
            try:
                self.result.text = str(eval(self.result.text))
            except Exception:
                self.result.text = 'Error'
        else:
            self.result.text += instance.text

import requests

class EmployeePage(Screen):
    def __init__(self, **kwargs):
        super(EmployeePage, self).__init__(**kwargs)
        self.build()

    def build(self):
        self.title = 'Employ'

        scroll = ScrollView(size_hint=(1, 1))
        lay = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        lay.bind(minimum_height=lay.setter('height'))

        self.ima = Image(source='1.jpg', size_hint=(1, 0.8))
        self.l1 = Label(text='Field monitoring', font_size='18', font_name='Roboto-Bold', size_hint=(1, None), height=30)

        self.id = TextInput(hint_text='Customer Number', size_hint_y=None, height=40)
        self.id2 = TextInput(hint_text='Code Personal', size_hint_y=None, height=40)

        self.dd = TextInput(hint_text='Date', text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    size_hint_y=None, height=40, readonly=True, disabled=True)
        self.info_claa = TextInput(hint_text='Information classification', size_hint_y=None, height=40)
        self.stat = TextInput(hint_text='Statement', size_hint_y=None, height=80)
        self.lo = TextInput(hint_text='Location', size_hint_y=None, height=40)
        self.tr_au = TextInput(hint_text='Number of telegram', size_hint_y=None, height=40)

        sub = Button(text='Add Employee', size_hint_y=None, height=50, on_press=self.submit)
        view_button = Button(text='View Data', size_hint_y=None, height=50, on_press=self.view_data)
        logout_button = Button(text='Logout', size_hint_y=None, height=50)
        logout_button.bind(on_press=self.logout)

        # إضافة العناصر إلى الواجهة
        lay.add_widget(self.ima)
        lay.add_widget(self.l1)
        lay.add_widget(self.id)
        lay.add_widget(self.id2)
        lay.add_widget(self.tr_au)
        lay.add_widget(self.dd)
        lay.add_widget(self.info_claa)
        lay.add_widget(self.stat)
        lay.add_widget(self.lo)
        lay.add_widget(sub)
        lay.add_widget(view_button)
        lay.add_widget(logout_button)

        scroll.add_widget(lay)
        self.add_widget(scroll)
    def logout(self, instance):
        self.manager.current = 'calculator'


    def submit(self, instance):
        data = {
            'num_cust': self.id.text,
            'date': self.dd.text,
            'class': self.info_claa.text,
            'statmen': self.stat.text,
            'num_address': self.lo.text,
            'target': self.tr_au.text,
            'code_op': self.id2.text,
        }

        # تحقق من أن الحقول المطلوبة ليست فارغة
        for key, value in data.items():
            if not value.strip():
                self.show_popup("⚠️ Missing Field", f"The field '{key}' is required.")
                return

        url = "https://flask-api-4-1sxj.onrender.com/add_data"
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.show_popup("✅ Success", "Employee added successfully.")
            else:
                try:
                    msg = response.json().get("message", response.text)
                except Exception:
                    msg = response.text
                self.show_popup("❌ Error", f"Failed to add employee:\n{msg}")
        except Exception as e:
            self.show_popup("❌ Network Error", str(e))

        # إعادة تعيين الحقول
        self.id.text = ""
        self.info_claa.text = ""
        self.stat.text = ""
        self.lo.text = ""
        self.tr_au.text = ""
        self.id2.text = ""

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_btn = Button(text='Close')
        content.add_widget(close_btn)

        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


    def view_data(self, instance):
        self.manager.current = 'viewdata'

class ViewDataPage(Screen):
    def __init__(self, **kwargs):
        super(ViewDataPage, self).__init__(**kwargs)
        self.build()

    def build(self):
        # حاوية عامة لتوسيط المحتوى
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=(50, 100, 50, 100))

        # استخدام GridLayout لتنسيق البيانات كجدول
        table_layout = GridLayout(cols=len(self.get_headers()), spacing=10, size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))

        # إضافة العناوين كصف أول
        headers = self.get_headers()
        for header in headers:
            reshaped_header = arabic_reshaper.reshape(header)
            bidi_header = get_display(reshaped_header)
            table_layout.add_widget(Label(text=bidi_header, size_hint=(None, None), size=(150, 50), 
                                          font_name='NotoSansArabic-Regular.ttf', bold=True))

        # جلب البيانات من قاعدة البيانات وإضافتها
        data = self.get_data()
        for row in data:
            for cell in row:
                text = str(cell)
                if any('\u0600' <= char <= '\u06FF' for char in text):  # التحقق من وجود نص عربي
                    reshaped_text = arabic_reshaper.reshape(text)
                    bidi_text = get_display(reshaped_text)
                    table_layout.add_widget(Label(text=bidi_text, size_hint=(None, None), size=(150, 40), 
                                                  font_name='NotoSansArabic-Regular.ttf'))
                else:
                    table_layout.add_widget(Label(text=text, size_hint=(None, None), size=(150, 40), 
                                                  font_name='NotoSansArabic-Regular.ttf'))

        # إضافة ScrollView لتمكين التمرير
        scroll_view = ScrollView(size_hint=(1, None), size=(800, 600))
        scroll_view.add_widget(table_layout)
       
        # إضافة التمرير إلى الحاوية الرئيسية
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

        back_button = Button(text="back", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        
        # زر تسجيل الخروج
        exit_button = Button(text="logout", size_hint=(1, 0.1))
        exit_button.bind(on_press=lambda x: sys.exit())

        # إضافة الأزرار للحاوية الرئيسية
        main_layout.add_widget(back_button)
        main_layout.add_widget(exit_button)
        
    def go_back(self, instance):
        self.manager.current = 'employee'
    def get_headers(self):
        # العناوين المستخدمة في الجدول
        return ['رقم البرقية', 'عنوان التوجية', 'تاريخ التوجية', 'هدف التوجية', 'المخاطر', 'الموقع', 'مدة التوجية']

    def get_data(self):
        try:
            response = requests.get("https://flask-api-4-1sxj.onrender.com/data")  # Replace <your-server-ip> with your server's IP
            if response.status_code == 200:
                return response.json()  # Assuming the server returns a list of lists
            else:
             self.show_popup("❌ Error", f"Failed to fetch data. Response status: {response.status_code}")
             return []
        except Exception as e:
            self.show_popup("❌ Error", f"An error occurred while connecting to the server: {e}")
            return []

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_btn = Button(text='Close')
        content.add_widget(close_btn)

        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


    

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorPage(name='calculator'))
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(EmployeePage(name='employee'))
        sm.add_widget(ViewDataPage(name='viewdata'))
        return sm

if __name__ == '__main__':
    MyApp().run()