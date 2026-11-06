# -*- coding: utf-8 -*-
"""تدقيق شامل للموقع: HTML، SEO، الروابط، الأيقونات، البيانات المنظّمة."""
import glob
import json
import os
import re
import sys
from collections import Counter

ROOT = "/home/user/site"
D = "https://abunawaf.vercel.app"
SOCIAL_HOSTS = ["wa.me", "t.me", "snapchat.com", "instagram.com",
                "tiktok.com", "x.com", "facebook.com", "github.com", "tel:"]

errors, warnings, info = [], [], []


def E(f, m): errors.append(f"[{f}] {m}")
def W(f, m): warnings.append(f"[{f}] {m}")


SKIP = ("/tools/", "/.git/", "/pages/tools.html")   # tools.html صفحة تحويل noindex
files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
         if not any(x in f for x in SKIP)]

exist = {os.path.relpath(f, ROOT).replace("\\", "/") for f in files}
files_all = {os.path.relpath(f, ROOT).replace("\\", "/")
             for f in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True)
             if os.path.isfile(f) and "/.git/" not in f and "/tools/" not in f}
titles, descs, canonicals = Counter(), Counter(), Counter()

for f in sorted(files):
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    h = open(f, encoding="utf-8").read()

    # ── أساسيات ──
    if '<html lang="ar"' not in h: E(rel, "lang=\"ar\" مفقود")
    if 'dir="rtl"' not in h: E(rel, "dir=\"rtl\" مفقود")
    if h.count("<h1") != 1: E(rel, f"عدد H1 = {h.count('<h1')} (يجب 1)")
    if "<title>" not in h: E(rel, "title مفقود")
    else:
        t = re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip()
        titles[t] += 1
        if len(t) > 65: W(rel, f"title طويل ({len(t)} حرفاً)")
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    if not m: E(rel, "meta description مفقود")
    else:
        descs[m.group(1)] += 1
        if rel != "404.html" and not (110 <= len(m.group(1)) <= 165):
            W(rel, f"طول description = {len(m.group(1))}")
    c = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    if not c: E(rel, "canonical مفقود")
    else:
        canonicals[c.group(1)] += 1
        if not c.group(1).startswith(D): E(rel, f"canonical على نطاق غير معتمد: {c.group(1)}")
    if 'name="viewport"' not in h: E(rel, "viewport مفقود")
    if 'http-equiv="Content-Security-Policy"' in h: W(rel, "CSP مضمّن في HTML (يُدار من vercel.json)")

    # ── OG / Twitter ──
    for tag in ['property="og:title"', 'property="og:description"', 'property="og:image"',
                'property="og:url"', 'property="og:type"', 'name="twitter:card"']:
        if tag not in h: E(rel, f"وسم مفقود: {tag}")
    ogu = re.search(r'property="og:url" content="([^"]*)"', h)
    if ogu and canonicals and ogu.group(1) not in (c.group(1),) if c else False:
        pass
    ogi = re.search(r'property="og:image" content="([^"]*)"', h)
    if ogi:
        p = ogi.group(1).replace(D, ROOT)
        if p.startswith("http"):
            pass
        elif not os.path.exists(p): E(rel, f"og:image غير موجود: {ogi.group(1)}")

    # ── JSON-LD ──
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            data = json.loads(blk)
        except Exception as ex:
            E(rel, f"JSON-LD غير صالح: {ex}")
            continue
        for node in data.get("@graph", [data]):
            if node.get("@type") == "Organization" or "Organization" in str(node.get("@type")):
                cps = node.get("contactPoint") or []
                cps = cps if isinstance(cps, list) else [cps]
                for cp in cps:
                    if cp.get("contactOption") == "TollFree":
                        E(rel, "contactOption=TollFree على رقم جوال")
                sa = node.get("sameAs") or []
                if "https://twitter.com/ksa_hack2" in sa and "https://x.com/ksa_hack2" in sa:
                    W(rel, "sameAs يكرّر twitter.com و x.com")
            if node.get("@type") == "ItemList" and "SiteNavigationElement" in str(node):
                for it in node.get("itemListElement", []):
                    u = it.get("url", "").replace(D, "")
                    t = u.lstrip("/") or "index.html"
                    if t.endswith("/"): t += "index.html"
                    if t != "index.html" and t not in exist:
                        E(rel, f"تنقل يشير لصفحة غير موجودة: {u}")

    # ── أزرار التواصل ──
    blocks = re.findall(r'<div class="social-icons[^"]*">(.*?)</div>', h, re.S)
    if not blocks:
        E(rel, "لا توجد كتلة أزرار تواصل")
    else:
        total = 0
        for b in blocks:
            btns = re.findall(r'class="social-btn[^"]*"', b)
            total += len(btns)
            for host in SOCIAL_HOSTS:
                if host not in b:
                    E(rel, f"قناة مفقودة في كتلة التواصل: {host}")
            for a in re.findall(r"<a [^>]*>", b):
                if 'aria-label=' not in a and 'title=' not in a:
                    E(rel, "زر تواصل بلا aria-label")
                href = re.search(r'href="([^"]*)"', a)
                if href and href.group(1).startswith("http") and 'rel="noopener' not in a:
                    W(rel, "رابط خارجي بلا noopener")
        info.append(f"{rel}: {len(blocks)} كتلة / {total} زر")

    # ── واتساب ──
    if "wa.me/966572851032" not in h: E(rel, "رابط واتساب الرسمي مفقود")
    if "wa.me/966572851032" in h and "tel:+966572851032" not in h:
        W(rel, "زر الاتصال الهاتفي مفقود")

    # ── مكان الإقامة النائب ──
    if "VERIFICATION_CODE_HERE" in h: E(rel, "رمز تحقق وهمي متبقٍ")
    if "{D}" in h or "__D__" in h: E(rel, "علامة نائبة غير مُستبدلة")

    # ── الروابط الداخلية ──
    for href in re.findall(r'href="([^"]+)"', h):
        if href.startswith(("http://", "https://", "//", "mailto:", "tel:", "#", "javascript:", "data:")):
            continue
        clean = href.split("#")[0].split("?")[0]
        if not clean: continue
        if clean.startswith("/"):
            target = clean.lstrip("/")
        else:
            target = os.path.normpath(os.path.join(os.path.dirname(rel), clean)).replace("\\", "/")
        if target.endswith("/") or target == "." or target == "":
            target = (target.rstrip("/") + "/index.html").lstrip("/")
        if target not in exist and target not in files_all and target != "index.html":
            E(rel, f"رابط داخلي مكسور: {href} → {target}")

    # ── الصور ──
    for src in re.findall(r'<img [^>]*src="([^"]+)"', h):
        if src.startswith("http") or src.startswith("data:"): continue
        p = os.path.normpath(os.path.join(ROOT, src.lstrip("/")))
        if not os.path.exists(p): E(rel, f"صورة مفقودة: {src}")
        if "<img" in h and 'loading="lazy"' not in h and 'fetchpriority' not in h:
            W(rel, "img بلا loading=lazy")

    if rel != "pages/tools.html" and 'class="m-dock"' not in h:
        W(rel, "شريط التواصل السفلي مفقود")

