from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from contextlib import contextmanager
import time
import threading
import os

app = Flask(__name__)

###-------------------------------------------------------------------------------------
# 初始化 Flask app 和 SQLAlchemy
app = Flask(__name__)

DATABASE_URL_KEY =""
engine = create_engine("")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
##定義上下文管理器---------------------------------------------------
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###----------------------------------------------------------------------------
##資料庫建構
#咖啡參數
class CoffeePara(db.Model):
			__tablename__ ="Coffee_Parameter"
			user_id = db.Column(db.String(33), primary_key=True)
			beans= db.Column(db.Integer, nullable=False)
			water= db.Column(db.Integer, nullable=False)
			brew_times= db.Column(db.Integer, nullable=False)

#產地資料
class CoffeeNation(db.Model):
			__tablename__ ="Coffee_Nation"
			nation = db.Column(db.String(10), primary_key=True)
			continent = db.Column(db.String(5), nullable=False)
			description= db.Column(db.String(300), nullable=False)
                     

###-------------------------------------------------------------------------------------
# Channel access token 和 Channel secret環境變數設置----------------------------
line_bot_api = LineBotApi()
handler = WebhookHandler()


###-------------------------------------------------------------------------------------
##設置路由，測試伺服器是否正常運行，並確保只有來自 LINE 平台的合法請求才能觸發 Bot 的相應行為
@app.route('/')
def index():
    return 'LINE Bot is running!'

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
        abort(400)

    return 'OK'
###---------------------------------------------------------------------------------------------------------------
##flex放這裡

##flex參數
flex_parameter = FlexSendMessage(
    alt_text="請確認是否修改參數",
    contents={
  "type": "bubble",
  "direction": "ltr",
  "header": {
    "type": "box",
    "layout": "vertical",
    "backgroundColor": "#FFC600FF",
    "contents": [
      {
        "type": "text",
        "text": "確定要修改參數嗎？",
        "weight": "bold",
        "size": "sm",
        "color": "#000000FF",
        "align": "center",
        "contents": []
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "否",
          "data": "no"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "是",
          "data": "yes"
        }
      }
    ]
  }
}
)

#選洲
flex_continent = FlexSendMessage(
    alt_text="請輸入洲別",
  contents=
  {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "非洲",
                "label": "非洲"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "中美洲",
                "text": "中美洲"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "南美洲",
                "label": "南美洲"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "亞洲",
                "text": "亞洲"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "大洋洲",
                "label": "大洋洲"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "加勒比海",
                "text": "加勒比海"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        }
      ]
    }
  }
    )

##國家非洲
flex_africa = FlexSendMessage(
    alt_text="請輸入國家",
  contents=
  {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "衣索比亞",
                "label": "衣索比亞"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "肯亞",
                "text": "肯亞"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "葉門",
                "label": "葉門"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "象牙海岸",
                "text": "象牙海岸"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "坦尚尼亞",
                "label": "坦尚尼亞"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "辛巴威",
                "text": "辛巴威"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "馬拉威",
                "label": "馬拉威"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            }
          ]
        }
      ]
    }
    }
)

##國家亞洲
flex_asia = FlexSendMessage(
    alt_text="請輸入國家",
  contents={
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "印尼",
                "label": "印尼"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "越南",
                "text": "越南"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "印度",
                "label": "印度"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
          ]
        }
      ]
    }
  }
)

##國家中美洲
flex_midameri = FlexSendMessage(
    alt_text="請輸入國家",
  contents={
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "哥斯大黎加",
                "label": "哥斯大黎加"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "薩爾瓦多",
                "text": "薩爾瓦多"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "瓜地馬拉",
                "label": "瓜地馬拉"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "宏都拉斯",
                "text": "宏都拉斯"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "尼加拉瓜",
                "label": "尼加拉瓜"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "墨西哥",
                "text": "墨西哥"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "巴拿馬",
                "label": "巴拿馬"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            }
          ]
        }
      ]
    }
  }
)

##國家南美洲
flex_southameri = FlexSendMessage(
    alt_text="請輸入國家",
  contents={
          "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "巴西",
                "label": "巴西"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "哥倫比亞",
                "text": "哥倫比亞"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "祕魯",
                "label": "祕魯"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "厄瓜多爾",
                "text": "厄瓜多爾"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        }
      ]
    }
  }
)

