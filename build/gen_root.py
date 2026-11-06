# -*- coding: utf-8 -*-
"""توليد robots.txt و sitemap.xml و manifest.json و humans.txt و security.txt"""
import json, os
from datetime import date
from layout import BASE
from content_services import SERVICES
from content_guides import GUIDES

TODAY = date.today().isoformat()
OUT = "/home/user/site"

PAGES = [
    ("/", "1.0", "weekly"),
    ("/pages/services.html", "0.9", "weekly"),
    ("/guides/", "0.9", "weekly"),
    ("/pages/problems.html", "0.8", "weekly"),
    ("/pages/about.html", "0.7", "monthly"),
    ("/pages/contact.html", "0.6", "monthly"),
    ("/pages/privacy.html", "0.3", "yearly"),
    ("/pages/terms.html", "0.3", "yearly"),
] + [
    (f"/services/{s['slug']}.html", "0.8", "monthly") for s in SERVICES
] + [
    (f"/guides/{g['slug']}.html", "0.7", "monthly") for g in GUIDES
]


def robots():
    txt = """# robots.txt — فريق أبو نواف للأمن السيبراني
# https://ant.xo.je/
# آخر تحديث: {today}

User-agent: *
Allow: /
Disallow: /api/
Disallow: /*?utm_
Disallow: /*?fbclid

# ── محركات البحث ──
User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /assets/images/

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: YandexBot
Allow: /

User-agent: Applebot
Allow: /

# ── معاينات المشاركة ──
User-agent: Twitterbot
Allow: /

User-agent: facebookexternalhit
Allow: /

User-agent: WhatsApp
Allow: /

User-agent: TelegramBot
Allow: /

# ── روبوتات الذكاء الاصطناعي (مسموح — نريد الظهور في إجابات AI) ──
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

# ── أدوات تحليل SEO ──
User-agent: AhrefsBot
Allow: /

User-agent: SemrushBot
Allow: /

Sitemap: {base}/sitemap.xml
""".format(today=TODAY, base=BASE)
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(txt)
    print("  ✓ robots.txt")


def sitemap():
    rows = []
    for path, prio, freq in PAGES:
        loc = BASE + path
        rows.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
    <xhtml:link rel="alternate" hreflang="ar-SA" href="{loc}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{chr(10).join(rows)}
</urlset>
"""
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    print(f"  ✓ sitemap.xml ({len(PAGES)} URLs)")


def manifest():
    m = {
        "id": BASE + "/",
        "name": "فريق أبو نواف للأمن السيبراني",
        "short_name": "ابونواف",
        "description": "أمن سيبراني وحماية خصوصية: استعادة الحسابات، مكافحة الابتزاز، وتأمين الحسابات.",
        "lang": "ar",
        "dir": "rtl",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#0f2438",
        "theme_color": "#1a365d",
        "categories": ["security", "productivity", "utilities"],
        "icons": [
            {"src": "/assets/images/icon-192.png", "sizes": "192x192",
             "type": "image/png", "purpose": "any maskable"},
            {"src": "/assets/images/icon-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "any maskable"},
            {"src": "/assets/icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }
    open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(m, ensure_ascii=False, indent=2))
    print("  ✓ manifest.json")


def humans():
    txt = f"""/* TEAM */
    الفريق: فريق أبو نواف للأمن السيبراني
    الموقع: الرياض، المملكة العربية السعودية
    المجال: الأمن السيبراني · حماية الخصوصية · الاستجابة للحوادث
    التواصل: https://t.me/KSA_hack01

/* SITE */
    اللغة: العربية
    آخر تحديث: {TODAY}
    الموقع: {BASE}
    المعايير: HTML5 · CSS3 · ES6 · Schema.org · WCAG AA

/* NOTE */
    هذا الموقع لا يستخدم أي أدوات تتبع إعلانية.
"""
    open(os.path.join(OUT, "humans.txt"), "w", encoding="utf-8").write(txt)
    print("  ✓ humans.txt")


def security_txt():
    os.makedirs(os.path.join(OUT, ".well-known"), exist_ok=True)
    txt = f"""Contact: https://t.me/KSA_hack01
Expires: 2027-12-31T23:59:59.000Z
Preferred-Languages: ar, en
Canonical: {BASE}/.well-known/security.txt
"""
    open(os.path.join(OUT, ".well-known", "security.txt"), "w", encoding="utf-8").write(txt)
    print("  ✓ .well-known/security.txt")


def fix_status_widget():
    """تصحيح خلل مؤشر «مغلق حالياً» ليعمل بتوقيت الرياض لا توقيت الزائر."""
    p = os.path.join(OUT, "js", "main.js")
    src = open(p, encoding="utf-8").read()
    old = """        const now = new Date();
        const hour = now.getHours() + (now.getMinutes() / 60);
        const day = now.getDay(); // 0=الأحد, 5=الجمعة"""
    new = """        // ← إصلاح: احسب دائماً بتوقيت الرياض (UTC+3) لا بتوقيت جهاز الزائر
        const now = new Date();
        const riyadh = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Riyadh' }));
        const hour = riyadh.getHours() + (riyadh.getMinutes() / 60);
        const day = riyadh.getDay(); // 0=الأحد, 5=الجمعة"""
    if old in src:
        src = src.replace(old, new)
        # تصحيح منطق الساعات: 14:30 حتى 24:00
        src = src.replace(
            "const isWorkingHours = (hour >= 14.5 && hour < 24) || (hour >= 0 && hour < 0.5);",
            "const isWorkingHours = (hour >= 14.5 && hour < 24);")
        open(p, "w", encoding="utf-8").write(src)
        print("  ✓ js/main.js — أُصلح مؤشر الحالة (توقيت الرياض)")
    else:
        print("  ! js/main.js — لم يُعثر على الكتلة الأصلية (تحقق يدوياً)")


if __name__ == "__main__":
    print("توليد الملفات التقنية:")
    robots(); sitemap(); manifest(); humans(); security_txt(); fix_status_widget()
