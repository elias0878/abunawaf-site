# -*- coding: utf-8 -*-
"""
إعادة بناء صفحات الموقع بمحتوى وتصميم الموقع الأصلي (ant.xo.je) حرفياً،
مع الاحتفاظ بكل تحسينات SEO + أزرار التواصل + الأداء.
"""
import json
import os
import re
import sys

sys.path.insert(0, "/home/user/site/tools")
from upgrade import CHANNELS, WA_NUMBER, WA_TEXT, social_icons, _rel
from add_socialbar import BAR as SOCIALBAR
from icons import WA, TG, PHONE

SRC = "/home/user/rebuild/_source"
OUT = "/home/user/site"
D = "https://abunawaf.vercel.app"

WA_URL = f"https://wa.me/{WA_NUMBER}?text={WA_TEXT}"
TG_URL = "https://t.me/KSA_hack01"

NAV = [("/", "الرئيسية"), ("/pages/services.html", "الخدمات"),
       ("/pages/tools.html", "الأدوات"), ("/pages/problems.html", "مشكلات وحلول"),
       ("/pages/terms.html", "الشروط"), ("/pages/contact.html", "تواصل معنا")]

FOOTER_QUICK = [("/", "الرئيسية"), ("/pages/services.html", "الخدمات"),
                ("/pages/tools.html", "الأدوات"), ("/pages/problems.html", "مشكلات وحلول"),
                ("/pages/terms.html", "الشروط والأحكام"), ("/guides/", "الأدلة والمقالات"),
                ("/pages/privacy.html", "سياسة الخصوصية"),
                ("/pages/about.html", "من نحن"), ("/pages/contact.html", "تواصل معنا")]

FOOTER_SERVICES = [("/pages/services.html#recover-stolen", "استعادة حساب مسروق"),
                   ("/pages/services.html#recover-suspended", "استعادة حساب موقوف"),
                   ("/pages/services.html#info-gathering", "جمع معلومات وكشف هوية"),
                   ("/pages/services.html#delete-deceased", "حذف حساب متوفي"),
                   ("/pages/services.html#anti-blackmail", "مكافحة ابتزاز إلكتروني")]


# ───────────────────────── أدوات مساعدة ─────────────────────────
def orig_body(name):
    """يستخرج منطقة المحتوى من صفحة أصلية."""
    s = open(os.path.join(SRC, name), encoding="utf-8").read()
    start = s.find('<header class="hero"')
    if start == -1:
        start = s.find('<header class="page-header"')
    if start == -1:
        raise SystemExit(f"لم أجد محتوى في {name}")
    end = s.find("<footer", start)
    return s[start:end].rstrip()


def normalize(html):
    """توحيد الروابط والمسارات إلى جذور مطلقة."""
    html = html.replace('href="https://ant.xo.je/pages/', 'href="/pages/')
    html = html.replace('href="https://ant.xo.je/"', 'href="/"')
    html = html.replace('href="https://ant.xo.je', 'href="' + D)
    html = re.sub(r'href="(?:\.\./)?index\.html(#[^"]*)?"', lambda m: 'href="/%s"' % (m.group(1) or ""), html)
    html = re.sub(r'href="(?:\.\./)?([a-z]+)\.html(#[^"]*)?"',
                  lambda m: 'href="/pages/%s.html%s"' % (m.group(1), m.group(2) or ""), html)
    html = html.replace('src="../assets/', 'src="/assets/').replace('src="assets/', 'src="/assets/')
    html = html.replace('src="../', 'src="/').replace('href="../css/', 'href="/css/')
    html = html.replace('href="../manifest.json"', 'href="/manifest.json"')
    # صور وأيقونات داخل المحتوى فقط
    html = re.sub(r'\s(?:loading="lazy")?\s*fetchpriority="low"', "", html)
    return html