##國家大洋洲
flex_ocean = FlexSendMessage(
    alt_text="請輸入國家",
  contents={
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "新幾內亞",
                "label": "新幾內亞"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": " 澳洲",
                "text": "澳洲"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "夏威夷",
                "label": "夏威夷"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            }
          ]
        }
      ]
    }
  }
)

##國家加勒比海
flex_carri = FlexSendMessage(
    alt_text="請輸入國家",
  contents= {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "產地介紹",
          "weight": "bold",
          "size": "xl",
          "color": "#876C5A"
        },
        {
          "type": "text",
          "text": "我想了解......",
          "size": "xs",
          "margin": "sm"
        },
        {
          "type": "separator",
          "margin": "lg"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "牙買加",
                "label": "牙買加"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "波多黎各",
                "text": "波多黎各"
              },
              "style": "primary",
              "height": "sm",
              "margin": "xxl",
              "color": "#797D62"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "text": "多明尼加",
                "label": "多明尼加"
              },
              "style": "primary",
              "height": "sm",
              "color": "#797D62"
            }
          ]
        }
      ]
    }
    }
    )

##是否以參數計時
flex_count = FlexSendMessage(
  alt_text="Yes Or No",
  contents={
   "type": "bubble",
  "body": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "是",
          "data": "yescount"
        },
        "color": "#BB5E00"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "否",
          "data": "nocount"
        },
        "color": "#BB5E00"
      }
    ],
    "backgroundColor": "#D9B3B3"
  },
  "styles": {
    "header": {
      "separator": False
    }
  }
  }
)

##Flex結束
##----------------------------------------------------------------------------------------------------------------------
##狀態初始化
user_state_dic={}
text_message=None

##----------------------------------------------------------------------------------------------------------------------------
##沖泡時間class
class BrewingProcess:
    def __init__(self, user_id):
        self._user_id = user_id
        self._bloom_time = 30           # 悶蒸時間, 秒
        self._total_pulsing = 3 * 60    # 總沖泡時間, 秒
        self.reset()

    def reset(self):
    #"""重置所有相關參數"""
        self._durations_pulse = []
        self._water_per_pulse = []
        self._total_ground = -1
        self._water_total = -1
        self._repeatCount = -1
        self._running = False

    def setData(self, water_total, total_ground, repeat_count):
    #"""設定沖泡參數"""
        self._water_total = float(water_total)
        self._total_ground = float(total_ground)
        self._repeatCount = int(repeat_count)
    #"""計算每次沖泡的水量與時間"""
        remain_time = self._total_pulsing - self._bloom_time
        remain_water = self._water_total - self._total_ground * 2
    #"""計算每次注水量與時間"""
        self.duration_per_pulse = remain_time // self._repeatCount
        self.water_per_pulse = remain_water // self._repeatCount

    def send_msg(self, message):
    #    """訊息處理"""
        line_bot_api.push_message(self._user_id, TextMessage(text=message))

    def calculate_pulses(self):
    #"""計算每次沖泡的水量與時間"""
        remain_time = self._total_pulsing - self._bloom_time
        remain_water = self._water_total - self._total_ground * 2

    # 設定悶蒸時間和水量
        self._durations_pulse = [self._bloom_time]
        self._water_per_pulse = [self._total_ground * 2]

    # 每次注水時間和水量
        for i in range(self._repeatCount):
            # 最後一次注水
            if i == self._repeatCount - 1:
                self._durations_pulse.append(remain_time)
                self._water_per_pulse.append(int(remain_water))
            else:
                self._durations_pulse.append(self.duration_per_pulse)
                self._water_per_pulse.append(int(self.water_per_pulse))

                # 更新剩餘時間和水量
                remain_time -= self.duration_per_pulse
                remain_water -= self.water_per_pulse
            
    def countdown_timer(self):
        #"""倒數計時器"""
        for idx, duration in enumerate(self._durations_pulse):
            water = self._water_per_pulse[idx]
            if idx == 0:
                msg = f"開始悶蒸{water}克"
            elif idx == len(self._durations_pulse)-1:
                msg = f"進行最後一次注水，{water}克，記得要在3分鐘以內流完唷！"
            else:
                msg = f"進行第{idx}次注水，{water}克。"
            
            self.send_msg(msg)

            while duration > 0:
                time.sleep(1)
                duration -= 1

        self.send_msg("沖泡完成。")
        self.reset()

    def start(self):
        #"""啟動沖泡流程"""
        if self._running:
            self.send_msg("已經在執行沖煮計時！")
            return
        self._running = True
        self.calculate_pulses()
        threading.Thread(target=self.countdown_timer).start()



