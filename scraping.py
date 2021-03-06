import os
import urllib.parse
from time import sleep
import re
import pathlib
import requests
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# 設定
PATH = os.path.join(os.environ["USERPROFILE"], "Downloads")  # 保存先パス
SLEEP_BETWEEN_INTERACTIONS = 2  # クリックなどの動作後の待ち時間（秒）


# ドライバ設定
driver_path = r".\chromedriver.exe"
chrome_service = fs.Service(executable_path=driver_path)
options = Options()
options.add_argument('--headless')
options.add_experimental_option(
    'excludeSwitches', ['enable-automation', 'enable-logging'])


# main関数
def main():
    print("検索ワードを入力してください")
    print("例: ねこ　かわいい　イラスト")
    search_word = input("検索ワード: ")
    print()

    print("ダウンロードする枚数を入力してください")
    print("例: 10")
    img_num = int(input("枚数: "))
    print()

    # ブラウザ起動
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # Google画像検索でキーワードを検索
    driver.get(
        "https://www.google.co.jp/search?q={}&hl=ja&tbm=isch".format(urllib.parse.quote(search_word)))

    # ページ上の画像のサムネイルを読み込み
    print("ページ読み込み: 開始-------------------------------------------------------------------------------")
    temp = 0
    while True:
        thumbnails = driver.find_elements(
            By.XPATH, "//img[@class='rg_i Q4LuWd']")
        count = len(thumbnails)
        print("画像候補数: "+str(count))
        if(count > img_num*2 or count == temp):
            break
        temp = count
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        sleep(SLEEP_BETWEEN_INTERACTIONS)
    print("ページ読み込み: 完了-------------------------------------------------------------------------------", end="\n\n")

    # 画像のサムネイルをひとつずつクリックして画像のURLを取得
    print("画像URL取得: 開始----------------------------------------------------------------------------------")
    img_urls = []
    count = 1
    for thumbnail in thumbnails:
        if count > img_num:
            break
        driver.execute_script('arguments[0].click();', thumbnail)
        sleep(SLEEP_BETWEEN_INTERACTIONS)
        candidates = driver.find_elements(By.CLASS_NAME, "n3VNCb")
        for candidate in candidates:
            img_url = candidate.get_attribute("src")
            if re.search("^https", img_url) and re.search("jpg$", img_url):
                img_urls.append(img_url)
                print("画像"+str(count)+": "+img_url)
                count += 1
                break
    print("画像URL取得: 完了----------------------------------------------------------------------------------", end="\n\n")

    # ブラウザ終了
    driver.quit()

    # 画像をダウンロードして保存
    print("画像ダウンロード: 開始-----------------------------------------------------------------------------")
    word = search_word.replace("　", " ").replace(" ", "_")
    image_path = os.path.join(PATH, word)
    pathlib.Path(image_path).mkdir()
    for i, img_url in enumerate(img_urls, 1):
        res = requests.get(img_url)
        filename = word+"_"+str(i)+".jpg"
        with open(os.path.join(image_path, filename), "wb") as file:
            file.write(res.content)
        print("画像"+str(i)+": "+filename)
        sleep(SLEEP_BETWEEN_INTERACTIONS)
    print("画像ダウンロード: 完了-----------------------------------------------------------------------------")
    input("エンターキーを押して終了")


# main関数呼び出し
if __name__ == "__main__":
    main()