# ── تكرارات ──
for name, cnt in (("title", titles), ("description", descs), ("canonical", canonicals)):
    for v, n in cnt.items():
        if n > 1: E("عام", f"{name} مكرر ×{n}: {v[:60]}")

# ── sitemap ──
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for u in locs:
    rel = u.replace(D, "").lstrip("/") or "index.html"
    if rel.endswith("/"): rel += "index.html"
    if rel not in exist: E("sitemap", f"عنوان لصفحة غير موجودة: {u}")
for f in exist:
    if f == "404.html" or f.startswith("pages/tools"): continue
    u = D + "/" + ("" if f == "index.html" else f)
    if f.endswith("/index.html"): u = D + "/" + f[:-10]
    if u not in locs: W("sitemap", f"صفحة غير مُدرجة: {f}")

# ── robots + feed ──
rb = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if f"Sitemap: {D}/sitemap.xml" not in rb: E("robots", "سطر Sitemap مفقود/خطأ")
if "feed.xml" not in open(os.path.join(ROOT, "index.html"), encoding="utf-8").read():
    W("index", "feed.xml غير معلن في <head>")

# ── vercel.json ──
vj = json.load(open(os.path.join(ROOT, "vercel.json"), encoding="utf-8"))
allkeys = {x["key"] for hh in vj["headers"] for x in hh["headers"]}
for need in ("Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options",
             "Referrer-Policy", "Permissions-Policy", "Content-Security-Policy", "X-Robots-Tag"):
    if need not in allkeys: E("vercel.json", f"ترويسة أمنية مفقودة: {need}")

# ── تقرير ──
print("=" * 74)
print(f"  تدقيق الموقع — {len(files)} صفحة")
print("=" * 74)
if errors:
    print(f"\n❌ أخطاء ({len(errors)}):")
    for e in errors: print("   ", e)
if warnings:
    print(f"\n⚠️  تحذيرات ({len(warnings)}):")
    for w in warnings: print("   ", w)
if not errors and not warnings:
    print("\n✅ لا أخطاء ولا تحذيرات")
print(f"\nنتيجة: {len(errors)} خطأ / {len(warnings)} تحذير / {len(files)} صفحة")
sys.exit(1 if errors else 0)
