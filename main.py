import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from sqlalchemy import create_engine
import os

now = datetime.datetime.now()

if now.hour > 18 or now.hour < 3:

    col = ['date',
           'man_ag_sapporo', 'woman_ag_sapporo',
           'man_ag_sendai', 'woman_ag_sendai',
           'man_ag_ueno', 'woman_ag_ueno',
           'man_ag_shibuya', 'woman_ag_shibuya',
           'man_ori_utsunomiya', 'woman_ori_utsunomiya',
           'man_ori_omiya', 'woman_ori_omiya',
           'man_ori_shinjuku', 'woman_ori_shinjuku',
           'man_ori_shibuyahonten', 'woman_ori_shibuyahonten',
           'man_ori_shibuyaekimae', 'woman_ori_shibuyaekimae',
           'man_ori_machida', 'woman_ori_machida',
           'man_ori_yokohama', 'woman_ori_yokohama',
           'man_ori_shizuoka', 'woman_ori_shizuoka',
           'man_ori_nagoyasakae', 'woman_ori_nagoyasakae',
           'man_ori_nagoyanishiki', 'woman_ori_nagoyanishiki',
           'man_ori_kyoto', 'woman_ori_kyoto',
           'man_ori_chayamachi', 'woman_ori_chayamachi',
           'man_ori_umeda', 'woman_ori_umeda',
           'man_ori_shinsaibashi', 'woman_ori_shinsaibashi',
           'man_ori_namba', 'woman_ori_namba',
           'man_ori_kobe', 'woman_ori_kobe',
           'man_ori_okayama', 'woman_ori_okayama',
           'man_ori_hiroshima', 'woman_ori_hiroshima',
           'man_ori_kokura', 'woman_ori_kokura',
           'man_ori_fukuoka', 'woman_ori_fukuoka',
           'man_ori_kumamoto', 'woman_ori_kumamoto',
           'man_ori_miyazaki', 'woman_ori_miyazaki',
           'man_ori_kagoshima', 'woman_ori_kagoshima',
           'man_ori_okinawa', 'woman_ori_okinawa',
           'man_ai_kabukicho', 'woman_ai_kabukicho',
           'man_ai_shinjuku', 'woman_ai_shinjuku',
           'man_ai_shibuya', 'woman_ai_shibuya',
           'man_ai_ikebukurohigashi', 'woman_ai_ikebukurohigashi',
           'man_ai_ikebukuronishi', 'woman_ai_ikebukuronishi',
           'man_ai_ueno', 'woman_ai_ueno',
           'man_ai_ebisu', 'woman_ai_ebisu',
           'man_ai_kinshicho', 'woman_ai_kinshicho',
           'man_ai_chiba', 'woman_ai_chiba',
           'man_ai_oomiya', 'woman_ai_oomiya',
           'man_ai_yokohama', 'woman_ai_yokohama',
           'man_ai_sendai', 'woman_ai_sendai',
           'man_ai_niigata', 'woman_ai_niigata',
           'man_ai_toyama', 'woman_ai_toyama',
           'man_ai_nagoya', 'woman_ai_nagoya',
           'man_ai_umeda', 'woman_ai_umeda',
           'man_ai_sannomiya', 'woman_ai_sannomiya',
           'man_ai_okayama', 'woman_ai_okayama',
           'man_ai_kokura', 'woman_ai_kokura',
           'man_ai_okinawa', 'woman_ai_okinawa']

    row = [now]

    # ag
    ag_list = ['sapporo', 'sendai', 'ueno', 'shibuya']

    ag_num_list = []
    for ag in ag_list:
        url = 'https://ag-ree.jp/restaurant/' + ag + '/'
        r_ag = requests.get(url)
        s_ag = BeautifulSoup(r_ag.text, 'html.parser')
        temps = s_ag.find_all("span", attrs={"class": "customer_num"})
        for i in range(len(temps)):
            ag_num_list.append(temps[i].get_text())

    row.extend(ag_num_list)

    # oriental lounge
    r_ori = requests.get('https://oriental-lounge.com/')
    s_ori = BeautifulSoup(r_ori.text, "html.parser")
    ori_man_num_html_list = s_ori.find_all("li", attrs={"class": "man"})
    ori_woman_num_html_list = s_ori.find_all("li", attrs={"class": "woman"})

    ori_num_list = []
    for i in range(len(ori_man_num_html_list)):
        ori_num_list.append(ori_man_num_html_list[i].get_text())
        ori_num_list.append(ori_woman_num_html_list[i].get_text())

    row.extend(ori_num_list)

    # aisekiya
    r_ai = requests.get('https://aiseki-ya.com/')
    s_ai = BeautifulSoup(r_ai.text, 'html.parser')
    ai_man_num_list = s_ai.find_all("div", attrs={"class": "cong_man"})
    ai_woman_num_list = s_ai.find_all("div", attrs={"class": "cong_woman"})
    ai_list = s_ai.find_all("div", attrs={"class": "shopname"})

    ai_num_list = []
    for i in range(len(ai_list)):
        ai_num_list.append(ai_man_num_list[i].find("span").get_text())
        ai_num_list.append(ai_woman_num_list[i].find("span").get_text())

    row.extend(ai_num_list)

    df = pd.DataFrame([row], columns=col)

    engine = create_engine(os.getenv('DATABASE'))
    df.to_sql('data2', con=engine, if_exists='append', index=False)
