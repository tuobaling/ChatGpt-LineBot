import requests
from bs4 import BeautifulSoup
import datetime as dt

# 新聞資料
def stock_news(stock_name = "大盤"):
  data=[]

  if stock_name == "大盤" or stock_name == "美股":
    stock_name = "美股"
    json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name} -盤中速報&limit=5&page=1').json() # 取得美股 Json 格式資料
    items = json_data['data']['items']
    # print(items)
    for item in items:
        # 網址、標題和日期
        news_id = item["newsId"]
        title = item["title"]
        if "<mark>" in title:
          title = title.replace("<mark>", "").replace("</mark>", "")
        # print(title)
        publish_at = item["publishAt"]
        # print(publish_at)
        # 使用 UTC 時間格式 Coordinated Universal Time 世界協調時間
        utc_time = dt.datetime.utcfromtimestamp(publish_at) # 把原本很大的數字(時間戳記)轉成日期時間
        # print(utc_time)
        formatted_date = utc_time.strftime('%Y-%m-%d')
        # 前往網址擷取內容
        url = requests.get(f'https://news.cnyes.com/'
                          f'news/id/{news_id}').content
        soup = BeautifulSoup(url, 'html.parser')
        p_elements = soup.find_all('p')
        # print(p_elements)
        # 提取段落内容
        p = ''
        for paragraph in p_elements[4:]:
          # print(paragraph.text)
          p += paragraph.get_text()
        data.append([stock_name, formatted_date, title, p])
    return data

  else:
    # 取得個股 Json 格式資料
    json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name}&limit=50&page=1').json()
    # print(json_data)
    # 依照格式擷取資料
    items = json_data['data']['items']
    # print(items)
    for item in items:
      # 標題、網址、和日期
      title = item["title"]
      if "<mark>" in title:
        title = title.replace("<mark>", "").replace("</mark>", "")
        if stock_name not in title:
          continue
        # print(title)

        news_id = item["newsId"]

        # 前往網址擷取內容
        url = requests.get(f'https://news.cnyes.com/'
                          f'news/id/{news_id}').content
        soup = BeautifulSoup(url, 'html.parser')
        p_elements = soup.find_all('p')
        # print(p_elements)
        # 提取段落内容
        p = ''
        for paragraph in p_elements[4:]:
          p += paragraph.get_text()

        if p == "":
          continue

        publish_at = item["publishAt"]
        # print(publish_at)
        # 使用 UTC 時間格式 Coordinated Universal Time 世界協調時間
        utc_time = dt.datetime.utcfromtimestamp(publish_at) # 把原本很大的數字(時間戳記)轉成日期時間
        # print(utc_time)
        formatted_date = utc_time.strftime('%Y-%m-%d')

        data.append([stock_name, formatted_date, title, p])
    return data

# for new in stock_news("蘋果"):
#   print(new)
# stock_news()