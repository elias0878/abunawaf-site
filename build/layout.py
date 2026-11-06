# -*- coding: utf-8 -*-
"""
نظام البناء — قوالب الصفحات المشتركة
كل صفحة تُولَّد من هنا لضمان تناسق الوسوم (title/desc/canonical/schema).
"""
from html import escape

BASE = "https://ant.xo.je"

# ─────────────────────────── بيانات الكيان (مصدر واحد للحقيقة) ───────────────────────────
ORG = {
    "name": "فريق أبو نواف للأمن السيبراني",
    "alt": ["أبو نواف", "ابونواف", "أبو نواف هكر أخلاقي"],
    "url": BASE + "/",
    "logo": BASE + "/assets/images/logo.jpg",
    "desc": "فريق سعودي متخصص في الأمن السيبراني وحماية الخصوصية الرقمية: استعادة الحسابات، مكافحة الابتزاز الإلكتروني، وتأمين الحسابات.",
    "city": "الرياض",
    "region": "منطقة الرياض",
    "country": "SA",
    "telegram": "https://t.me/KSA_hack01",
    "sameAs": [
        "https://t.me/KSA_hack01",
        "https://www.snapchat.com/add/ant_ceh",
        "https://www.instagram.com/ksa_hack01",
        "https://www.tiktok.com/@ksa_hack01",
        "https://twitter.com/ksa_hack2",
        "https://x.com/ksa_hack2",
        "https://www.facebook.com/profile.php?id=61554330014413",
        "https://github.com/elias0878",
    ],
    "hours": {"opens": "14:30", "closes": "23:59",
              "days": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Saturday"]},
}

NAV = [
    ("الرئيسية", "/"),
    ("الخدمات", "/pages/services.html"),
    ("الأدلة", "/guides/"),
    ("مشكلات وحلول", "/pages/problems.html"),
    ("من نحن", "/pages/about.html"),
    ("تواصل", "/pages/contact.html"),
]


def schema_organization():
    return {
        "@type": "Organization",
        "@id": BASE + "/#organization",
        "name": ORG["name"],
        "alternateName": ORG["alt"],
        "url": ORG["url"],
        "logo": {"@type": "ImageObject", "url": ORG["logo"], "width": 399, "height": 400},
        "image": ORG["logo"],
        "description": ORG["desc"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": ORG["city"],
            "addressRegion": ORG["region"],
            "addressCountry": ORG["country"],
        },
        "areaServed": [
            {"@type": "Country", "name": "المملكة العربية السعودية"},
            {"@type": "Country", "name": "الإمارات العربية المتحدة"},
            {"@type": "Country", "name": "الكويت"},
            {"@type": "Country", "name": "قطر"},
        ],
        "knowsAbout": [
            "أمن المعلومات", "حماية الخصوصية", "الاستجابة للحوادث",
            "استعادة الحسابات", "الابتزاز الإلكتروني", "OSINT",
        ],
        "sameAs": ORG["sameAs"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ORG["hours"]["days"],
            "opens": ORG["hours"]["opens"],
            "closes": ORG["hours"]["closes"],
        }],
    }


def schema_website():
    return {
        "@type": "WebSite",
        "@id": BASE + "/#website",
        "url": ORG["url"],
        "name": "أبو نواف (ابونواف) — هكر أخلاقي سعودي",
        "alternateName": "ابونواف",
        "inLanguage": "ar",
        "publisher": {"@id": BASE + "/#organization"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": BASE + "/?s={search_term_string}"},
            "query-input": "required name=search_term_string",
        },
    }


def schema_breadcrumb(items):
    """items: [(name, url_or_None), ...] — آخر عنصر بلا رابط"""
    out = []
    for i, (name, url) in enumerate(items, start=1):
        node = {"@type": "ListItem", "position": i, "name": name}
        if url:
            node["item"] = url
        out.append(node)
    return {"@type": "BreadcrumbList",
            "@id": items[-1][1] or BASE + "/",
            "itemListElement": out}


def schema_faq(pairs, page_url):
    return {
        "@type": "FAQPage",
        "@id": page_url + "#faq",
        "mainEntity": [{
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        } for q, a in pairs],
    }


