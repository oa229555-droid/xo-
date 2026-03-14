# kill.py
import os
import requests
import json
import time
import google.generativeai as genai
from bs4 import BeautifulSoup

print("KILL START")

KEY = "AIzaSyD9eDKDNlYHTtvGMv9u6_TP3-9tKZ63SMk"
genai.configure(api_key=KEY)
model = genai.GenerativeModel('gemini-pro')

w = ['سكس', 'porn', 'xxx', 'رقص', 'اغراء', 'عاريات', 'nude', 'adult', '18+']
t = []

for x in w[:2]:
    try:
        r = requests.get(f"https://www.google.com/search?q={x}", timeout=5)
        s = BeautifulSoup(r.text, 'html.parser')
        for a in s.find_all('a'):
            h = a.get('href')
            if h and 'http' in h:
                u = h.split('&')[0].replace('/url?q=', '')
                if u not in t:
                    t.append(u)
                    print(f"+ {u}")
    except:
        continue

print(f"found {len(t)}")

for u in t[:5]:
    try:
        r = requests.get(u, timeout=5)
        s = BeautifulSoup(r.text, 'html.parser')
        text = s.get_text()[:2000]
        
        p = f"{u}\n{text}\n\nporn? yes/no json only: {{\"porn\":true/false,\"%\":0-100}}"
        res = model.generate_content(p)
        
        try:
            j = json.loads(res.text.replace('```json','').replace('```',''))
            if j.get('porn') and j.get('%',0) > 70:
                print(f"!!! PORN: {u}")
                with open('porn.txt','a') as f:
                    f.write(f"{u}\n")
        except:
            continue
        time.sleep(2)
    except:
        continue

print("KILL END")
