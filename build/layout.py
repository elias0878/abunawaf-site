# -*- coding: utf-8 -*-
"""
نظام البناء — قوالب الصفحات المشتركة
كل صفحة تُولَّد من هنا لضمان تناسق الوسوم (title/desc/canonical/schema).
"""
from html import escape

BASE = "https://ant.xo.je"
WHATSAPP_URL = "https://wa.me/966572851032"
WHATSAPP_TEXT = "https://wa.me/966572851032?text=" + "السلام عليكم، تواصلت معكم من موقع أبو نواف.%20"
PHONE = "+966572851032"
PHONE_DISPLAY = "+966 57 285 1032"

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
        "https://wa.me/966572851032",
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
        "telephone": PHONE,
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "customer support",
            "contactOption": "TollFree",
            "availableLanguage": ["ar", "en"],
            "areaServed": "SA",
        }],
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
         extra_head="", keywords=None, container=True, active="/", url_override=None):
    """
    path      : مسار الصفحة من الجذر، مثل "/pages/services.html"
    schema_graph: قائمة كيانات (بدون @context) تُدمج مع Organization و WebSite
    """
    url = url_override or (BASE + path)
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

    body_inner = f'<main id="main-content">\n{body}\n</main>' if container else f'<div id="main-content">{body}</div>'

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
    <meta property="og:updated_time" content="2026-11-06T12:00:00+03:00">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:creator" content="@ksa_hack2">
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
    <link rel="preload" href="/css/main.css" as="style">
    <link rel="preload" href="/assets/images/logo.jpg" as="image" fetchpriority="high">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/extra.css">
    <link rel="dns-prefetch" href="//wa.me">
    <link rel="preconnect" href="https://wa.me">
    <link rel="preconnect" href="https://t.me">
    <meta name="color-scheme" content="light">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="أبو نواف">
    <!-- تحقق محركات البحث: استبدل القيم below برموزك من Google Search Console وBing Webmaster -->
    <meta name="google-site-verification" content="GOOGLE_VERIFICATION_CODE_HERE">
    <meta name="msvalidate.01" content="BING_VERIFICATION_CODE_HERE">
{extra_head}
    <script type="application/ld+json">{ld}</script>
</head>
<body>
    <a class="skip-link" href="#main-content">تخطي إلى المحتوى الرئيسي</a>
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
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                        <a href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer">واتساب: {PHONE_DISPLAY}</a>
                    </div>
                    <div class="footer-contact-item">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.13.96.36 1.9.7 2.8a2 2 0 01-.45 2.1L8.1 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.45c.9.34 1.84.57 2.8.7A2 2 0 0122 16.9z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        <a href="tel:{PHONE}" dir="ltr">{PHONE_DISPLAY}</a>
                    </div>
                    <div class="footer-social">
                        <span>تابعنا:</span>
                        <div class="social-icons">
                            <a class="social-btn" style="--brand:#25D366" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer" aria-label="واتساب" title="واتساب"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path fill="currentColor" stroke="none" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
                            <a class="social-btn" style="--brand:#229ED9" href="https://t.me/KSA_hack01" target="_blank" rel="noopener noreferrer" aria-label="تيليجرام" title="تيليجرام"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path d="M21.5 4.3L2.9 11.6c-.8.3-.8 1.4.1 1.6l4.6 1.4 1.8 5.4c.2.7 1.1.9 1.6.3l2.5-2.9 4.7 3.5c.6.4 1.5.1 1.6-.7l3-14.6c.2-.9-.7-1.6-1.5-1.3z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg></a>
                            <a class="social-btn" style="--brand:#E1306C" href="https://www.instagram.com/ksa_hack01" target="_blank" rel="noopener noreferrer" aria-label="إنستقرام" title="إنستقرام"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><circle cx="17.2" cy="6.8" r="1.3" fill="currentColor" stroke="none"/></svg></a>
                            <a class="social-btn" style="--brand:#010101" href="https://www.tiktok.com/@ksa_hack01" target="_blank" rel="noopener noreferrer" aria-label="تيك توك" title="تيك توك"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path fill="currentColor" stroke="none" d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64c.3 0 .6.05.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1.04-.1z"/></svg></a>
                            <a class="social-btn" style="--brand:#FFFC00" href="https://www.snapchat.com/add/ant_ceh" target="_blank" rel="noopener noreferrer" aria-label="سناب شات" title="سناب شات"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path fill="currentColor" stroke="none" d="M12 2.2c2.9 0 4.9 2.1 4.9 5 0 .7-.04 1.4-.1 2.1.5.2 1-.3 1.5-.3.6 0 1 .4 1 .8 0 .6-.8.9-1.4 1.2-.4.2-.6.5-.5.9.3 1.3 1.6 2.6 3 3-.2.7-1.6 1-2.5 1.2-.2.5-.3 1.1-.6 1.1-.5 0-1.1-.3-2-.3-.7 0-1.2.7-2.4.7s-1.7-.7-2.4-.7c-.9 0-1.5.3-2 .3-.3 0-.4-.6-.6-1.1-.9-.2-2.3-.5-2.5-1.2 1.4-.4 2.7-1.7 3-3 .1-.4-.1-.7-.5-.9-.6-.3-1.4-.6-1.4-1.2 0-.4.4-.8 1-.8.5 0 1 .5 1.5.3-.06-.7-.1-1.4-.1-2.1 0-2.9 2-5 4.9-5z"/></svg></a>
                            <a class="social-btn" style="--brand:#000000" href="https://x.com/ksa_hack2" target="_blank" rel="noopener noreferrer" aria-label="إكس" title="إكس"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path fill="currentColor" stroke="none" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.45-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg></a>
                            <a class="social-btn" style="--brand:#1877F2" href="https://www.facebook.com/profile.php?id=61554330014413" target="_blank" rel="noopener noreferrer" aria-label="فيسبوك" title="فيسبوك"><svg viewBox="0 0 24 24" fill="none" width="18" height="18" aria-hidden="true"><path fill="currentColor" stroke="none" d="M24 12.073C24 5.446 18.627.073 12 .073S0 5.446 0 12.073c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">2026</span> فريق أبو نواف للأمن السيبراني — جميع الحقوق محفوظة.</p>
            </div>
        </div>
    </footer>

    <a class="wa-float" href="{WHATSAPP_TEXT}" target="_blank" rel="noopener noreferrer"
       aria-label="تواصل عبر واتساب على الرقم {PHONE_DISPLAY}">
        <svg viewBox="0 0 24 24" fill="none" width="30" height="30" aria-hidden="true"><path fill="currentColor" stroke="none" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        <span class="wa-float-text">واتساب<br><b dir="ltr">{PHONE_DISPLAY}</b></span>
    </a>

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
