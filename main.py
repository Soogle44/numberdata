import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import streamlit as st
from sqlalchemy import create_engine
import os

now = datetime.datetime.now()

if now.hour > 18 or now.hour < 3:

    # make columns
    columns = ["date"]

    # ag
    ag_list = ['sapporo', 'sendai', 'ueno', 'shibuya']
    for ag in ag_list:
        columns.append("man_ag_" + ag)
        columns.append("woman_ag_" + ag)

    # oriental lounge
    req = requests.get('https://oriental-lounge.com/')
    soup = BeautifulSoup(req.text, "html.parser")
    ori_html_list = soup.find_all("span", attrs={"class": "en"})

    for ori in ori_html_list:
        columns.append(
            "man_ori_" + ori.get_text().lower().replace(" ", ""))
        columns.append(
            "woman_ori_" + ori.get_text().lower().replace(" ", ""))

    # aisekiya
    ai_list = ["kabukicho", "ueno", "shibuya"]
    for ai in ai_list:
        columns.append("man_ai_" + ai)
        columns.append("woman_ai_" + ai)

    # get number
    row = [now]

    # ag
    ag_num_list = []
    for ag in ag_list:
        url = 'https://ag-ree.jp/restaurant/' + ag + '/'
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')
        temps = s.find_all("span", attrs={"class": "customer_num"})
        for i in range(len(temps)):
            ag_num_list.append(temps[i].get_text())

    row.extend(ag_num_list)

    # oriental lounge
    ori_man_num_html_list = soup.find_all("li", attrs={"class": "man"})
    ori_woman_num_html_list = soup.find_all("li", attrs={"class": "woman"})

    ori_num_list = []
    for i in range(len(ori_man_num_html_list)):
        ori_num_list.append(ori_man_num_html_list[i].get_text())
        ori_num_list.append(ori_woman_num_html_list[i].get_text())

    row.extend(ori_num_list)

    # aisekiya
    r = requests.get('https://aiseki-ya.com/')
    s = BeautifulSoup(r.text, 'html.parser')

    ai_man_num_list = s.find_all("div", attrs={"class": "cong_man"})
    ai_woman_num_list = s.find_all("div", attrs={"class": "cong_woman"})

    ai_num_list = []
    for i in range(len(ai_list)):
        ai_num_list.append(ai_man_num_list[i].find("span").get_text())
        ai_num_list.append(ai_woman_num_list[i].find("span").get_text())

    # make now row
    row.extend(ai_num_list)

    # make now df
    df = pd.DataFrame([row], columns=columns)

    # connect database
    engine = create_engine(
        os.environ['DATABASE'])

    # append data
    df.to_sql('data', con=engine, if_exists='append', index=False)
