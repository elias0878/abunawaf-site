# -*- coding: utf-8 -*-
"""اختبار حقيقي للموقع في متصفح Chromium: أخطاء الكونسول، الروابط،
ظهور أزرار التواصل فوق الطية، والتفاعل مع زر المشاركة."""
import http.server
import os
import socketserver
import threading
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = "/home/user/site"
OUT = "/home/user/site/build"
import random as _r
PORT = _r.randint(8300, 8900)
import random
os.makedirs(OUT, exist_ok=True)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}"

PAGES = ["/", "/pages/services.html", "/pages/contact.html", "/pages/problems.html",
         "/pages/about.html", "/guides/", "/services/anti-blackmail.html",
         "/services/security-audit.html", "/guides/two-factor-authentication-guide.html",
         "/pages/privacy.html", "/pages/terms.html"]

results, problems = [], []

with sync_playwright() as p:
    b = p.chromium.launch()
    for device, vp, ua in [
        ("desktop", {"width": 1440, "height": 900}, None),
        ("mobile", {"width": 390, "height": 844},
         "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
         "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"),
    ]:
        ctx = b.new_context(viewport=vp, user_agent=ua, locale="ar-SA",
                            device_scale_factor=2 if device == "mobile" else 1)
        for path in PAGES:
            page = ctx.new_page()
            errs, failed = [], []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(f"JS: {e}"))
            page.on("requestfailed",
                    lambda r: failed.append(r.url) if "fonts.g" not in r.url else None)
            try:
                page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(700)
            except Exception as ex:
                problems.append(f"{device} {path}: تعذّر التحميل — {ex}")
                page.close()
                continue

            # ── أزرار التواصل: العدد + الظهور فوق الطية ──
            data = page.evaluate("""() => {
                const vh = window.innerHeight;
                const btns = [...document.querySelectorAll('.social-btn')];
                const visible = btns.filter(b => {
                    const r = b.getBoundingClientRect();
                    const st = getComputedStyle(b);
                    return r.width > 0 && r.height > 0 && st.visibility !== 'hidden'
                           && r.top >= 0 && r.top < vh;
                });
                const bar = document.querySelector('.social-icons');
                const br = bar ? bar.getBoundingClientRect() : null;
                return {
                    total: btns.length,
                    aboveFold: visible.length,
                    barTop: br ? Math.round(br.top) : null,
                    barInFold: br ? (br.top >= 0 && br.bottom <= vh) : false,
                    dock: !!document.querySelector('.m-dock:not([hidden])'),
                    dockVisible: (() => {
                        const d = document.querySelector('.m-dock');
                        return d ? getComputedStyle(d).display !== 'none' : false;
                    })(),
                    h1: document.querySelectorAll('h1').length,
                    overflowX: (() => {
                        const de = document.documentElement;
                        const oy = de.style.overflowY;
                        de.style.overflowY = 'hidden';   // استثناء شريط التمرير الرأسي في RTL
                        const over = de.scrollWidth > de.clientWidth + 1;
                        de.style.overflowY = oy;
                        return over;
                    })(),
                    title: document.title.length,
                };
            }""")

            r = dict(device=device, path=path, **data, console=errs[:3], failed=failed[:3])
            results.append(r)
            if data["aboveFold"] < 9:
                problems.append(f"{device} {path}: أزرار فوق الطية = {data['aboveFold']} (المطلوب 9)")
            if data["overflowX"]:
                problems.append(f"{device} {path}: تمرير أفقي زائد")
            if errs:
                problems.append(f"{device} {path}: أخطاء كونسول {errs[:2]}")
            if failed:
                problems.append(f"{device} {path}: طلبات فاشلة {failed[:2]}")
            if device == "mobile" and not data["dockVisible"]:
                problems.append(f"{device} {path}: شريط التواصل السفلي غير ظاهر")

            if path in ("/", "/pages/contact.html"):
                page.screenshot(path=f"{OUT}/shot-{device}{path.replace('/', '-')}.png",
                                full_page=False)
            page.close()
        ctx.close()

    # ── اختبار التفاعل: زر المشاركة + فتح رابط خارجي ──
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, permissions=[])
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="domcontentloaded")
    page.evaluate("window.__copied=false; navigator.clipboard.writeText=()=>{window.__copied=true;return Promise.resolve()}")
    page.click(".social-share")
    page.wait_for_timeout(300)
    copied = page.evaluate("window.__copied")
    print(("✓" if copied else "✗"), "زر المشاركة ينسخ الرابط")

    # كل روابط التواصل: هل لها href صحيح وغير مكرر؟
    hrefs = page.eval_on_selector_all(".social-btn[href]", "els => els.map(e => e.getAttribute('href'))")
    uniq = sorted(set(hrefs))
    print(f"✓ {len(hrefs)} زر تواصل، {len(uniq)} وجهة فريدة")
    for u in uniq:
        print("   ", u)

    # عدّ الأيقونات الظاهرة مع الشاشة الأولى (بصرياً)
    vis = page.evaluate("""() => {
        const vh = innerHeight;
        return [...document.querySelectorAll('.social-btn')]
            .filter(b => { const r = b.getBoundingClientRect(); return r.top >= 0 && r.bottom <= vh; }).length;
    }""")
    print(f"✓ {vis} أيقونة تواصل داخل الشاشة الأولى (1440×900)")

    # بطاقات الحسابات الرسمية (تصميم الموقع الأصلي)
    cards = page.eval_on_selector_all(".social-card", "els => els.length")
    print(f"✓ {cards} بطاقة حسابات رسمية في قسم «حسابات أبو نواف الرسمية»")
    page.evaluate("document.querySelector('#social-top')?.scrollIntoView()")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/shot-channels.png")
    ctx.close()
    b.close()

srv.shutdown()

print("\n" + "=" * 70)
print("  نتائج الاختبار في المتصفح")
print("=" * 70)
print(f"{'الجهاز':<9}{'الصفحة':<46}{'فوق الطية':>10}{'إجمالي':>8}")
for r in results:
    print(f"{r['device']:<9}{r['path']:<46}{r['aboveFold']:>10}{r['total']:>8}")
print()
if problems:
    print(f"❌ مشاكل ({len(problems)}):")
    for x in problems:
        print("   -", x)
    sys.exit(1)
print(f"✅ لا مشاكل — {len(results)} اختبار صفحة/جهاز ناجح")
