from selenium import webdriver # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
from selenium import common
import time
import random
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(r"C:\Users\USER\Desktop\chromedriver_win32 (2)/chromedriver.exe")

TOP_URL = "https://www.instagram.com/accounts/login/?hl=ja&source=auth_switcher"
fPath = r"C:\Users\USER\Desktop\data"

randIntFrom = 3
randIntTo = 5

userIdList = list()
likeUserIdList = list()
unfollowUserIdList = list()
# get data from file or database
f = open(fPath + '/new_japantrip_2019-04-15.txt', 'r')
line = f.readline()
while line:
    line = f.readline()
    likeUserIdList.append(line)
f.close()

driver.set_page_load_timeout(600) # ページロード最大600秒
driver.get(TOP_URL) # chrome起動→ログインページに移動
time.sleep(random.randint(randIntFrom, randIntTo))

id = driver.find_element_by_name("username")
id.send_keys("mdiz1103@gmail.com")

passwordId = driver.find_element_by_name("password")
passwordId.send_keys("11032189")

time.sleep(random.randint(randIntFrom, randIntTo))

# ログインボタンをクリック
login_button = driver.find_elements_by_tag_name("button")
login_button[1].click()

# 少し待機
time.sleep(random.randint(randIntFrom, randIntTo))

driver.get("https://www.instagram.com/?hl=ja")

# pop up
buttons = driver.find_elements_by_tag_name("button")
bt = 0
for i in range(buttons.__len__()):
    if buttons[i].text == "後で":
        bt = i

time.sleep(random.randint(randIntFrom, randIntTo))

if bt > 0:
    buttons[bt].click()

# 少し待機
time.sleep(random.randint(randIntFrom, randIntTo))

# follow

for item in userIdList:
    print(item + "のフォローを開始")
    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))
    # driver.get("https://www.instagram.com/p/"+item+"/")
    driver.get(item)

    buttons.clear()
    buttons = driver.find_elements_by_tag_name("button")
    bt = -1
    for i in range(buttons.__len__()):
        # print("bttext:" + buttons[i].text)
        if buttons[i].text == "フォローする":
            bt = i
        elif buttons[i].text == "フォロー中":
            # すでにフォロー済み　→　ログ残して次のユーザーへ
            print("すでにフォロー済み")

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    if bt > -1:
        buttons[bt].click()
        # 成否確認　３秒まってテキストを確認 →ログを残す
        time.sleep(3)
        if buttons[bt].text == "フォロー中":
            print("フォロー成功")
        else:
            print("フォロー失敗")
        time.sleep(1)


# unfollow
for item in unfollowUserIdList:
    print(item + "のアンフォローを開始")

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))
    # driver.get("https://www.instagram.com/p/" + item + "/")
    driver.get(item)

    buttons.clear()
    buttons = driver.find_elements_by_tag_name("button")
    bt = -1
    for i in range(buttons.__len__()):
        # print("bttext:" + buttons[i].text)
        if buttons[i].text == "フォロー中":
            bt = i
        elif buttons[i].text == "フォローする":
            # すでにフォロー解除済み　→　ログ残して次のユーザーへ
            print("すでにアンフォロー済み")

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    if bt > -1:
        buttons[bt].click()

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    # フォローをやめる
    buttons.clear()
    buttons = driver.find_elements_by_tag_name("button")
    bt2 = -1
    for i in range(buttons.__len__()):
        print("bttext:" + buttons[i].text)
        if buttons[i].text == "フォローをやめる":
            bt2 = i

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    if bt2 > -1:
        print("before:" + buttons[bt].text)
        buttons[bt2].click()
        # 成否確認　３秒まってテキストを確認 →ログを残す
        time.sleep(3)
        print("after:" + buttons[bt].text)
        if buttons[bt].text == "フォローする":
            print("アンフォロー成功")
        else:
            print("アンフォロー失敗")
        time.sleep(1)

# いいね
for item in likeUserIdList:
    print(item + "のlikeを開始")

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))
    # driver.get("https://www.instagram.com/p/" + item + "/")
    driver.get(item)

    # /html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button
    try:
        target = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
    except common.exceptions.NoSuchElementException:
        print("NoSuchElementException - 不正なパスorページが削除")
        continue

    span = driver.find_element_by_class_name("glyphsSpriteHeart__outline__24__grey_9")
    if span.get_attribute("aria-label") == "いいね！":
        target.click()
        # 成否確認　３秒まってテキストを確認 →ログを残す
        time.sleep(3)
        span2 = driver.find_element_by_class_name("glyphsSpriteHeart__outline__24__grey_9")
        print("after:" + span2.get_attribute("aria-label"))
        if span2.get_attribute("aria-label") == "アクティビティーフィード":
            print("いいね成功")
        else:
            print("いいね失敗")
        time.sleep(1)

    else:
        print(span.get_attribute("aria-label"))
        print("すでにいいね済み")
        # log残して次の投稿へ

    time.sleep(random.randint(randIntFrom, randIntTo))
    # target.click()