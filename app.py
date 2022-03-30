from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app=Flask(__name__)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

menu = {"大家鐵路$70":0, "大家鐵路$75":0, "太師傅$75":0, "太師傅$70":0, "太師傅$65":0, "正園A$60":0, "正園B$60":0, "正園羊肉$60":0, "吉樂米$65":0,
        "吉樂米$75":0, "吉樂米$85":0, "吉樂米素$65":0, "米寶$65":0, "米寶$75":0, "米寶素$65":0,  "彩鶴$50":0}
typesetting = ['', '', '', '', '', '\t', '\t', '', '', '', '', '', '\t', '\t', '', '\t']

botton = TemplateSendMessage(
    alt_text = "店家",
    template = CarouselTemplate( 
        columns = [
            CarouselColumn( 
                title = "米寶", 
                text = "請點選訂購內容", 
                actions = [
                    MessageAction( 
                        label = "米寶$65",
                        text = "米寶$65"
                    ),
                    MessageAction( 
                        label = "米寶$75",
                        text = "米寶$75"
                    ),
                    MessageAction(
                        label = "米寶素$65",
                        text = "米寶素$65"
                    )
                ]
            ),
            CarouselColumn( 
                title = "太師傅", 
                text = "請點選訂購內容", 
                actions = [
                    MessageAction( 
                        label = "太師傅$65",
                        text = "太師傅$65"
                    ),
                    MessageAction( 
                        label = "太師傅$70",
                        text = "太師傅$70"
                    ),
                    MessageAction(
                        label = "太師傅$75",
                        text = "太師傅$75"
                    )
                ]
            ),
            CarouselColumn( 
                title = "吉樂米", 
                text = "請點選訂購內容", 
                actions = [
                    MessageAction( 
                        label = "吉樂米$65",
                        text = "吉樂米$65"
                    ),
                    MessageAction( 
                        label = "吉樂米$75",
                        text = "吉樂米$75"
                    ),
                    MessageAction(
                        label = "吉樂米$85",
                        text = "吉樂米$85"
                    )
                ]
            ),
            CarouselColumn( 
                title = "吉樂米&彩鶴", 
                text = "請點選訂購內容", 
                actions = [
                    MessageAction( 
                        label = "吉樂米素$65",
                        text = "吉樂米素$65"
                    ),
                    MessageAction( 
                        label = "彩鶴$50",
                        text = "彩鶴$50"
                    ),
                    MessageAction( 
                        label = "排版用，不要亂點",
                        text = "aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1fdUpZVHZrY3VhRQ=="
                    )
                ]
            ),
            CarouselColumn( 
                title = "大家鐵路", 
                text ="請點選訂購內容", 
                actions =[
                    MessageAction( 
                        label = "大家鐵路$70",
                        text = "大家鐵路$70"
                    ),
                    MessageAction( 
                        label = "大家鐵路$75",
                        text = "大家鐵路$75"
                    ),
                    URIAction(
                        label = "排版用，不要亂點",
                        uri = "https://is.gd/5ws1Sr"
                    )
                ]
            ),
            CarouselColumn( 
                title = "正園", 
                text ="請點選訂購內容", 
                actions =[
                    MessageAction( 
                        label = "正園A$60",
                        text = "正園A$60"
                    ),
                    MessageAction( 
                        label = "正園B$60",
                        text = "正園B$60"
                    ),
                    MessageAction( 
                        label = "正園羊肉$60",
                        text = "正園羊肉$60"
                    )
                ]
            ),
            CarouselColumn( 
                title = "菜單", 
                text ="這裡一定要打不然會報錯雖然我也不知道為什麼", 
                actions =[
                    URIAction(
                        label='我會帶你到菜單的網站',
                        uri='https://webap1.kshs.kh.edu.tw/kshsSSO/publicWebAP/lunchList/index.aspx'
                    ),
                    URIAction(
                        label='我也會帶你到菜單的網站',
                        uri='https://webap1.kshs.kh.edu.tw/kshsSSO/publicWebAP/lunchList/index.aspx'
                    ),
                    URIAction(
                        label='我不會帶你到菜單的網站',
                        uri='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                    )
                ]
            )
        ]
    )
)

def order():
    # setups
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver.get("https://webap1.kshs.kh.edu.tw/kshsSSO/")

    # login
    waitforbrowser = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtID"))
    )
    stid = driver.find_element(By.ID, "ContentPlaceHolder1_txtID")
    stid.send_keys("[這裡填學號]")
    pw = driver.find_element(By.ID, "ContentPlaceHolder1_txtPassword")
    pw.send_keys("[這裡填密碼]")
    ckcd = driver.find_element(By.ID, "ContentPlaceHolder1_txtChkCode")
    ckcd.send_keys(driver.get_cookie("CheckCode")["value"])  # check code
    submit_1 = driver.find_element(By.ID, "ContentPlaceHolder1_lbLogin")
    submit_1.click()
    waitforbrowser = WebDriverWait(driver, 10).until(  # wait login
        EC.url_changes("https://webap1.kshs.kh.edu.tw/kshsSSO/")
    )
    driver.get("https://webap1.kshs.kh.edu.tw/kshsSSO/runAspx.aspx?url=fi9jb29wL2xpc3QuYXNweA==&progParent=c3R1ZGVudENvb3A=")

    # show menu
    waitforbrowser = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "合作社功能→→訂購午餐便當"))
    )
    bt1 = driver.find_element(By.LINK_TEXT, "合作社功能→→訂購午餐便當")
    bt1.click()
    waitforbrowser = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "訂購午餐便當"))
    )
    bt2 = driver.find_element(By.LINK_TEXT, "訂購午餐便當")
    bt2.click()
    waitforbrowser = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_btnLoad"))
    )
    showmenu = driver.find_element(By.ID, "ContentPlaceHolder1_btnLoad")
    showmenu.click()

    # order
    j=0
    waitforbrowser = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_gvLunch_ddlAmount_0"))
    )
    for i in menu:
        item = driver.find_element(By.ID, f'ContentPlaceHolder1_gvLunch_ddlAmount_{j}')
        Select(item).select_by_value(str(menu[i]))
        j+=1
    submit_2 = driver.find_element(By.ID, "ContentPlaceHolder1_btnUpdate")
    submit_2.click()
    waitforbrowser = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )
    driver.switch_to.alert.accept()
    driver.quit()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userID = event.source.user_id
    message = event.message.text
    # 訂餐訊息
    if message in menu:
        menu[message] += 1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "已收到您的訂單，您訂購的是" + message))
    # 截止&統計訊息
    elif message == "截止":
        if userID == "[my userid]":
            order()
            m = ""
            j = 0
            for i in menu:
                m += (i + '\t\t' + typesetting[j] + str(menu[i]) + '\n')
                menu[i] = 0
                j += 1
            m += "\n內訂已截止！記得繳錢！"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=m))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="還敢亂搞阿，以為我沒有修這個bug?"))
    # 菜單
    elif message[0] == '！' or message[0] == '!':
        line_bot_api.reply_message(event.reply_token, botton)
    # 刪除訂餐內容
    elif (message[0] == 'D' or message[0] == 'd') and (message[1] == 'E' or message[1] == 'e') and (message[2] == 'L' or message[2] == 'l'):
        if(message[3] == ' '):
            if message[4:] in menu:
                menu[message[4:]] -= 1
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "已刪除您 " + message[4:] + " 的訂單"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "無法辨識輸入的品項，請確認後再打一次"))
        else:
            if message[3:] in menu:
                menu[message[3:]] -= 1
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "已刪除您 " + message[3:] + " 的訂單"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "無法辨識輸入的品項，請確認後再打一次"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port=port)