##函數放置----------------------------------------------------------------------------------------------------------------------
##根據不同的postback訊息處理
def process_postback(event, data):
    # 處理 postback 的邏輯
    if data == "yes":
        line_bot_api.reply_message(event.reply_token, 
						TextSendMessage(text="""點選左下角的小鍵盤進入訊息框後，輸入沖煮咖啡的參數，格式如下，以空白分隔：
咖啡豆(g) 沖煮咖啡量(g) 注水次數(不含悶蒸)
例如：20 300 5
另外，為確保沖煮出來咖啡的品質，
50 >= 咖啡豆量 >= 10；
450>= 沖煮咖啡量 >= 120；
6>= 注水次數 >= 1

或輸入「取消」以離開參數輸入功能。"""
				)
				)
    
        user_state_dic[event.source.user_id]["state"] = "pending user parameter"
    ##no的話不用處理
    elif data == "no":
        line_bot_api.reply_message(event.reply_token, 
						TextSendMessage(text="如之後欲修改參數，重新點選圖文選單即可。"
				)
				)
        user_state_dic[event.source.user_id]["state"] = None

    elif data== "yescount":
        user_state_dic[event.source.user_id]["brew"].start()
    else:
        line_bot_api.reply_message(event.reply_token, 
						TextSendMessage(text="如需開始計時功能，重新點選圖文選單即可。"
				)
				)

###---------------------------------------------------------------------------------------------------------------
#裝飾器都放這裡
##以下是(flex message)postback的觸發器
@handler.add(PostbackEvent)  # 呼叫對 Postback 事件的處理
def handle_postback(event):
    postback_data = event.postback.data  # 提取postback的 data 值
    process_postback(event, postback_data)  # 將event 的值
###---------------------------------------------------------------------------------------------------------------
## 文字訊息處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    temp_para=None
    user_message = event.message.text  # 獲取用戶傳送的文字
    user_id = event.source.user_id
    if user_id not in user_state_dic.keys():
        user_state_dic[user_id]={"state":None}
        user_state = user_state_dic[user_id]["state"]

    user_state = user_state_dic[user_id]["state"]

