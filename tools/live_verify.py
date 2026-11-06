# -*- coding: utf-8 -*-
"""تحقّق شامل من النسخة المنشورة على Vercel."""
import json
import re
import ssl
import sys
import urllib.request

D = "https://abunawaf.vercel.app"
UA = {"User-Agent": "Mozilla/5.0 (compatible; abunawaf-check/1.0)"}
ok, bad = [], []


def get(path, method="GET"):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(D + path, headers=UA, method=method)
    try:
        with opener.open(req, timeout=25) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, {}, str(e)


# ── 1) الصفحات ──
sm = get("/sitemap.xml")[2]
urls = re.findall(r"<loc>([^<]+)</loc>", sm)
paths = [u.replace(D, "") or "/" for u in urls]
paths += ["/404.html", "/pages/tools.html", "/llms.txt", "/feed.xml",
          "/robots.txt", "/manifest.json", "/humans.txt",
          "/.well-known/security.txt"]

print("── حالة الصفحات " + "─" * 40)
for p in paths:
    st, hd, body = get(p)
    ct = hd.get("Content-Type") or hd.get("content-type", "")
    flag = "✓" if st in (200, 308) else "✗"
    if st not in (200, 308):
        bad.append(f"{p} → {st}")
    print(f"  {flag} {p:<52} {st}  {ct.split(';')[0]:<28} {len(body):>7,}b")
    if p == "/":
        for need in ["socialbar", "social-top", "social-card", "m-dock", "wa.me/966572851032", "terms-section" if False else "faq"]:
            if need in body:
                ok.append(f"index يحتوي {need}")
            else:
                bad.append(f"index يفتقد {need}")
    if st == 200 and p.endswith((".html", "/")) and p not in ("/404.html", "/pages/tools.html"):
        n = len(re.findall(r'class="social-btn', body))
        if n < 20:
            bad.append(f"{p}: عدد أزرار التواصل {n} < 20")
        if 'canonical" href="' + D not in body:
            bad.append(f"{p}: canonical ليس على النطاق المعتمد")

# ── 2) الترويسات ──
print("\n── الترويسات الأمنية " + "─" * 35)
st, hd, _ = get("/")
hl = {k.lower(): v for k, v in hd.items()}
checks = {
    "strict-transport-security": "max-age",
    "content-security-policy": "default-src",
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN",
    "referrer-policy": "strict-origin",
    "permissions-policy": "geolocation",
    "x-robots-tag": "index",
    "x-vercel-cache": "",
}
for k, v in checks.items():
    val = hl.get(k, "")
    hit = bool(val) and (not v or re.search(v, val))
    print(f"  {'✓' if hit else '✗'} {k}: {(val or '—')[:78]}")
    if not hit:
        bad.append(f"ترويسة {k} مفقودة/خطأ")

# ── 3) robots + feed + llms ──
print("\n── ملفات المحركات " + "─" * 38)
st, _, rb = get("/robots.txt")
print(f"  {'✓' if f'Sitemap: {D}/sitemap.xml' in rb else '✗'} robots.txt يحمل خريطة الموقع")
if f"Sitemap: {D}/sitemap.xml" not in rb:
    bad.append("robots.txt بلا Sitemap")
if "GPTBot" not in rb:
    bad.append("robots.txt لا يسمح لروبوتات AI")
print(f"  ✓ robots: {len(re.findall(r'User-agent:', rb))} وكيلاً")

st, hd, feed = get("/feed.xml")
print(f"  {'✓' if st == 200 and '<item>' in feed else '✗'} feed.xml ({feed.count('<item>')} عنصراً)")
if st != 200:
    bad.append("feed.xml لا يعمل")

st, _, llms = get("/llms.txt")
print(f"  {'✓' if st == 200 and 'الصفحات الأساسية' in llms else '✗'} llms.txt ({len(llms)} حرفاً)")

st, _, mf = get("/manifest.json")
try:
    m = json.loads(mf)
    print(f"  ✓ manifest.json — {len(m.get('shortcuts', []))} اختصاراً، start_url={m.get('start_url')}")
except Exception:
    bad.append("manifest.json غير صالح")

# ── 4) schema على الرئيسية ──
st, _, home = get("/")
gr = re.search(r'<script type="application/ld\+json">(.*?)</script>', home, re.S)
g = json.loads(gr.group(1))["@graph"]
types = ["+".join(x["@type"]) if isinstance(x["@type"], list) else x["@type"] for x in g]
print("\n── البيانات المنظّمة " + "─" * 37)
print("  ", " · ".join(types))
for need in ("Organization", "WebSite", "WebPage", "FAQPage", "Person", "ItemList"):
    if need not in types:
        bad.append(f"schema: {need} مفقود")

# ── 5) مؤشرات SEO ──
print("\n── مؤشرات SEO " + "─" * 43)
print(f"  ✓ صفحات في خريطة الموقع: {len(urls)}")
if 'GOOGLE_VERIFICATION_CODE_HERE' in home:
    bad.append("رمز تحقق وهمي ما زال موجوداً")
else:
    print("  ✓ لا رموز تحقق وهمية")
if 'TollFree' in home:
    bad.append("contactOption=TollFree ما زال موجوداً")
else:
    print("  ✓ contactOption صحيح")
if home.count('x.com/ksa_hack2') and 'twitter.com/ksa_hack2' in home:
    bad.append("sameAs يكرّر twitter/x")
else:
    print("  ✓ sameAs بلا تكرار")

# ── 5ب) الضغط ──
import subprocess
ce = subprocess.run(["curl", "-sI", "-H", "Accept-Encoding: gzip, br", D + "/"],
                    capture_output=True, text=True).stdout.lower()
enc = "br" if "content-encoding: br" in ce else ("gzip" if "content-encoding: gzip" in ce else "")
print(f"  {'✓' if enc else '✗'} ضغط النقل: {enc or 'غير مفعّل'}")
if not enc:
    bad.append("لا يوجد ضغط نقل")

# ── 6) أداء ──
import time
t0 = time.time()
get("/")
print(f"\n  ⏱ زمن الاستجابة الكامل للرئيسية: {(time.time()-t0)*1000:.0f} ms")
print(f"  📦 حجم HTML الرئيسية: {len(home)/1024:.1f} KB")

print("\n" + "=" * 66)
if bad:
    print(f"❌ {len(bad)} مشكلة:")
    for b in bad:
        print("   -", b)
    sys.exit(1)
print(f"✅ التحقق الحي ناجح — {len(ok)} تأكيداً، لا مشاكل")