def nav(active):
    items = []
    for href, label in NAV:
        cls = ' class="active" aria-current="page"' if href == active else (
            ' class="nav-cta"' if href == "/pages/contact.html" else "")
        items.append(f'                <li><a href="{href}"{cls}>{label}</a></li>')
    return f'''    <nav class="navbar" id="navbar" role="navigation" aria-label="القائمة الرئيسية">
        <div class="nav-container">
            <a href="/" class="nav-logo" aria-label="أبو نواف (ابونواف) هكر أخلاقي سعودي — الصفحة الرئيسية">
                <img src="/assets/images/logo.jpg" alt="شعار أبو نواف (ابونواف) هكر أخلاقي سعودي وخبير أمن سيبراني" class="logo-img" width="44" height="44" loading="eager">
                <div class="logo-text">
                    <span class="logo-name">ابونواف</span>
                    <span class="logo-sub">هكر أخلاقي سعودي</span>
                </div>
            </a>
            <ul class="nav-links" id="navLinks">
{chr(10).join(items)}
            </ul>
            <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="فتح القائمة" aria-expanded="false">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
        </div>
    </nav>
'''


def footer():
    quick = "\n".join(f'                        <li><a href="{h}">{t}</a></li>' for h, t in FOOTER_QUICK)
    serv = "\n".join(f'                        <li><a href="{h}">{t}</a></li>' for h, t in FOOTER_SERVICES)
    return f'''    <footer class="footer" role="contentinfo">
        <div class="container">
            <div class="footer-social-bar">
                <span>تابعنا وتواصل معنا</span>
                {social_icons(20)}
            </div>
            <div class="footer-grid">
                <div class="footer-about">
                    <div class="footer-logo">
                        <img src="/assets/images/logo.jpg" alt="شعار أبو نواف (ابونواف) هكر أخلاقي سعودي" class="footer-logo-img" width="40" height="40" loading="lazy">
                        <span>ابونواف</span>
                    </div>
                    <p>أبو نواف (ابونواف) هكر أخلاقي سعودي وخبير أمن سيبراني — خدمات فردية متخصصة في استعادة الحسابات المسروقة والموقوفة، مكافحة الابتزاز الإلكتروني، وكشف الهوية وجمع المعلومات.</p>
                </div>
                <div class="footer-links">
                    <h4>روابط سريعة</h4>
                    <ul>
{quick}
                    </ul>
                </div>
                <div class="footer-services">
                    <h4>خدماتنا</h4>
                    <ul>
{serv}
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>تواصل معنا</h4>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke="currentColor" stroke-width="2"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/></svg>
                        <span>الرياض، المملكة العربية السعودية</span>
                    </div>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                        <span>يومياً: 2:30م - 12:00ص (مغلق الجمعة)</span>
                    </div>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">{TG}</svg>
                        <a href="{TG_URL}" target="_blank" rel="noopener noreferrer me">@KSA_hack01</a>
                    </div>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">{WA}</svg>
                        <a href="{WA_URL}" target="_blank" rel="noopener noreferrer"><bdi dir="ltr">+966 57 285 1032</bdi></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">2026</span> أبو نواف (ابونواف) هكر أخلاقي سعودي | ant.xo.je — جميع الحقوق محفوظة.</p>
            </div>
        </div>
    </footer>
'''


def floats():
    return f'''    <a class="wa-float" href="{WA_URL}" target="_blank" rel="noopener noreferrer"
       aria-label="تواصل عبر واتساب على الرقم +966 57 285 1032">
        <svg viewBox="0 0 24 24" fill="none" width="30" height="30" aria-hidden="true">{WA}</svg>
        <span class="wa-float-text">واتساب<br><b dir="ltr">+966 57 285 1032</b></span>
    </a>

    <nav class="m-dock" aria-label="تواصل سريع">
        <a href="{WA_URL}" target="_blank" rel="noopener noreferrer" class="m-dock-btn m-dock-wa">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">{WA}</svg><span>واتساب</span>
        </a>
        <a href="{TG_URL}" target="_blank" rel="noopener noreferrer me" class="m-dock-btn m-dock-tg">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">{TG}</svg><span>تيليجرام</span>
        </a>
        <a href="tel:+{WA_NUMBER}" class="m-dock-btn m-dock-call">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">{PHONE}</svg><span>اتصال</span>
        </a>
    </nav>
'''


