# モジュール
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import re
import os
import shutil
import urllib.parse
import pathlib
from selenium.webdriver.chrome.options import Options


# ドライバ読み込み
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver.exe", options=options)


# 定数
SEARCH_WORD = ""  # 検索ワード
IMG_NUM = 0  # 画像枚数
PATH = r""  # 保存先パス
SLEEP_BETWEEN_INTERACTIONS = 2  # クリックなどの動作後の待ち時間（秒）


# main関数
def main():
    # Google画像検索でキーワードを検索
    driver.get(
        "https://www.google.co.jp/search?q={}&hl=ja&tbm=isch".format(urllib.parse.quote(SEARCH_WORD)))

    # ページ上のすべての画像のサムネイルを取得
    thumbnails = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")

    # 画像のサムネイルをひとつずつクリックして画像のURLを取得
    print("画像URL取得: 開始----------------------------------------------------------------------------------")
    img_urls = []
    for i, thumbnail in enumerate(thumbnails, 1):
        if i > IMG_NUM:
            break
        thumbnail.click()
        sleep(SLEEP_BETWEEN_INTERACTIONS)
        candidates = driver.find_elements_by_class_name("n3VNCb")
        for candidate in candidates:
            img_url = candidate.get_attribute("src")
            if re.match("https", img_url):
                img_urls.append(img_url)
                print("画像"+str(i)+": "+img_url)
                break
    driver.close()
    print("画像URL取得: 完了----------------------------------------------------------------------------------", end="\n\n")

    # 画像をダウンロードして保存
    print("画像ダウンロード: 開始-----------------------------------------------------------------------------")
    word = SEARCH_WORD.replace("　", " ").replace(" ", "_")
    image_path = os.path.join(PATH, word)
    pathlib.Path(image_path).mkdir()
    for i, img_url in enumerate(img_urls, 1):
        res = requests.get(img_url, stream=True)
        filename = word+"_"+str(i)+".jpg"
        with open(os.path.join(image_path, filename), "wb") as file:
            shutil.copyfileobj(res.raw, file)
        print("画像"+str(i)+": "+filename)
        sleep(SLEEP_BETWEEN_INTERACTIONS)
    print("画像ダウンロード: 完了-----------------------------------------------------------------------------")


# main関数呼び出し
if __name__ == "__main__":
    main()
