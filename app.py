from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
like_counter = defaultdict(int)

@app.route("/", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        echostr = request.args.get('echostr')
        return echostr or "hello"

    if request.method == "POST":
        xml_data = request.data
        root = ET.fromstring(xml_data)

        from_user = root.find("FromUserName").text
        to_user = root.find("ToUserName").text
        content = root.find("Content").text.strip()

        if content == "我喜欢你":
            today = datetime.now().strftime('%Y-%m-%d')
            like_counter[today] += 1
            count = like_counter[today]
            reply_content = f"你是今天第 {count} 个对我说“我喜欢你”的人 ❤️"
        else:
            reply_content = "我只对说“我喜欢你”的人有回应哟～"

        reply = f"""
        <xml>
          <ToUserName><![CDATA[{from_user}]]></ToUserName>
          <FromUserName><![CDATA[{to_user}]]></FromUserName>
          <CreateTime>{int(time.time())}</CreateTime>
          <MsgType><![CDATA[text]]></MsgType>
          <Content><![CDATA[{reply_content}]]></Content>
        </xml>
        """
        response = make_response(reply)
        response.content_type = "application/xml"
        return response
if __name__ == "__main__":
            app.run(host="0.0.0.0", port=10000)
