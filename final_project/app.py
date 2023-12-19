import sys
import configparser
import csv
import numpy as np

from plot import plot
import imgur
import send_pic


from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
import os
# 切換到這個檔案的位置
os.chdir(os.getcwd())

#Config Parser
config = configparser.ConfigParser()
config.read(f'{os.getcwd()}/cofig.ini')

app = Flask(__name__)

channel_access_token = config['Line']['CHANNEL_ACCESS_TOKEN']
channel_secret = config['Line']['CHANNEL_SECRET']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

@app.route("/callback", methods=['POST'])
def callback():
    global user_id
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 解析 request body 的 JSON 格式內容
    body_json = request.get_json()
    # 從 JSON 中取得使用者 ID
    user_id = body_json['events'][0]['source']['userId']
    app.logger.info("User ID: " + user_id)
    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
user_responses = {}
num_questions = 17
fail_responds = {}
def start(user_id):
    user_responses[user_id] = {'counter': 1, 'responses': [''] * num_questions}
def fail_respond(user_id):
    if user_id not in fail_responds:
        fail_responds[user_id] = {'counter': 0}
    fail_responds[user_id]['counter'] += 1

def Initialize_user(user_id):
    if user_id in user_responses:
        del user_responses[user_id]  # Initialize user data

def update_csv(user_id, message_text):
    # 暫存至data.csv
    csv_file = 'data.csv'
    # 完整的結果存至data.csv
    csv_file1 = 'answer.csv'
    # Check if the CSV file exists; if not, create it with header
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id'] + [f'Q{i}' for i in range(1, num_questions + 1)])

    # Get the user's current question number
    current_question = user_responses[user_id]['counter']

    # Update the user's response for the current question
    user_responses[user_id]['responses'][current_question - 1] = message_text

    # Increment the counter for the next question
    user_responses[user_id]['counter'] += 1
    if user_responses[user_id]['counter'] != (num_questions+1):
        # Update the CSV file with user ID and message text
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id] + user_responses[user_id]['responses'])
    else:
        if not os.path.exists(csv_file1):
            with open(csv_file1, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['user_id'] + [f'Q{i}' for i in range(1, num_questions + 1)])
                writer.writerow([user_id] + user_responses[user_id]['responses'])
        else:
            with open(csv_file1, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_id] + user_responses[user_id]['responses'])

def load_questions():
    questions = {}
    with open('question.csv', mode='r',encoding='Big5') as file:
        reader = csv.reader(file)
        for row in reader:
            questions[row[0]] = row[1]
    return questions
q = load_questions()

# Within your message_text handler function
@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    global user_id
    user_id = event.source.user_id
    if event.message.text == '開始測驗':
        message_text = q['Q1']
        if user_id in fail_responds:
            del fail_responds[user_id]
        # 重新輸入清除資料
        Initialize_user(user_id)
        start(user_id)
    elif user_id in user_responses:
        if event.message.text in ["1", "2", "3", "4", "5"]:
            # Update the CSV file with user ID and message text
            update_csv(user_id, event.message.text)
            if user_responses[user_id]['counter'] == 18:
                plot()
                image_url = imgur.imgur_url(user_id)
                send_pic.send_image_message_to_line_bot(channel_access_token, user_id, image_url, image_url)
                # Stress suggestions
                total,max_category = plot()
                if total >= 75:
                    message_text = '您的壓力指數高,建議您可以:\n1. 尋求輔導室或老師協助 \n2. 適當的休閒放鬆以及運動 \n3. 與家人朋友談心 \n4. 適時放空靜坐淨空腦袋'
                elif total >= 50 and total<75:
                    message_text = '您的壓力指數偏高,建議您可以:\n1. 適當的休閒活動 \n2. 做好時間分配\n3. 適度運動'
                else:
                    message_text = '您的壓力指數正常,希望您能繼續保持'

                category = max_category
                for i in category:
                    match i:
                        case "學業":
                            a = np.random.randint(0, 2)
                            suggestion = ['\n制定明確的學習計畫，分段學習，減輕學業壓力。',
                                            '\n尋求教授協助，參與學習小組，共同解決難題。',
                                            '\n保持身心健康，合理安排休息時間，提升學習效率。'] 
                            message_text += "\n\n您的壓力來源主要源自學業: "+ suggestion[a]
                        case "友情":
                            a = np.random.randint(0, 2)
                            suggestion = ['\n與朋友坦誠溝通，表達感受，解釋期望，建立互相理解的溝通基礎。',
                                            '\n尋找共同興趣，參與有助於友誼發展的活動，加深感情。',
                                            '\n學會界定個人底線，避免過度迎合，保持對自己的真實性。']
                            message_text += '\n\n您的壓力來源主要源自友情: ' + suggestion[a]
                        case "愛情":
                            a = np.random.randint(0, 2)
                            suggestion = ['\n與伴侶坦誠溝通，討論期望和需求，確保共同理解。',
                                            '\n保持個人空間，維護獨立性，建立平衡愛情和個人生活。',
                                            '\n學會處理衝突，尋求共識，共同成長，建立穩固的愛情基礎。']
                            message_text += '\n\n您的壓力來源主要源自愛情: ' + suggestion[a]
                        case "家庭":
                            a = np.random.randint(0, 2)
                            suggestion = ['\n與家人坦誠溝通，表達感受，共同尋找解決方案，建立更健康的溝通模式。',
                                            '\n設定明確界線，保持個人空間，確保有時間和空間進行自我反思和照顧。',
                                            '\n考慮尋求專業心理輔導，以協助處理家庭壓力，建立更穩固的情緒基石。']
                            message_text += '\n\n您的壓力來源主要源自家庭: ' + suggestion[a]
                        case "個人":
                            a = np.random.randint(0, 2)
                            suggestion = ['\n專注自我照顧，培養健康習慣，包括充足睡眠和適度運動，提升身心健康。',
                                            '\n培養正向心態，接受自己，學會放手，不要過度自我要求。',
                                            '\n尋求心理支持，與朋友或專業輔導師分享感受，建立穩固的情緒支持系統。']
                            message_text += '\n\n您的壓力來源主要源自個人: ' + suggestion[a]
                Initialize_user(user_id)
            # next question
            else:
                message_text = q[f'Q{user_responses[user_id]["counter"]}']
        else:
            message_text = "請輸入數字1~5!\n"
            message_text += q[f'Q{user_responses[user_id]["counter"]}']
    else:
        fail_respond(user_id)
        if fail_responds[user_id]['counter'] == 1:
            message_text = '如果要開始壓力測試，請輸入"開始測驗"!'
        elif fail_responds[user_id]['counter'] == 2:
            message_text = '請確認你輸入的是"開始測驗"!'
        elif fail_responds[user_id]['counter'] == 3:
            message_text = '已經第三次了!請輸入"開始測驗"!\n求求你了!'
        else :
            message_text = "壓力指數無法測驗 請放下手機!"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=message_text)]
            )
        )

if __name__ == "__main__":
    app.run()