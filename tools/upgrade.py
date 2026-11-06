# -*- coding: utf-8 -*-
"""
ترقية الموقع: أزرار التواصل الكاملة + تحسين SEO متقدّم.
يُشغَّل مرة واحدة ويعالج كل ملفات HTML.
"""
import json
import os
import re
import glob

ROOT = "/home/user/site"

# النطاق الأساسي (canonical / sitemap / schema) — يُغيَّر بأمر واحد عبر tools/set_domain.py
DOMAIN = "https://abunawaf.vercel.app"

from icons import WA, TG, SNAP, IG, TT, X, FB, GH, PHONE, SHARE

# ─────────────────────────── قنوات التواصل (مصدر واحد) ───────────────────────────
WA_NUMBER = "966572851032"
WA_DISPLAY = "+966 57 285 1032"
WA_TEXT = "السلام عليكم، تواصلت معكم من موقع أبو نواف."

CHANNELS = [
    dict(key="whatsapp", name="واتساب", handle="+966 57 285 1032",
         url=f"https://wa.me/{WA_NUMBER}?text={WA_TEXT}", brand="#25D366",
         icon=WA, rel_me=False, ltr=True,
         note="الأسرع للرد — متاح طوال أوقات العمل"),
    dict(key="telegram", name="تيليجرام", handle="@KSA_hack01",
         url="https://t.me/KSA_hack01", brand="#229ED9",
         icon=TG, rel_me=True,
         note="القناة الرئيسية للأسئلة التقنية"),
    dict(key="snapchat", name="سناب شات", handle="ant_ceh",
         url="https://www.snapchat.com/add/ant_ceh", brand="#FFFC00",
         icon=SNAP, rel_me=True, dark=True,
         note="تحديثات ومحتوى قصير"),
    dict(key="instagram", name="إنستقرام", handle="@ksa_hack01",
         url="https://www.instagram.com/ksa_hack01", brand="#E1306C",
         icon=IG, rel_me=True,
         note="محتوى توعوي وحالات عملية"),
    dict(key="tiktok", name="تيك توك", handle="@ksa_hack01",
         url="https://www.tiktok.com/@ksa_hack01", brand="#010101",
         icon=TT, rel_me=True,
         note="مقاطع قصيرة في الأمن السيبراني"),
    dict(key="x", name="إكس (تويتر)", handle="@ksa_hack2",
         url="https://x.com/ksa_hack2", brand="#000000",
         icon=X, rel_me=True,
         note="تنبيهات أمنية عاجلة"),
    dict(key="facebook", name="فيسبوك", handle="أبو نواف", 
         url="https://www.facebook.com/profile.php?id=61554330014413", brand="#1877F2",
         icon=FB, rel_me=True,
         note="الصفحة الرسمية"),
    dict(key="github", name="GitHub", handle="elias0878",
         url="https://github.com/elias0878", brand="#24292F",
         icon=GH, rel_me=True, ltr=True,
         note="أدوات ومشاريع مفتوحة المصدر"),
    dict(key="phone", name="اتصال هاتفي", handle=WA_DISPLAY,
         url=f"tel:+{WA_NUMBER}", brand="#0F2438",
         icon=PHONE, rel_me=False, ltr=True,
         note="للحالات الطارئة داخل السعودية"),
]


def _rel(ch):
    parts = ["noopener", "noreferrer"]
    if ch["rel_me"]:
        parts.append("me")
    return " ".join(parts)


def icon_btn(ch, size=22):
    """زر أيقونة واحد."""
    label = f'{ch["name"]} — القناة الرسمية لفريق أبو نواف'
    title = ch["name"]
    handle = f' <bdi dir="ltr">{ch["handle"]}</bdi>' if ch.get("ltr") else f' {ch["handle"]}'
    return (f'<a class="social-btn" style="--brand:{ch["brand"]}" href="{ch["url"]}" '
            f'target="_blank" rel="{_rel(ch)}" aria-label="{label}" title="{title}">'
            f'<svg viewBox="0 0 24 24" fill="none" width="{size}" height="{size}" aria-hidden="true">'
            f'{ch["icon"]}</svg></a>')


def share_btn(size=22):
    return ('<button type="button" class="social-btn social-share" data-share '
            'style="--brand:#d6b256" aria-label="مشاركة هذه الصفحة" title="مشاركة الصفحة">'
            f'<svg viewBox="0 0 24 24" fill="none" width="{size}" height="{size}" aria-hidden="true">'
            f'{SHARE}</svg></button>')


def social_icons(size=22):
    return ('<div class="social-icons">'
            + "".join(icon_btn(c, size) for c in CHANNELS)
            + share_btn(size)
            + "</div>")


