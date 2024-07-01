import openai
from replit import db
import pandas as pd
from my_commands.stock_price import Indicator
from my_commands.stock_news_updated import get_html, get_news, get_stock_name
from my_commands.stock_value import stock_fundamental

df_stock_names = pd.read_csv('US_stock_names.csv')


# 建立 GPT 3.5-16k 模型
def get_reply(messages):
  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      # model = "gpt-4",
      messages=messages)
    reply = response.choices[0].message.content
  except openai.OpenAIError as err:
    reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
  return reply


# 建立訊息模板(Prompt)
def generate_content_msg(symbol):
  stock_name = get_stock_name(symbol, df_stock_names)  # 對照股名，否則回傳大盤（NASDAQ）

  price_data = Indicator(symbol)
  html = get_html(stock_name)
  news_data = get_news(symbol, html)

  content_msg = '請依據以下資料來進行分析並給出一份完整的分析報告:\n'

  content_msg += f'近期價格和交易量資訊:\n {price_data[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]}\n'

  content_msg += f'近期技術指標:\n {price_data[["8MA", "13MA", "12EMA",	"26EMA", "MACD", "Signal Line",	"MACD_Histogram", "Upper_Band", "Lower_Band"]]}\n'

  if symbol != "大盤":
    stock_value_data = stock_fundamental(symbol)
    content_msg += f'每季財報資訊：\n {stock_value_data}\n'

  content_msg += f'近期新聞資訊: \n {news_data}\n'
  content_msg += f'請給我{stock_name}近期的趨勢報告,請以詳細、\
    嚴謹及專業的角度撰寫此報告,並提及重要的數字以及新聞部分句子佐證, reply in 繁體中文'

  return content_msg


# StockGPT
def stock_gpt(symbol="大盤"):
  content_msg = generate_content_msg(symbol)  # 大盤也有開高低收

  msg = [{
    "role":
    "system",
    "content":
    "你現在是一位專業的證券分析師, 你會統整近期的股價、技術指標\
      、基本面、新聞資訊等方面並進行分析, 然後生成一份專業的趨勢分析報告"
  }, {
    "role": "user",
    "content": content_msg
  }]

  reply_data = get_reply(msg)

  return reply_data
