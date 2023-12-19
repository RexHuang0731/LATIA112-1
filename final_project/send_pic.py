import requests
import json

def send_image_message_to_line_bot(channel_access_token, user_id, original_image_url, preview_image_url):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'image',
                'originalContentUrl': original_image_url,
                'previewImageUrl': preview_image_url
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("圖片訊息已成功發送至 LINE Bot！")
    else:
        print(f"發送圖片訊息至 LINE Bot 時發生錯誤：{response.text}")