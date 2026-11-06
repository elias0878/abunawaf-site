# -*- coding: utf-8 -*-
"""إرسال خريطة الموقع إلى IndexNow (Bing / Yandex / Seznam)."""
import json
import re
import urllib.request

KEY = open("/home/user/site/tools/indexnow_key.txt", encoding="utf-8").read().strip()
HOST = "abunawaf.vercel.app"
sm = open("/home/user/site/sitemap.xml", encoding="utf-8").read()
urls = re.findall(r"<loc>([^<]+)</loc>", sm)

body = json.dumps({"host": HOST, "key": KEY,
                   "keyLocation": f"https://{HOST}/{KEY}.txt",
                   "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=25) as r:
        print(f"IndexNow → {r.status} ({len(urls)} عنواناً)")
except Exception as e:
    print("IndexNow فشل:", e)
