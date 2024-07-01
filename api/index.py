from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

from api.my_commands.stock_gpt import stock_gpt, get_reply
import pandas as pd

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
df_stock_names = pd.read_csv('US_stock_names.csv')
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        print("電子簽章錯誤, 請檢查密鑰是否正確？")
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    user_message = event.message.text
      
    if event.message.type != "text":
        return
    
    if user_message == "啟動":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我是時下流行的AI智能，目前可以為您服務囉，歡迎來跟我互動~"))
        return

    if user_message == "安靜":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="感謝您的使用，若需要我的服務，請跟我說 「啟動」 謝謝~"))
        return
    
    if user_message == '大盤' or (user_message.upper() in list(
        df_stock_names["short_stock_names"])):
      working_status = True
      reply_text = stock_gpt(user_message.upper())
    # 一般訊息
    else:
      msg = [{
        "role": "system",
        "content": "reply in 繁體中文"
      }, {
        "role": "user",
        "content": user_message
      }]
      working_status = True
      reply_text = get_reply(msg)

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))
  
    #if working_status:
    #    chatgpt.add_msg(f"Human:{event.message.text}?\n")
    #    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    #    chatgpt.add_msg(f"AI:{reply_msg}\n")
    #    line_bot_api.reply_message(
    #        event.reply_token,
    #        TextSendMessage(text=reply_msg))


if __name__ == "__main__":
    app.run()
