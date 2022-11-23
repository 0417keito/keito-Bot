from django.http import HttpResponse, HttpResponseForbidden
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage
from django.views.decorators.csrf import csrf_exempt
from . import models 
import MeCab

CHANNEL_SECRET = '569a985e6d60b9ccd2f1875373f5ef74'
CHANNEL_ACCESS_TOKEN = 'TQzX/x/r4fr0JV/T76oJ1o6jPiV1OBSCsVRWMrxViWSp6Odkja/uSWw60MfVSsrGVD711ebxv34aiyDfC4B720Nj733HamTm5DRVCRJki7jf/n/9L3cQN5BDRtdh9tKolcBHWv6gZ62edm28KQssfAdB04t89/1O/w1cDnyilFU='
handler = WebhookHandler(channel_secret=CHANNEL_SECRET)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

@csrf_exempt 
def callback(request):
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode('utf-8')
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print('Invalid signature.')
            return HttpResponseForbidden()
        return HttpResponse(status=200)

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='初めまして、過去問BOTです。\n探したい中学校名(略称も可)と年度(無くても可)を送信してください!\n例:開成中学校2022年'))  
    
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_text = event.message.text
    user = event.source.user_id
    tagger = MeCab.Tagger('-Owakati')
    tagger_text = tagger.parse(user_text)
    user_words = tagger_text.split(' ')
    target_lists = []
    first_word = user_words[0]
    end_word = user_words[-3]
    if end_word.isdecimal() == True:
        query_sets = models.School_exam.objects.filter(school_name__icontains=first_word).filter(school_name__icontains=end_word)
    else:
        query_sets = models.School_exam.objects.filter(school_name__icontains=first_word)
    query_list = list(query_sets.values()) 
    target_lists.append(query_list)
    
    for item in query_list:
        d = str(item['school_name'])  + '\n' +\
                    '国語:' + str(item['japanese']) + '\n' +\
                    '算数:' + str(item['math']) + '\n' +\
                    '理科:' + str(item['science']) + '\n' +\
                    '社会:' + str(item['society'])
        line_bot_api.push_message(
            user,TextSendMessage(text=d)
        )
