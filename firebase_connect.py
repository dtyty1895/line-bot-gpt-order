import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import _G
load_dotenv()

class FirebaseConnect:
    def __init__(self) -> None:
        self.cred = credentials.Certificate("linebot-ordergpt-firebase-adminsdk-rdheg-bf3a86fe29.json")
        self.ref = None
    def firebase_init(self):
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })
        self.ref = db.reference("/")

    def get_menus(self):
        _G.menus = self.ref.child('Menus').get()
      
    def test_input(self):

        # 測試連接，例如寫入一個測試資料
        test_data = {
            'message': 'Hello, Realtime Database!'
        }
        self.ref.child('test_collection').set(test_data)
        print("Firebase 輸入資料測試成功！")

    def test_ouput(self):
        a = self.ref.child('test_collection').get()
        print(a)
        print("Firebase 獲取資料測試成功！")

    def test_connect(self):
        self.test_input()
        self.test_ouput()