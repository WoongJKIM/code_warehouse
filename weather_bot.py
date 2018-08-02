#기상 특보 정보를 가져와 태풍/호우/대설 주의보/경보인 내역만 슬랙으로 알림

import pandas as pd
import numpy as np
import datetime as dt
import math
import json
from random import shuffle
import re

#페이지를 긁어오는 라이브러리
import requests
from bs4 import BeautifulSoup 
from urllib.request import urlopen

import os
import sys

#현재 파일 상대경로 받아오기 아이파이썬에서
#path=os.getcwd()

#현재 파일의 경로를 받아옵 크론잡에서 사용할 경우
path = os.path.realpath(os.path.dirname(__file__))

helper_path = os.path.join(path, 'helper/')
sys.path.append(helper_path)

#슬랙 매신져로 보내는 함수
from helper.send_tool import send_by_slack

def _get_weather_info_df():
    df = pd.DataFrame()

    idx = 1

    now_at = dt.datetime.now()

    while 1:
        url = "http://newsky2.kma.go.kr/service/WetherSpcnwsInfoService/SpecialNewsStatus?serviceKey=TOKEN_KEY&numOfRows={num_of_rows}&fromTmFc={now_at}&toTmFc={now_at}&pageNo={page_no}"
        print(url.format(num_of_rows = 1, now_at = now_at.strftime('%Y%m%d'), page_no = idx))
        res = requests.get(url.format(num_of_rows = 1, now_at = now_at.strftime('%Y%m%d%H%M'), page_no = idx))
        xml_soup = BeautifulSoup(res.content, 'xml')

        t6_xml = xml_soup.t6
        t6_tmFc = xml_soup.tmFc
        t6_tmEf = xml_soup.tmEf
        t6_totalCount = xml_soup.totalCount
        
        start_at = dt.datetime.strptime((t6_tmFc.contents)[0], '%Y%m%d%H%M')
        end_at = dt.datetime.strptime((t6_tmEf.contents)[0], '%Y%m%d%H%M')
        
        print(start_at, end_at)
        
        if (start_at - dt.timedelta(hours = 1) <= now_at) & (start_at + dt.timedelta(hours = 1) >= now_at):
            contents = (t6_xml.contents)[0]
            
            res = (None != re.search('(대설)', contents)) | (None != re.search('(호우)', contents)) | (None != re.search('(태풍)', contents))
            
            if res:
                df.loc[idx - 1, "contents"] = (t6_xml.contents)[0]
                df.loc[idx - 1, "start_at"] = start_at
                df.loc[idx - 1, "end_at"] = end_at
            else:
                pass

        if idx == int(((t6_totalCount).contents)[0]):
            break
        else:
            pass
        
    return df

def _slack_send_message(message):
    
    token = 'SLACK 채널 토큰'
    title = message
    sender = '기상 특보'
    
    send_by_slack.SendSlack.set_send_slack(token, title, sender)
    
class weatherBot():
    def __init__(self):
        pass
    
    def set_weather(self):
        _df = _get_weather_info_df()
        
        print(_df)
        
        if len(_df.index) > 0:
            for idx, row in _df.iterrows():
                message = '@channel \n발효 시간(' + row['end_at'].strftime('%Y-%m-%d %H:%M')  + ':00) : \n' + row['contents']
                _slack_send_message(message)
        else:
            pass
        
if __name__ == "__main__":
    weather_bot = weatherBot()
    weather_bot.set_weather()