def channel_cards():
    """بطاقات القنوات الكاملة — قسم في الواجهة."""
    cards = []
    for ch in CHANNELS:
        handle = f'<bdi dir="ltr">{ch["handle"]}</bdi>' if ch.get("ltr") else ch["handle"]
        cards.append(f'''<a class="ch-card" href="{ch["url"]}" target="_blank" rel="{_rel(ch)}" style="--brand:{ch["brand"]}" aria-label="{ch["name"]} — {ch["handle"]}">
                <span class="ch-icon"><svg viewBox="0 0 24 24" fill="none" width="24" height="24" aria-hidden="true">{ch["icon"]}</svg></span>
                <span class="ch-body">
                    <span class="ch-name">{ch["name"]}</span>
                    <span class="ch-handle">{handle}</span>
                    <span class="ch-note">{ch["note"]}</span>
                </span>
            </a>''')
    return ('<div class="ch-grid">\n' + "\n".join(cards) + "\n</div>")


# ─────────────────────────── تعديل ملفات HTML ───────────────────────────
def fix_social_blocks(html):
    """استبدال كل كتل social-icons بالقائمة الكاملة، بمقاس مناسب للسياق."""
    def repl(m):
        start = m.start()
        in_footer = html.rfind("<footer", 0, start) > html.rfind("</footer>", 0, start)
        size = 18 if in_footer else 22
        content = social_icons(size)
        if in_footer:
            content = content.replace('social-icons">',
                                      'social-icons social-icons-sm">', 1)
        return content
    return re.sub(r'<div class="social-icons[^"]*">.*?</div>', repl, html, flags=re.S)


HEAD_ADDITIONS = {
    "rss": '<link rel="alternate" type="application/rss+xml" title="أدلة أبو نواف — RSS" href="__D__/feed.xml">',
    "dns": '<link rel="dns-prefetch" href="//fonts.gstatic.com">',
}


def upgrade_head(html, path_url):
    # 1) احذف وسم التحقق الوهمي
    html = re.sub(r'\s*<meta name="google-site-verification" content="GOOGLE_VERIFICATION_CODE_HERE">\s*\n?', "\n", html)
    html = re.sub(r'\s*<meta name="msvalidate\.01" content="BING_VERIFICATION_CODE_HERE">\s*\n?', "\n", html)
    html = re.sub(r'\s*<meta name="yandex-verification" content="YANDEX_VERIFICATION_CODE_HERE">\s*\n?', "\n", html)

    # 2) أضف RSS + dns-prefetch قبل </head> إن لم يوجدا
    if 'application/rss+xml' not in html:
        extra = (HEAD_ADDITIONS["rss"].replace("__D__", DOMAIN) + "\n"
                 + HEAD_ADDITIONS["dns"] + "\n")
        html = html.replace("</head>", extra + "</head>", 1)

    # 3) preload خفيف لملف الخطوط (يحسّن LCP)
    if 'rel="preload"' in html and 'family=Tajawal' in html and 'as="style" href="https://fonts.googleapis.com' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tajawal',
            '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap">\n    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tajawal',
            1)
    return html