# ───────────────────────── البيانات المنظّمة ─────────────────────────
ORG = {
    "@type": "Organization",
    "@id": D + "/#organization",
    "name": "أبو نواف (ابونواف) — هكر أخلاقي سعودي",
    "alternateName": "ابونواف",
    "url": D + "/",
    "logo": {"@type": "ImageObject", "@id": D + "/#logo",
             "url": D + "/assets/images/logo.jpg", "contentUrl": D + "/assets/images/logo.jpg",
             "width": 512, "height": 512, "caption": "أبو نواف (ابونواف)"},
    "image": {"@id": D + "/#logo"},
    "description": "فريق أبو نواف (ابونواف) للأمن السيبراني والاختراق الأخلاقي في الرياض — استعادة الحسابات المسروقة والموقوفة، مكافحة الابتزاز الإلكتروني، OSINT، وفحص وتأمين الحسابات.",
    "address": {"@type": "PostalAddress", "addressLocality": "الرياض", "addressRegion": "Riyadh",
                "addressCountry": "SA"},
    "telephone": "+966572851032",
    "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support",
                      "telephone": "+966572851032", "availableLanguage": ["ar", "en"],
                      "areaServed": "SA",
                      "hoursAvailable": {"@type": "OpeningHoursSpecification",
                                         "dayOfWeek": ["Saturday", "Sunday", "Monday", "Tuesday",
                                                       "Wednesday", "Thursday"],
                                         "opens": "14:30", "closes": "23:59"}}],
    "areaServed": {"@type": "Country", "name": "السعودية"},
    "knowsLanguage": ["ar", "en"],
    "slogan": "الدفع بعد الإنجاز — بسرية تامة",
    "knowsAbout": ["استعادة الحسابات المخترقة", "مكافحة الابتزاز الإلكتروني", "OSINT",
                   "الأمن السيبراني", "حماية الخصوصية", "اختبار الاختراق الأخلاقي"],
    "sameAs": ["https://t.me/KSA_hack01", "https://www.snapchat.com/add/ant_ceh",
               "https://www.instagram.com/ksa_hack01", "https://www.tiktok.com/@ksa_hack01",
               "https://x.com/ksa_hack2",
               "https://www.facebook.com/profile.php?id=61554330014413",
               "https://github.com/elias0878"],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
        "opens": "14:30", "closes": "23:59"}],
}

PERSON = {
    "@type": "Person", "@id": D + "/#person", "name": "أبو نواف",
    "alternateName": "ابونواف", "jobTitle": "هكر أخلاقي سعودي وخبير أمن سيبراني",
    "description": "متخصص سعودي في الأمن السيبراني والاختراق الأخلاقي يقود فريق أبو نواف في الرياض.",
    "worksFor": {"@id": D + "/#organization"}, "url": D + "/pages/about.html",
    "knowsAbout": ["الأمن السيبراني", "الاختراق الأخلاقي", "OSINT", "استعادة الحسابات",
                   "مكافحة الابتزاز الإلكتروني"],
    "sameAs": ["https://t.me/KSA_hack01", "https://x.com/ksa_hack2", "https://github.com/elias0878"],
}


