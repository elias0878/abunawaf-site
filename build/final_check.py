import urllib.request, urllib.error, json, re, ssl
BASE="https://abunawaf.vercel.app"
ctx=ssl.create_default_context()
def get(u):
    req=urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0 Audit"})
    try:
        r=urllib.request.urlopen(req,timeout=25,context=ctx); return r.status,{k.lower():v for k,v in r.headers.items()},r.read()
    except urllib.error.HTTPError as e:
        return e.code,{k.lower():v for k,v in e.headers.items()},e.read()
    except Exception as e: return 0,{},str(e).encode()

print("═"*78); print("  فحص نهائي — abunawaf.vercel.app"); print("═"*78)
s,h,_=get(BASE+"/")
print("\n▸ رؤوس الأمان")
for k in ["strict-transport-security","x-content-type-options","x-frame-options","referrer-policy","permissions-policy","content-encoding","x-vercel-cache"]:
    v=h.get(k,"—"); print(f"   {'✓' if v!='—' else '✗'} {k}: {v[:60]}")

print("\n▸ الحالات الخاصة")
for p in ["/","/guides/","/guides","/index.html","/pages/tools.html","/nope-404"]:
    st,hh,b=get(BASE+p)
    loc=hh.get("location","")
    print(f"   {p:22} {st}{' → '+loc if loc else ''}")

print("\n▸ canonical + OG")
for p in ["/","/guides/","/services/anti-blackmail.html"]:
    st,_,b=get(BASE+p)
    can=re.search(rb'rel="canonical" href="([^"]+)"',b)
    og=re.search(rb'og:image" content="([^"]+)"',b)
    ogdim=re.findall(rb'og:image:(width|height)" content="(\d+)"',b)
    print(f"   {p:32} canon={can.group(1).decode() if can else '—'}")
    print(f"   {'':32} og={og.group(1).decode().split('/')[-1] if og else '—'} {[(a.decode(),c.decode()) for a,c in ogdim]}")

print("\n▸ Schema على الرئيسية")
st,_,b=get(BASE+"/")
for m in re.findall(rb'<script type="application/ld\+json">(.*?)</script>', b, re.S):
    j=json.loads(m)
    for n in j.get("@graph",[j]):
        t=n.get("@type"); t="+".join(t) if isinstance(t,list) else t
        print("   •",t)

print("\n▸ robots.txt")
st,_,b=get(BASE+"/robots.txt")
txt=b.decode()
print("   " + txt.strip().replace("\n","\n   ")[:420])

print("\n▸ sitemap")
import xml.etree.ElementTree as ET
st,_,b=get(BASE+"/sitemap.xml")
root=ET.fromstring(b); ns="{http://www.sitemaps.org/schemas/sitemap/0.9}"
locs=[u.text for u in root.iter(ns+"loc")]
print(f"   {len(locs)} عنواناً، آخر تحديث {root.find('.//'+ns+'lastmod').text}")