##根據user_state做判斷-----------------------------------------------------------------------------
###若未屬於任何狀態下-----------------------------------------------------------------------------
    if user_state==None:
        
        ##使用者點選參數輸入-----------------------------------------------------------------------------
        if user_message =="參數輸入":
            with SessionLocal() as db:
                temp_para = db.query(CoffeePara).filter_by(user_id=event.source.user_id).first()
            if not temp_para:
                line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text="""點選左下角的小鍵盤進入訊息框後，輸入沖煮咖啡的參數，格式如下，以空白分隔：
咖啡豆(g) 沖煮咖啡量(g) 注水次數(不含悶蒸)
例如：20 300 5
另外，為確保沖煮出來咖啡的品質，
50 >= 咖啡豆量 >= 10 ；
450>= 沖煮咖啡量 >= 120；
6>= 注水次數 >= 1

或輸入「取消」以離開參數輸入功能。"""
                    )
                    )
                user_state_dic[user_id]["state"]="pending user parameter"

            ##呼叫flex message
            else:
                line_bot_api.reply_message(
                event.reply_token, 
                flex_parameter
                )

        ##使用者點選手沖計時-----------------------------------------------------------------------------
        if user_message =="手沖計時":
             with SessionLocal() as db:
                temp_count = db.query(CoffeePara).filter_by(user_id=event.source.user_id).first()
                if not temp_count:
                    line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text=f"您尚未輸入任何參數，請點選圖文選單的「參數輸入」以輸入手沖咖啡參數。"
                    ) 
                    )
                else:
                    ##判斷是否已將參數設為物件
                    if "brew" not in user_state_dic[user_id]:
                         user_state_dic[user_id]["brew"]=BrewingProcess(user_id)
                    
                    user_state_dic[user_id]["brew"].setData(water_total=temp_count.water, total_ground=temp_count.beans, repeat_count=temp_count.brew_times)

                    if temp_count.brew_times == 1:
                         line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text=f"""你先前輸入的參數為：以{temp_count.beans}g的豆量，沖煮{temp_count.water}g的咖啡液，共注水{temp_count.brew_times}次。
經系統計算過後，悶蒸後只進行一次注水{int(user_state_dic[user_id]["brew"].water_per_pulse)}克，是否要以此參數作為依據計時？"""
                        ) 
                        )
                    else:
                        line_bot_api.reply_message(
                        event.reply_token, 
                        TextSendMessage(text=f"""你先前輸入的參數為：以{temp_count.beans}g的豆量，沖煮{temp_count.water}g的咖啡液，共注水{temp_count.brew_times}次。
    經系統計算過後，每次注水量為{int(user_state_dic[user_id]["brew"].water_per_pulse)}克，間隔時間為{user_state_dic[user_id]["brew"].duration_per_pulse}秒，是否要以此參數作為依據計時？"""
                            ) 
                            )
                    line_bot_api.push_message(event.source.user_id, flex_count)


        ##使用者點選參數輸入-----------------------------------------------------------------------------
        if user_message == "產地介紹":
            line_bot_api.reply_message(
                event.reply_token, 
                flex_continent
                )
            user_state_dic[user_id]["state"]="pending_continent"
        
        if user_message == "參數介紹":

            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="""咖啡粉量：咖啡粉量與水的比例決定了咖啡的濃淡。一般來說，粉水比約為1:15至1:18，但可以根據個人喜好做調整。粉量越多，咖啡濃度越高，但過多會產生苦味。
                            
注水次數：注水次數會影響咖啡的萃取率。一般來說，多段的注水可以讓咖啡粉充分浸潤，萃取出更豐富的風味。本系統預設除最後一次注水外，每次注水的份量一樣。
                            
總沖煮咖啡量：總沖煮咖啡量與粉水比密切相關。決定了最終咖啡的濃度。
                            
總沖煮時間：沖煮時間過短，咖啡萃取不足，風味淡薄或容易有尖銳或極端的風味出現；時間過長，則容易產生過度萃取的苦味與澀味。本系統參考現職咖啡師與網路上建議的時間，將沖煮時間固定為三分鐘，並預設每次注水間的時間一樣。
                            
悶蒸：悶蒸讓咖啡粉充分吸水，有助於釋放二氧化碳，讓後續萃取更均勻。悶蒸時間一般為30秒左右，水量約為咖啡粉量的1.5至2倍。

參考資料：步昂咖啡【手沖入門】學會這六大步驟，新手也能享受美味手沖咖啡
https://reurl.cc/5DdOxy
"""
                    )
                    ) 
            

        if user_message == "功能說明":
            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="""輸入「參數輸入」或點擊圖文選單，以新增或修改你的咖啡沖煮參數。

輸入「手沖計時」或點擊圖文選單，開始進行沖煮計時。
悶蒸時間為30秒、總沖煮時間為3分鐘，以此標準以及你的沖煮參數，給予注水時間和份量的提醒。

輸入「產地介紹」或點擊圖文選單，以獲取各咖啡產地之資訊。
我們收錄三十幾個有產咖啡的國家介紹，可以更了解咖啡的淵源以及各產地的特色。

輸入「參數介紹」以了解各參數對手沖咖啡的影響，協助你調整參數。

輸入「功能介紹」或點擊圖文選單，可以再看一次此說明。
"""
                    )
                    )
        
