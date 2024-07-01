import numpy as np
import pandas as pd
import yfinance as yf


# 基本面資料
def stock_fundamental(stock_id="大盤"):
  if stock_id == "大盤":
    return None

  stock = yf.Ticker(stock_id)  # 一個物件，可以取得報表等資訊
  balance_sheet = stock.quarterly_balance_sheet  # 資產負債表(B/S)
  financials = stock.quarterly_financials  # 綜合損益表(I/S)

  # 資產負債表(B/S) + 綜合損益表(I/S)
  Total_statement = pd.concat([balance_sheet, financials], axis=0)

  # 流動比率
  current_ratio = np.round(
    (Total_statement.loc["Current Assets"] /
     Total_statement.loc["Current Liabilities"]).tolist(), 2)

  # 營業收入
  quarterly_revenue = np.round(Total_statement.loc["Total Revenue"].tolist(),
                               2)

  # 營收成長率
  quarterly_revenue_growth = np.round(
    Total_statement.loc["Total Revenue"].pct_change(-1).dropna().tolist(),
    2)  # pct_change(-1)代表跟前一季比較，因為是季報
  # dropna預設會把橫的空值刪掉
  # 三率成長率
  # 營業毛利成長率
  quarterly_gross_profit_growth = np.round(
    Total_statement.loc["Gross Profit"].pct_change(-1).dropna().tolist(), 2)

  # 營業利益成長率
  quarterly_operating_Income_growth = np.round(
    Total_statement.loc["Operating Income"].pct_change(-1).dropna().tolist(),
    2)

  # 稅後淨利成長率
  quarterly_net_Income_growth = np.round(
    Total_statement.loc["Net Income"].pct_change(-1).dropna().tolist(), 2)

  # 每季EPS
  quarterly_eps = np.round(Total_statement.loc["Basic EPS"].dropna().tolist(),
                           2)

  # EPS季增率
  quarterly_eps_growth = np.round(
    Total_statement.loc["Basic EPS"].pct_change(-1).dropna().tolist(), 2)

  # 轉換日期
  dates = [
    date.strftime('%Y-%m-%d') for date in stock.quarterly_financials.columns
  ]

  data = {
    '季日期':
    dates[:len(quarterly_revenue_growth)],  # 因為時間從報表的左到右是新到舊，所以這行會把最後一行的日期用掉
    "流動比率": current_ratio.tolist(),  # 由array轉list
    "營業收入": quarterly_revenue.tolist(),
    '營收成長率': quarterly_revenue_growth.tolist(),  # 總之，成長率和日期會比eps少一筆，可能為了取一年
    "營業毛利成長率": quarterly_gross_profit_growth.tolist(),
    "營業利益成長率": quarterly_operating_Income_growth.tolist(),
    "稅後淨利成長率": quarterly_net_Income_growth.tolist(),
    'EPS': quarterly_eps.tolist(),
    'EPS 季增率': quarterly_eps_growth.tolist()
  }

  return data


# def main():
#   display(stock_fundamental("aapl")) # 大盤沒有基本面資料 # 大小寫都可以

# if __name__ == "__main__":
#   main()