def graph(url, title, desc, crumbs=None, faq=None, extra=None):
    g = [ORG,
         {"@type": "WebSite", "@id": D + "/#website", "url": D + "/",
          "name": "أبو نواف (ابونواف) — هكر أخلاقي سعودي",
          "alternateName": "ابونواف", "inLanguage": "ar",
          "publisher": {"@id": D + "/#organization"}},
         {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
          "description": desc, "isPartOf": {"@id": D + "/#website"},
          "inLanguage": "ar", "datePublished": "2026-10-11", "dateModified": "2026-11-06",
          "speakable": {"@type": "SpeakableSpecification",
                        "cssSelector": ["h1", ".hero-desc", ".page-header p"]},
          "reviewedBy": {"@id": D + "/#organization"}},
         PERSON,
         {"@type": "ItemList", "@id": D + "/#nav", "name": "قائمة تنقل الموقع",
          "itemListElement": [{"@type": "SiteNavigationElement", "position": i,
                               "name": t, "url": D + h} for i, (h, t) in enumerate(NAV, 1)]}]
    if crumbs:
        g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
                  "itemListElement": [
                      {"@type": "ListItem", "position": i, "name": n,
                       "item": (D + u if u else url)}
                      for i, (n, u) in enumerate(crumbs, 1)]})
    if faq:
        g.append({"@type": "FAQPage", "@id": url + "#faq",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a in faq]})
    if extra:
        g.extend(extra)
    return json.dumps({"@context": "https://schema.org", "@graph": g},
                      ensure_ascii=False, separators=(",", ":"))


def head(rel, title, desc, schema, og_img="/assets/images/og-services.jpg"):
    url = D + ("/" if rel == "index.html" else "/" + rel)
    alt = title.split("|")[0].strip()[:110]
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="author" content="أبو نواف (ابونواف) — هكر أخلاقي سعودي">
    <meta name="theme-color" content="#1a365d">
    <link rel="canonical" href="{url}">
    <link rel="alternate" hreflang="ar-SA" href="{url}">
    <link rel="alternate" hreflang="ar" href="{url}">
    <link rel="alternate" hreflang="x-default" href="{url}">
    <link rel="alternate" type="application/rss+xml" title="أدلة أبو نواف — RSS" href="{D}/feed.xml">
    <link rel="dns-prefetch" href="//fonts.gstatic.com">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="أبو نواف (ابونواف)">
    <meta property="og:locale" content="ar_SA">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{D}{og_img}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{alt}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{D}{og_img}">
    <meta name="twitter:image:alt" content="{alt}">
    <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&amp;display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&amp;display=swap">
    <link rel="preload" href="/css/main.css" as="style">
    <link rel="preload" href="/assets/images/logo.jpg" as="image" fetchpriority="high">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/extra.css">
    <script type="application/ld+json">{schema}</script>
</head>
<body>
    <a class="skip-link" href="#main-content">تخطي إلى المحتوى الرئيسي</a>
    <div class="status-indicator" id="statusIndicator">
        <span class="status-dot"></span>
        <span class="status-text">متاح للتواصل</span>
    </div>

{nav("/" if rel == "index.html" else "/" + rel)}
    {SOCIALBAR}
'''


def tail(scripts="/js/main.js"):
    tags = "".join(f'\n    <script src="{s}" defer></script>' for s in scripts.split(","))
    return f'''
{floats()}
{tags}
</body>
</html>
'''


# ───────────────────────── صفحات ─────────────────────────
def build_index():
    content = normalize(orig_body("index.html"))
    # واتساب كزر أساسي في الهيرو + تيليجرام
    content = content.replace(
        '''                <a href="#social-top" class="btn btn-primary btn-lg">''',
        f'''                <a href="{WA_URL}" class="btn btn-whatsapp btn-lg" target="_blank" rel="noopener noreferrer">
                    <svg viewBox="0 0 24 24" fill="none" class="btn-icon" width="20" height="20">{WA}</svg>
                    واتساب الآن — <span dir="ltr">+966 57 285 1032</span>
                </a>
                <a href="{TG_URL}" class="btn btn-telegram btn-lg" target="_blank" rel="noopener noreferrer me">
                    <svg viewBox="0 0 24 24" fill="none" class="btn-icon" width="20" height="20">{TG}</svg>
                    تيليجرام @KSA_hack01
                </a>
                <a href="#social-top" class="btn btn-outline btn-lg">''')
    # توحيد رابط إكس
    content = content.replace('href="https://twitter.com/ksa_hack2"', 'href="https://x.com/ksa_hack2"')
    # إضافة واتساب وجيت هاب والهاتف لشبكة الحسابات الرسمية
    wa_card = f'''                    <a href="{WA_URL}" class="social-card featured social-card-wa" target="_blank" rel="noopener noreferrer" aria-label="واتساب أبو نواف +966572851032">
                        <div class="social-icon whatsapp"><svg viewBox="0 0 24 24" fill="none">{WA}</svg></div>
                        <span>واتساب</span>
                        <span class="social-sub" dir="ltr">+966 57 285 1032</span>
                    </a>
                    <a href="https://github.com/elias0878" class="social-card" target="_blank" rel="noopener noreferrer me" aria-label="جيت هاب elias0878">
                        <div class="social-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg></div>
                        <span>GitHub</span>
                    </a>