##等待使用者輸入參數---------------------------------------------------------------------------------------------------------
    elif user_state == "pending user parameter":
        if user_message == "取消":
          line_bot_api.reply_message(event.reply_token, 
						TextSendMessage(text="如之後欲修改參數，重新點選圖文選單即可。"
				)
				)
          user_state_dic[user_id]["state"] = None
        else:
          try:
              parameter = event.message.text
              parameter = [int(i) for i in parameter.split()]
              ##判斷是否在合法範圍----------------------------------------------------------------------------
              if 50 >= parameter[0] >= 10 and 450>= parameter[1] >= 120 and 6>= parameter[2] >= 1:
                  with get_db() as db:
                      temp_para = db.query(CoffeePara).filter_by(user_id=event.source.user_id).first()
              ##判斷此次資料為修改或新增---------------------------------------------------------------------
              ###新增----------------------------------------------------------------------------------
                      if not temp_para:
                          ##創造session加入新row
                          new_para = CoffeePara(user_id=event.source.user_id, beans=parameter[0], water= parameter[1], brew_times=parameter[2])
                          db.add(new_para)
                          db.commit()
                          line_bot_api.reply_message(event.reply_token, 
                          TextSendMessage(text=f"""已新增您的沖煮參數：
  以{parameter[0]}g的豆量，沖煮{parameter[1]}g的咖啡液，共注水{parameter[2]}次。
  若需要修改，點選圖文選單重新輸入即可！"""
                              )
                              )
                          user_state_dic[user_id]["state"] = None
                  ###修改-------------------------------------------------------------------------------------
                      else:
                          temp_para.beans=parameter[0]
                          temp_para.water= parameter[1]
                          temp_para.brew_times=parameter[2]
                          db.commit()
                          line_bot_api.reply_message(event.reply_token, 
                          TextSendMessage(text=f"""已修改您的沖煮參數：
  以{parameter[0]}g的豆量，沖煮{parameter[1]}g的咖啡液，共注水{parameter[2]}次。"""
                      )
                      )
                          user_state_dic[user_id]["state"] = None
              ###若為非法數值---------------------------------------------------------------          
              else:
                  raise ValueError
              
          except (TypeError, ValueError, AttributeError):
              line_bot_api.reply_message(event.reply_token, 
          TextSendMessage(text="""請重新輸入正確資料。
  (50 >= 咖啡豆量 >= 10；
  450>= 沖煮咖啡量 >= 120；
  6>= 注水次數 >= 1)
  
  或輸入「取消」以離開參數輸入功能。"""
              )
              )
              

##等待輸入洲別------------------------------------------------------------------------------------------------------------------------------     
    elif user_state == "pending_continent":
        
        if user_message =="非洲":
            user_state_dic[user_id]["state"]="pending_nation"
            line_bot_api.reply_message(
                event.reply_token, 
                flex_africa
                )
			
        elif user_message =="亞洲":
            user_state_dic[user_id]["state"]="pending_nation"
            line_bot_api.reply_message(
                event.reply_token, 
                flex_asia
                )
            
        elif user_message =="中美洲":
            user_state_dic[user_id]["state"]="pending_nation"
            line_bot_api.reply_message(
                event.reply_token, 
                flex_midameri
                )

        elif user_message =="南美洲":
            user_state_dic[user_id]["state"]="pending_nation"
            line_bot_api.reply_message(
                event.reply_token, 
                flex_southameri
                )

        elif user_message =="大洋洲":
            user_state_dic[user_id]["state"]="pending_nation"
            line_bot_api.reply_message(
                event.reply_token, 
                flex_ocean
                )

        elif user_message =="加勒比海":
            user_state_dic[user_id]["state"]="pending_nation"
            line_bot_api.reply_message(
                event.reply_token, 
                flex_carri
                )
			
        elif user_message in ["南極洲", "北美洲", "歐洲"]:
            user_state_dic[user_id]["state"]=None
            line_bot_api.reply_message(
				event.reply_token, 
				TextSendMessage(text="系統未收錄該洲國家資料，或該洲國家無產咖啡。"
				) 
	            )
	            
        else:
            user_state_dic[user_id]["state"]=None
            line_bot_api.reply_message(
				event.reply_token, 
				TextSendMessage(text="洲名錯誤，請點擊按鈕或重新輸入。"
				) 
	            )

##等待輸入國家------------------------------------------------------------------------------------------------------------------------------     
    elif user_state == "pending_nation":
        temp_data=None
        with get_db() as db:
            temp_data = db.query(CoffeeNation).filter_by(nation=user_message).first()
            if temp_data:
                temp_description = temp_data.description
                user_state_dic[user_id]["state"]=None
                line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text=temp_description
                        ) 
                        )
            else:
                user_state_dic[user_id]["state"]=None
                line_bot_api.reply_message(
                        event.reply_token, 
                        TextSendMessage(text="國家名錯誤，或系統未收錄該國家資料，請點擊按鈕或重新輸入。"
                        ) 
                        )


###-------------------------------------------------------------------------------------------------------
## 確保程式碼只有在作為主程式執行時才會啟動應用程式。
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
