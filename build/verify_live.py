import urllib.request, json, re, ssl, sys
BASE="https://abunawaf.vercel.app"
ctx=ssl.create_default_context()
def get(url, method="GET"):
    req=urllib.request.Request(url, method=method, headers={"User-Agent":"Mozilla/5.0 (compatible; SEO-Audit)"})
    try:
        r=urllib.request.urlopen(req, timeout=25, context=ctx)
        return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:
        return 0, {}, str(e).encode()

import xml.etree.ElementTree as ET
s,h,b=get(BASE+"/sitemap.xml") if False else get(BASE+"/sitemap.xml")
print(f"sitemap.xml   HTTP {s}  {h.get('Content-Type')}  {len(b)}B  enc={h.get('Content-Encoding')}")
urls=[u.text for u in ET.fromstring(b).findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
print(f"  → {len(urls)} عنواناً\n")

ok=fail=0
for u in urls:
    path=u.replace("https://ant.xo.je","")
    st,hd,body=get(BASE+path)
    title=re.search(rb"<title>(.*?)</title>", body, re.S)
    t=title.group(1).decode("utf-8") if title else "—"
    h1=len(re.findall(rb"<h1", body))
    can=re.search(rb'rel="canonical" href="([^"]+)"', body)
    c=can.group(1).decode() if can else "—"
    status="✓" if st==200 and h1==1 else "✗"
    if status=="✓": ok+=1
    else: fail+=1
    print(f"{status} {st} {path:44} h1={h1} canon={'ant.xo.je' if 'ant.xo.je' in c else c[:30]:10} | {t[:52]}")
print(f"\nصفحات سليمة: {ok}/{len(urls)}  فاشلة: {fail}")

print("\n=== حالات خاصة ===")
for path,expect in [("/does-not-exist-xyz","404"),("/pages/tools.html","redirect/301"),
                    ("/index.html","301→/"),("/guides","301→/guides/")]:
    st,hd,b2=get(BASE+path)
    print(f"  {path:28} → HTTP {st} {('→ '+hd.get('Location','')) if hd.get('Location') else ''}  (متوقع {expect})")

print("\n=== رؤوس الأمان ===")
st,hd,_=get(BASE+"/")
for k in ["strict-transport-security","x-content-type-options","x-frame-options","referrer-policy","content-encoding","cache-control","server"]:
    print(f"  {k}: {hd.get(k,'—')}")

print("\n=== أصول ===")
for a in ["/css/main.css","/css/extra.css","/js/main.js","/assets/images/og-default.jpg",
          "/assets/images/icon-512.png","/robots.txt","/manifest.json","/favicon.ico","/.well-known/security.txt"]:
    st,hd,b3=get(BASE+a)
    print(f"  {a:34} {st} {hd.get('Content-Type','—')[:34]:34} {len(b3)}B cache={hd.get('Cache-Control','—')[:28]}")
