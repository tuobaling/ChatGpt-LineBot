import yfinance as yf

# import datetime as dt


# 從 yfinance 取得一周股價資料
def Indicator(stock_id="大盤"):

  if stock_id == "大盤":
    stock_id = "^IXIC"  # NASDAQ # ^GSPC是S&P500
  # end = dt.date.today()
  # start = end - dt.timedelta(days = 20)
  stock_df = yf.download(stock_id, period="6mo")  # 取得今天以前的6個月的資料

  # 計算8日MA、13日MA等指標
  stock_df['8MA'] = stock_df['Close'].rolling(window=8).mean()
  stock_df['13MA'] = stock_df['Close'].rolling(window=13).mean()
  stock_df['12EMA'] = stock_df['Close'].ewm(span=12, adjust=False).mean()
  stock_df['26EMA'] = stock_df['Close'].ewm(span=26, adjust=False).mean()
  stock_df['MACD'] = stock_df['12EMA'] - stock_df['26EMA']
  stock_df['Signal Line'] = stock_df['MACD'].ewm(span=9, adjust=False).mean()
  stock_df['MACD_Histogram'] = stock_df['MACD'] - stock_df['Signal Line']
  stock_df['Upper_Band'] = stock_df['Close'].rolling(
    window=20).mean() + stock_df['Close'].rolling(window=20).std() * 1.5
  stock_df['Lower_Band'] = stock_df['Close'].rolling(
    window=20).mean() - stock_df['Close'].rolling(window=20).std() * 1.5
  return stock_df.tail(10)


# def main():
#   display(Indicator("AAPL")) # 可填個股代碼，沒填就是大盤(以NASDAQ為例)
#   # Indicator()

# if __name__ == "__main__":
#   main()