def upgrade_schema(html):
    """إثراء JSON-LD: Person، SiteNavigationElement، speakable، إصلاح ContactPoint."""
    def repl(m):
        raw = m.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return m.group(0)
        graph = data.get("@graph")
        if not isinstance(graph, list):
            return m.group(0)

        D = DOMAIN
        for node in graph:
            t = node.get("@type")
            types = t if isinstance(t, list) else [t]

            # Organization: احذف contactOption الخاطئ وأضف الحقول الصحيحة
            if "Organization" in types:
                cps = node.get("contactPoint")
                if isinstance(cps, list):
                    for cp in cps:
                        cp.pop("contactOption", None)          # ليس رقماً مجانياً
                        cp.setdefault("contactType", "customer support")
                        cp.update({
                            "telephone": "+966572851032",
                            "email": "contact@ant.xo.je",
                            "availableLanguage": ["ar", "en"],
                            "areaServed": "SA",
                        })
                node["knowsLanguage"] = ["ar", "en"]
                node.setdefault("slogan", "حماية خصوصيتك الرقمية تبدأ بإجراء صحيح")

            # WebPage: أضف speakable + lastReviewed
            if "WebPage" in types:
                node.setdefault("speakable", {
                    "@type": "SpeakableSpecification",
                    "cssSelector": ["h1", ".page-head .lead", ".hero-desc"],
                })
                node["lastReviewed"] = "2026-11-06"
                node.setdefault("reviewedBy", {"@id": D + "/#organization"})

        ids = {n.get("@id") for n in graph}

        # Person (E-E-A-T)
        if D + "/#person" not in ids:
            graph.append({
                "@type": "Person",
                "@id": D + "/#person",
                "name": "أبو نواف",
                "alternateName": "ابونواف",
                "jobTitle": "استشاري أمن سيبراني",
                "description": "متخصص سعودي في الأمن السيبراني والاستجابة للحوادث، يقود فريق أبو نواف في الرياض.",
                "worksFor": {"@id": D + "/#organization"},
                "url": D + "/pages/about.html",
                "knowsAbout": ["أمن المعلومات", "الاستجابة للحوادث", "حماية الخصوصية", "OSINT", "الابتزاز الإلكتروني"],
                "sameAs": [
                    "https://t.me/KSA_hack01",
                    "https://x.com/ksa_hack2",
                    "https://github.com/elias0878",
                ],
            })

        # SiteNavigationElement — يساعد على فهم بنية الموقع
        if D + "/#nav" not in ids:
            nav = [
                ("الرئيسية", "/"),
                ("الخدمات", "/pages/services.html"),
                ("الأدلة", "/guides/"),
                ("مشكلات وحلول", "/pages/problems.html"),
                ("من نحن", "/pages/about.html"),
                ("تواصل", "/pages/contact.html"),
            ]
            graph.append({
                "@type": "ItemList",
                "@id": D + "/#nav",
                "name": "قائمة تنقل الموقع",
                "itemListElement": [
                    {"@type": "SiteNavigationElement", "position": i,
                     "name": n, "url": D + u}
                    for i, (n, u) in enumerate(nav, 1)
                ],
            })

        data["@graph"] = graph
        return ('<script type="application/ld+json">'
                + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                + "</script>")

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, html, flags=re.S)


def add_channels_section(html):
    """إدراج قسم قنوات التواصل في الصفحة الرئيسية بعد الهيرو."""
    if 'id="channels"' in html:
        return html
    section = f'''
<section class="channels-section" id="channels" aria-labelledby="channels-title">
    <div class="container">
        <h2 id="channels-title">قنوات التواصل الرسمية</h2>
        <p class="ch-lead">كل القنوات أدناه رسمية ومدارة من الفريق مباشرة. أي حساب يتواصل معك باسمنا وغير مذكور هنا ليس تابعاً لنا.</p>
{channel_cards()}
        <p class="ch-note-bottom">
            <svg viewBox="0 0 24 24" fill="none" width="16" height="16" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8.4-7 10-4-1.6-7-5.5-7-10V6l7-3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
            لا نطلب كلمات المرور ولا رموز التحقق عبر أي قناة — بلا استثناء.
        </p>
    </div>
</section>
'''
    marker = '<section class="container" style="padding:64px 20px">'
    idx = html.find(marker)
    if idx == -1:
        return html
    return html[:idx] + section + "\n" + html[idx:]


def add_mobile_dock(html):
    """شريط تواصل سفلي ثابت للجوال."""
    if 'class="m-dock"' in html:
        return html
    dock = f'''
<nav class="m-dock" aria-label="تواصل سريع">
    <a href="https://wa.me/{WA_NUMBER}?text={WA_TEXT}" target="_blank" rel="noopener noreferrer" class="m-dock-btn m-dock-wa">
        <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">{WA}</svg><span>واتساب</span>
    </a>
    <a href="https://t.me/KSA_hack01" target="_blank" rel="noopener noreferrer me" class="m-dock-btn m-dock-tg">
        <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">{TG}</svg><span>تيليجرام</span>
    </a>
    <a href="tel:+{WA_NUMBER}" class="m-dock-btn m-dock-call">
        <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">{PHONE}</svg><span>اتصال</span>
    </a>
</nav>
'''
    return html.replace("</body>", dock + "</body>", 1)


def set_domain(html):
    """توحيد كل الروابط المطلقة على النطاق المعتمد."""
    for old in ("https://ant.xo.je", "http://ant.xo.je"):
        html = html.replace(old, DOMAIN)
    return html


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    files = [f for f in files if "/tools/" not in f and "/.git/" not in f]
    print(f"معالجة {len(files)} ملفاً...\n")
    for f in files:
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        html = open(f, encoding="utf-8").read()
        before = len(html)

        html = set_domain(html)
        html = fix_social_blocks(html)
        html = upgrade_head(html, rel)
        html = upgrade_schema(html)
        if rel == "index.html":
            html = add_channels_section(html)
        if rel != "pages/tools.html":
            html = add_mobile_dock(html)

        open(f, "w", encoding="utf-8").write(html)
        print(f"  ✓ {rel:52} {before:>7,} → {len(html):>7,}")


if __name__ == "__main__":
    main()