# ─────────────────────────── القالب الرئيسي ───────────────────────────
def page(*, path, title, desc, h1, body, schema_graph, breadcrumb=None,
         og_image="og-default.jpg", og_type="website", noindex=False,
         extra_head="", keywords=None, container=True, active="/"):
    """
    path      : مسار الصفحة من الجذر، مثل "/pages/services.html"
    schema_graph: قائمة كيانات (بدون @context) تُدمج مع Organization و WebSite
    """
    url = BASE + path
    robots = ("noindex, follow" if noindex else
              "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1")

    graph = [schema_organization(), schema_website(), {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": title,
        "description": desc,
        "isPartOf": {"@id": BASE + "/#website"},
        "about": {"@id": BASE + "/#organization"},
        "inLanguage": "ar",
        "datePublished": "2026-10-11",
        "dateModified": "2026-11-06",
    }]
    if breadcrumb:
        graph.append(schema_breadcrumb(breadcrumb))
    graph.extend(schema_graph or [])

    import json
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, separators=(",", ":"))

    kw = keywords or ("ابونواف, أبو نواف, هكر أخلاقي سعودي, استعادة حساب مخترق, "
                      "مكافحة ابتزاز إلكتروني, تأمين حسابات, الرياض")

    # بناء NAV مع الحالة النشطة
    nav_items = []
    for label, href in NAV:
        cls = ' class="active" aria-current="page"' if href == active else ""
        nav_items.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    nav_html = "\n                    ".join(nav_items)

    body_inner = f'<main>\n{body}\n</main>' if container else body

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(desc)}">
    <meta name="keywords" content="{escape(kw)}">
    <meta name="robots" content="{robots}">
    <meta name="theme-color" content="#1a365d">
    <meta name="author" content="فريق أبو نواف للأمن السيبراني">
    <link rel="canonical" href="{url}">
    <link rel="alternate" hreflang="ar-SA" href="{url}">
    <link rel="alternate" hreflang="ar" href="{url}">
    <link rel="alternate" hreflang="x-default" href="{url}">

    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:image" content="{BASE}/assets/images/{og_image}">
    <meta property="og:image:secure_url" content="{BASE}/assets/images/{og_image}">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{escape(h1)}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{url}">
    <meta property="og:locale" content="ar_SA">
    <meta property="og:site_name" content="أبو نواف — هكر أخلاقي سعودي">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(title)}">
    <meta name="twitter:description" content="{escape(desc)}">
    <meta name="twitter:image" content="{BASE}/assets/images/{og_image}">
    <meta name="twitter:site" content="@ksa_hack2">

    <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/extra.css">
{extra_head}
    <script type="application/ld+json">{ld}</script>
</head>
<body>
    <div class="status-indicator" id="statusIndicator">
        <span class="status-dot"></span>
        <span class="status-text">متاح للتواصل</span>
    </div>

    <nav class="navbar" id="navbar" role="navigation" aria-label="القائمة الرئيسية">
        <div class="nav-container">
            <a href="/" class="nav-logo" aria-label="أبو نواف — الصفحة الرئيسية">
                <img src="/assets/images/logo.jpg" alt="شعار فريق أبو نواف للأمن السيبراني" class="logo-img" width="44" height="44" loading="eager">
                <div class="logo-text">
                    <span class="logo-name">ابونواف</span>
                    <span class="logo-sub">هكر أخلاقي سعودي</span>
                </div>
            </a>
            <ul class="nav-links" id="navLinks">
                    {nav_html}
            </ul>
            <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="فتح القائمة" aria-expanded="false">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
        </div>
    </nav>
    <div class="mobile-overlay" id="mobileOverlay"></div>

{body_inner}

    <footer class="footer" role="contentinfo">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-about">
                    <div class="footer-logo">
                        <img src="/assets/images/logo.jpg" alt="شعار فريق أبو نواف" class="footer-logo-img" width="40" height="40" loading="lazy">
                        <span>ابونواف</span>
                    </div>
                    <p>فريق سعودي متخصص في الأمن السيبراني وحماية الخصوصية الرقمية: استعادة الحسابات، مكافحة الابتزاز الإلكتروني، وتأمين الحسابات.</p>
                </div>
                <div class="footer-links">
                    <h4>روابط سريعة</h4>
                    <ul>
                        <li><a href="/">الرئيسية</a></li>
                        <li><a href="/pages/services.html">الخدمات</a></li>
                        <li><a href="/guides/">الأدلة والحلول</a></li>
                        <li><a href="/pages/problems.html">مشكلات وحلول</a></li>
                        <li><a href="/pages/about.html">من نحن</a></li>
                        <li><a href="/pages/privacy.html">سياسة الخصوصية</a></li>
                        <li><a href="/pages/terms.html">الشروط والأحكام</a></li>
                    </ul>
                </div>
                <div class="footer-services">
                    <h4>خدماتنا</h4>
                    <ul>
                        <li><a href="/services/recover-stolen-account.html">استعادة حساب مسروق</a></li>
                        <li><a href="/services/recover-suspended-account.html">استعادة حساب موقوف</a></li>
                        <li><a href="/services/anti-blackmail.html">مكافحة الابتزاز الإلكتروني</a></li>
                        <li><a href="/services/osint-identity.html">كشف الهوية وجمع المعلومات</a></li>
                        <li><a href="/services/security-audit.html">فحص أمني شامل</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>تواصل معنا</h4>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke="currentColor" stroke-width="2"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/></svg>
                        <span>الرياض، المملكة العربية السعودية</span>
                    </div>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                        <span>يومياً 2:30م – 12:00ص (مغلق الجمعة)</span>
                    </div>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18" aria-hidden="true"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
                        <a href="{ORG['telegram']}" target="_blank" rel="noopener">@KSA_hack01</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">2026</span> فريق أبو نواف للأمن السيبراني — جميع الحقوق محفوظة.</p>
            </div>
        </div>
    </footer>

    <button class="scroll-top" id="scrollTop" aria-label="العودة للأعلى">
        <svg viewBox="0 0 24 24" fill="none" width="24" height="24" aria-hidden="true"><path d="M5 15l7-7 7 7" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>

    <script src="/js/main.js"></script>
</body>
</html>"""


def write(path, html):
    import os
    full = os.path.join("/home/user/site", path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path}  ({len(html):,} bytes)")
