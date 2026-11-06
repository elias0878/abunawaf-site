import asyncio
from playwright.async_api import async_playwright

CARDS = {
  "og-default": ("أبو نواف", "هكر أخلاقي سعودي", "استعادة الحسابات · مكافحة الابتزاز · حماية الخصوصية"),
  "og-services": ("خدماتنا", "الأمن السيبراني والاستجابة للحوادث", "استعادة الحسابات · OSINT · فحص أمني · تأمين"),
  "og-guides": ("أدلة وحلول", "محتوى تقني مجاني", "خطوات عملية موثّقة لحماية حساباتك"),
}
LOGO = "file:///home/user/site/assets/images/logo.jpg"

TMPL = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{font-family:'Tajawal',sans-serif;position:relative;
 background:linear-gradient(135deg,#0f2438 0%,#1a365d 55%,#2c5282 100%)}}
.glow{{position:absolute;width:820px;height:820px;border-radius:50%;
 background:radial-gradient(circle,rgba(214,178,86,.20) 0%,transparent 62%);top:-330px;right:-240px}}
.grid{{position:absolute;inset:0;opacity:.30;background-image:
 linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);
 background-size:60px 60px}}
.bar{{position:absolute;top:0;right:0;width:100%;height:8px;
 background:linear-gradient(90deg,#d6b256,#f0d68a,#d6b256)}}
.logo{{position:absolute;right:80px;top:170px;width:190px;height:190px;border-radius:26px;
 border:3px solid rgba(214,178,86,.55);box-shadow:0 22px 55px rgba(0,0,0,.45);object-fit:cover}}
.txt{{position:absolute;right:320px;left:80px;top:150px}}
.kicker{{display:inline-block;font-size:25px;font-weight:700;color:#d6b256;
 border:2px solid rgba(214,178,86,.5);border-radius:999px;padding:9px 26px;margin-bottom:26px}}
h1{{font-size:74px;font-weight:900;color:#fff;line-height:1.1;letter-spacing:-1.5px}}
p{{font-size:29px;color:rgba(255,255,255,.80);margin-top:22px;font-weight:700;line-height:1.55}}
.foot{{position:absolute;bottom:40px;right:80px;font-size:25px;font-weight:700;color:#d6b256;
 display:flex;align-items:center;gap:12px}}
.dot{{width:12px;height:12px;border-radius:50%;background:#48bb78;box-shadow:0 0 14px #48bb78}}
</style></head><body>
<div class="bar"></div><div class="grid"></div><div class="glow"></div>
<img class="logo" src="LOGO">
<div class="txt">
  <div class="kicker">{kicker}</div>
  <h1>{title}</h1>
  <p>{sub}</p>
</div>
<div class="foot"><span class="dot"></span>ant.xo.je</div>
</body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1200,"height":630})
        for name,(kicker,title,sub) in CARDS.items():
            html = TMPL.format(kicker=kicker, title=title, sub=sub).replace("LOGO", LOGO)
            open(f"/tmp/{name}.html","w",encoding="utf-8").write(html)
            await pg.goto(f"file:///tmp/{name}.html")
            await pg.wait_for_timeout(2000)
            await pg.screenshot(path=f"assets/images/{name}.jpg", type="jpeg", quality=90)
            print("made", name)
        await b.close()
asyncio.run(main())
