from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'pGKUj4Gzjis5dmDJRiN8IRfff5J/MtdPfMZRIHSFgs+4F9IyyvBU/lqTQ0ELLd9pLmQwifvkzly3Pe9OXKtlFxFq8CMT2b0cj4bNCt360eNOMUyOW7vlBfeHsmcOT9vKLuBr6aMcVFjAX3pCzrR9nwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3028b906433d9020eee437dc1f1bb49c')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
