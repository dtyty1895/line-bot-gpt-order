from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import tempfile, os
import datetime
import openai
import time
import traceback
import firebase_admin
from firebase_admin import credentials, db
from firebase_connect import FirebaseConnect
import json
from utils import OpenAIAgent

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']            # 回覆的 reply token
        timestamp = json_data['events'][0]['timestamp']      # 訊息時間戳
        msg_type = json_data['events'][0]['message']['type'] # 訊息類型
        # 如果是文字訊息
        if msg_type == 'text':
            msg = json_data['events'][0]['message']['text']  # 取出文字內容
            chatgpt = firebaseconnect.ref.get('test_collection')              # 讀取 Firebase 資料庫內容
            print(f"chatgpt : {chatgpt}")

            if chatgpt == None:
                messages = []       # 如果資料庫裡沒有內容，建立空串列
            else:
                messages = chatgpt  # 如果資料庫裡有內容，設定歷史紀錄為資料庫內容

            if msg == '!reset':
                pass
                # fdb.delete('/','chatgpt')    # 如果收到 !reset 的訊息，表示清空資料庫內容
                # reply_msg = TextSendMessage(text='對話歷史紀錄已經清空！')
            else:
                messages.append({"role":"user","content":msg})  # 如果是一般文字訊息，將訊息添加到歷史紀錄裡
                response = openai_agent._get_chat_completion(messages)
                ai_msg = response.choices[0].message.content.replace('\n','')  # 移除回應裡的換行符
                messages.append({"role":"assistant","content":ai_msg})  # 歷史紀錄裡添加回應訊息
                firebaseconnect.ref.set(messages)        # 使用非同步的方式紀錄訊息
                reply_msg = TextSendMessage(text=ai_msg)     # 回應訊息
            line_bot_api.reply_message(tk,reply_msg)
        else:
            reply_msg = TextSendMessage(text='你傳的不是文字訊息呦')
            line_bot_api.reply_message(tk,reply_msg)
    except:
        print('error')
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    firebaseconnect = FirebaseConnect()
    firebaseconnect.firebase_init()
    firebaseconnect.get_menus()
    openai_agent = OpenAIAgent()
    openai_agent._set_system()  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)