'''
    content = content.replace('''                    <a href="https://x.com/ksa_hack2"''', wa_card + '''                    <a href="https://x.com/ksa_hack2"''')
    # روابط الأدلة في نهاية الصفحة
    content = content.replace('</header>', '''</header>''')
    faq = [
        ("من هو أبو نواف (ابونواف) هكر أخلاقي سعودي؟",
         "أبو نواف (المعروف أيضاً باسم ابونواف هكر اخلاقي) هو متخصص سعودي في الأمن السيبراني والاختراق الأخلاقي يقود فريقاً تقنياً في الرياض. يقدم حلولاً احترافية لاستعادة الحسابات المخترقة والموقوفة، مكافحة الابتزاز الإلكتروني، جمع المعلومات (OSINT)، وفحص وتأمين الحسابات."),
        ("كيف يمكن استعادة حساب مسروق أو مخترق من خلال ابونواف؟",
         "تواصل معنا عبر تيليجرام @KSA_hack01 أو سناب شات ant_ceh أو واتساب +966572851032. تتراوح مدة استعادة الحساب المسروق من 2 إلى 6 ساعات حسب المنصة والتعقيد (سناب شات، إنستغرام، تويتر X، تيك توك، فيسبوك)، مع تقديم تقرير شامل قبل البدء."),
        ("كم تستغرق استعادة حساب موقوف أو محظور؟",
         "مدة استعادة الحساب الموقوف أو المحظور تتراوح بين 6 إلى 24 ساعة حسب المنصة وسبب الإيقاف. نقدم تقريراً شاملاً يوضح نسبة النجاح والمدة الدقيقة قبل الشروع في العمل."),
        ("هل الدفع بعد الإنجاز؟ وما هي أوقات عمل فريق ابونواف؟",
         "نعم، الدفع يكون بعد الإنجاز والتأكد من النتائج (العملاء الجدد يحتاجون ضماناً بسيطاً أو دفع 50% عند إكمال نصف العمل وتوثيقه). نعمل يومياً من 2:30 مساءً حتى 12:00 منتصف الليل بتوقيت الرياض (مغلق يوم الجمعة)."),
    ]
    title = "أبو نواف (ابونواف) هكر أخلاقي سعودي | استعادة الحسابات ومكافحة الابتزاز"
    desc = ("فريق أبو نواف (ابونواف) للأمن السيبراني في الرياض: استعادة الحسابات المسروقة والموقوفة، "
            "مكافحة الابتزاز الإلكتروني، كشف الهوية (OSINT) — إنجاز خلال 2-48 ساعة والدفع بعد الإنجاز.")
    sch = graph(D + "/", title, desc, faq=faq)
    html = head("index.html", title, desc, sch, "/assets/images/og-default.jpg")
    html += f'    <main id="main-content">\n{content}\n    </main>\n'
    html += footer() + tail()
    return html


def build_simple(name, rel, title, desc, crumbs, og="/assets/images/og-services.jpg",
                 faq=None, scripts="/js/main.js"):
    content = normalize(orig_body(name))
    content = content.replace('href="https://twitter.com/ksa_hack2"', 'href="https://x.com/ksa_hack2"')
    url = D + "/" + rel
    sch = graph(url, title, desc, crumbs=crumbs, faq=faq)
    html = head(rel, title, desc, sch, og)
    html += f'    <main id="main-content">\n{content}\n    </main>\n'
    html += footer() + tail(scripts)
    return html


PAGES = {}


def main():
    PAGES["index.html"] = build_index()

    PAGES["pages/services.html"] = build_simple(
        "pages/services.html", "pages/services.html",
        "خدمات أبو نواف (ابونواف) | 8 خدمات أمن سيبراني مع مدة كل خدمة",
        "ثماني خدمات متخصصة: استعادة حساب مسروق 2-6 ساعات، حساب موقوف 6-24 ساعة، مكافحة ابتزاز 1-3 ساعات، "
        "حذف حساب متوفي 24-48 ساعة، فحص أمني، OSINT — تقرير شامل قبل البدء والدفع بعد الإنجاز.",
        crumbs=[("الرئيسية", "/"), ("الخدمات", None)])

    PAGES["pages/problems.html"] = build_simple(
        "pages/problems.html", "pages/problems.html",
        "مشكلات وحلول سريعة | أبو نواف (ابونواف)",
        "حلول فورية لأكثر المشكلات شيوعاً: حساب مخترق، حساب موقوف، ابتزاز إلكتروني، كلمة مرور ضعيفة، "
        "وحساب شخص متوفى — خطوات عملية مرتّبة من فريق أبو نواف.",
        crumbs=[("الرئيسية", "/"), ("مشكلات وحلول", None)],
        scripts="/js/main.js,/js/problems.js")

    PAGES["pages/tools.html"] = build_simple(
        "pages/tools.html", "pages/tools.html",
        "أدوات أبو نواف (ابونواف) | أدوات OSINT و X Intelligence",
        "مجموعة أدوات أبو نواف (ابونواف) المتقدمة في الاستخبارات مفتوحة المصدر (OSINT): تحليل حسابات X "
        "وتيك توك وسناب شات، استخراج التغريدات المحذوفة، وفحص البريد الإلكتروني.",
        crumbs=[("الرئيسية", "/"), ("الأدوات", None)],
        og="/assets/images/og-guides.jpg")

    PAGES["pages/contact.html"] = build_simple(
        "pages/contact.html", "pages/contact.html",
        "تواصل مع فريق أبو نواف (ابونواف) | الحسابات الرسمية",
        "طرق التواصل الرسمية مع فريق أبو نواف: تيليجرام @KSA_hack01، واتساب +966572851032، سناب شات ant_ceh، "
        "إنستقرام وتيك توك وإكس — يومياً 2:30م إلى 12:00ص عدا الجمعة.",
        crumbs=[("الرئيسية", "/"), ("تواصل معنا", None)],
        og="/assets/images/og-default.jpg")

    PAGES["pages/terms.html"] = build_simple(
        "pages/terms.html", "pages/terms.html",
        "الشروط والأحكام ونظام العمل | أبو نواف (ابونواف)",
        "شروط العمل والدفع لدى فريق أبو نواف: تقرير شامل قبل البدء، الدفع بعد الإنجاز، الضمان للعملاء الجدد، "
        "وخطة العمل السبع خطوات كاملة.",
        crumbs=[("الرئيسية", "/"), ("الشروط والأحكام", None)])

    for rel, html in PAGES.items():
        p = os.path.join(OUT, rel)
        open(p, "w", encoding="utf-8").write(html)
        print(f"  ✓ {rel:<28} {len(html):>7,} حرفاً")


if __name__ == "__main__":
    main()
