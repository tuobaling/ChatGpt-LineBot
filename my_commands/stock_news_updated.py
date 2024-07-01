import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
# from selenium import webdriver
# from selenium.webdriver.common.by import By

def get_stock_name(symbol, df): # 取得股票全名，或是大盤（NASDAQ）
  if symbol == "大盤":
    return "NASDAQ"
  return df[df["short_stock_names"] == symbol].iloc[0]["long_stock_names"]

def get_html(name):

  # chrome_options = webdriver.ChromeOptions()
  # chrome_options.add_argument("--headless") # 不顯示瀏覽器 # colab一定要有這行
  # chrome_options.add_argument("--no-sandbox") # 以最高權限運行

  # driver = webdriver.Chrome(options = chrome_options)
  # driver.get("https://news.yahoo.com/")

  # _input = driver.find_element(By.ID, "ybar-sbq")
  # search = driver.find_element(By.ID, "ybar-search")

  # _input.send_keys(name)
  # search.click()
  # time.sleep(2) # 這個刪掉就會出錯
  # many_a = driver.find_elements(By.TAG_NAME, "a")
  # for a in many_a:
  #   if a.text == "More": # 防止News在More裡，所以無論如何都先點一下More
  #     more = a
  #     more.click()
  #     # driver.save_screenshot("test.png")
  #     break
  # many_a = driver.find_elements(By.TAG_NAME, "a")
  # for a in many_a:
  #   if a.text == "News":
  #     news = a
  #     break
  #   # print(a.text)

  # news.click()
  # time.sleep(2)
  # url = driver.current_url # https://news.search.yahoo.com/search?p=AAPL&fr2=piv-web&.tsrc=uh3_news_web&fr=uh3_news_web
  # print(url)
  # response = requests.get(url) # 這行跟46行的結果等於47、48行
  # return response.content
  # html = driver.page_source
  # return html

  # driver.save_screenshot("test.png")
  response = requests.get(f"https://news.search.yahoo.com/search?p={name}&fr2=piv-web&.tsrc=uh3_news_web&fr=uh3_news_web")
  return response.content

def get_news(symbol, html):
  links_soup = bs(html, features = "html.parser")
  # print(links_soup.prettify())
  titles = []
  updated_titles = [] # 有時候會有問題而設置的
  links = []
  articles = []
  times = []

  divs = links_soup.find_all("div", attrs = {"class": "dd NewsArticle"})
  for div in divs:
    h4 = div.find("h4")
    title = h4.text
    link = div.find("a").get("href")
    if "https://finance.yahoo.com/news/" in link: # 防止格式不一，所以只抓Yahoo的
      titles.append(title)
      # print(title)
      links.append(link)
      # print(link)
  # print(links)
  for index in range(len(links)):
    article = ""
    response = requests.get(links[index])
    news_soup = bs(response.text, features = "html.parser")
    news_time = news_soup.find("div", attrs = {"class": "caas-attr-time-style"})
    if news_time == None: # 防止時間抓不到而出錯
      continue
    times.append(news_time.text)
    updated_titles.append(titles[index])
    div = news_soup.find("div", attrs = {"class": "caas-body"})
    ps = div.findAll("p")
    for p in ps:
      article += p.text
    articles.append(article)
    time.sleep(2)
  # print(titles, times, articles)
  # 以下為將資料做成二維表格
  df_news = pd.DataFrame()
  df_news["Company"] = [symbol] * len(updated_titles)
  df_news["Titles"] = updated_titles
  df_news["Times"] = times
  df_news["Articles"] = articles
  return df_news

# def main():
#   symbol = input("請輸入美股代碼: ")
#   name = get_stock_name(symbol, df_stock_names)
#   html = get_html(name)
#   df_news = get_news(symbol, html)
#   display(df_news)
  # 以下註解其實就是get_html函式在做的
  # import requests
  # from bs4 import BeautifulSoup as bs

  # keyword = get_stock_name("AAPL", df_stock_names)
  # response = requests.get(f"https://news.search.yahoo.com/search?p={keyword}&fr2=piv-web&.tsrc=uh3_news_web&fr=uh3_news_web")
  # soup = bs(response.text, "html.parser")
  # print(soup.prettify())


# if __name__ == "__main__":
#   main()