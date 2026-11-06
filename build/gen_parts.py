# -*- coding: utf-8 -*-
"""أيقونات SVG مضمّنة + أجزاء HTML مشتركة."""

ICONS = {
    "key": '<path d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "ban": '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M5.6 5.6l12.8 12.8" stroke="currentColor" stroke-width="2"/>',
    "shield-alert": '<path d="M12 3l7 3v5c0 4.5-3 8.4-7 10-4-1.6-7-5.5-7-10V6l7-3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 8v4m0 3h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "search": '<circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "user-x": '<circle cx="9" cy="8" r="3.5" stroke="currentColor" stroke-width="2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M17 9l4 4m0-4l-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2.5" stroke="currentColor" stroke-width="2"/><path d="M8 10V7a4 4 0 018 0v3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "shield-check": '<path d="M12 3l7 3v5c0 4.5-3 8.4-7 10-4-1.6-7-5.5-7-10V6l7-3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 11.5l2.2 2.2L15.5 9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "message": '<path d="M21 12a8 8 0 01-8 8H7l-4 3v-4.5A8 8 0 0113 4a8 8 0 018 8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    "clock": '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3.5 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "bolt": '<path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 016.5 3H20v16H6.5A2.5 2.5 0 004 21.5v-16z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8 7h8M8 11h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "alert-tri": '<path d="M12 4l9 16H3l9-16z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 10v4m0 3h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "check": '<path d="M5 13l4.5 4.5L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    "arrow": '<path d="M14 6l-6 6 6 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
    "telegram": '<path d="M21.5 4.3L2.9 11.6c-.8.3-.8 1.4.1 1.6l4.6 1.4 1.8 5.4c.2.7 1.1.9 1.6.3l2.5-2.9 4.7 3.5c.6.4 1.5.1 1.6-.7l3-14.6c.2-.9-.7-1.6-1.5-1.3z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    "whatsapp": '<path fill="currentColor" stroke="none" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><circle cx="17.2" cy="6.8" r="1.3" fill="currentColor" stroke="none"/>',
    "tiktok": '<path fill="currentColor" stroke="none" d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64c.3 0 .6.05.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1.04-.1z"/>',
    "x": '<path fill="currentColor" stroke="none" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.45-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/>',
    "snapchat": '<path fill="currentColor" stroke="none" d="M12 2.2c2.9 0 4.9 2.1 4.9 5 0 .7-.04 1.4-.1 2.1.5.2 1-.3 1.5-.3.6 0 1 .4 1 .8 0 .6-.8.9-1.4 1.2-.4.2-.6.5-.5.9.3 1.3 1.6 2.6 3 3-.2.7-1.6 1-2.5 1.2-.2.5-.3 1.1-.6 1.1-.5 0-1.1-.3-2-.3-.7 0-1.2.7-2.4.7s-1.7-.7-2.4-.7c-.9 0-1.5.3-2 .3-.3 0-.4-.6-.6-1.1-.9-.2-2.3-.5-2.5-1.2 1.4-.4 2.7-1.7 3-3 .1-.4-.1-.7-.5-.9-.6-.3-1.4-.6-1.4-1.2 0-.4.4-.8 1-.8.5 0 1 .5 1.5.3-.06-.7-.1-1.4-.1-2.1 0-2.9 2-5 4.9-5z"/>',
    "facebook": '<path fill="currentColor" stroke="none" d="M24 12.073C24 5.446 18.627.073 12 .073S0 5.446 0 12.073c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.13.96.36 1.9.7 2.8a2 2 0 01-.45 2.1L8.1 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.45c.9.34 1.84.57 2.8.7A2 2 0 0122 16.9z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
}


# رقم الواتساب الرسمي + روابط التواصل الاجتماعي (مصدر واحد)
WHATSAPP_URL = "https://wa.me/966572851032"
WHATSAPP_TEXT = "https://wa.me/966572851032?text=" + "السلام عليكم، تواصلت معكم من موقع أبو نواف.%20"
PHONE_DISPLAY = "+966 57 285 1032"
PHONE_TEL = "tel:+966572851032"

SOCIAL_LINKS = [
    # (icon, name, url, brand-color)
    ("whatsapp", "واتساب", WHATSAPP_URL, "#25D366"),
    ("telegram", "تيليجرام", "https://t.me/KSA_hack01", "#229ED9"),
    ("snapchat", "سناب شات", "https://www.snapchat.com/add/ant_ceh", "#FFFC00"),
    ("instagram", "إنستقرام", "https://www.instagram.com/ksa_hack01", "#E1306C"),
    ("tiktok", "تيك توك", "https://www.tiktok.com/@ksa_hack01", "#010101"),
    ("x", "إكس (تويتر)", "https://x.com/ksa_hack2", "#000000"),
    ("facebook", "فيسبوك", "https://www.facebook.com/profile.php?id=61554330014413", "#1877F2"),
]


def social_bar(cls="social-bar", label="تواصل معنا مباشرة"):
    """شريط أيقونات التواصل الاجتماعي — يظهر في أعلى الصفحة"""
    items = []
    for ic, name, url, color in SOCIAL_LINKS:
        items.append(
            f'<a class="social-btn" style="--brand:{color}" href="{url}" target="_blank" '
            f'rel="noopener noreferrer" aria-label="{name} — حساب أبو نواف الرسمي" title="{name}">'
            f'{icon(ic, 22)}</a>')
    return (f'<div class="{cls}">\n'
            f'<span class="social-label">{icon("bolt", 16)} {label}</span>\n'
            f'<div class="social-icons">{"".join(items)}</div>\n'
            f'</div>')


def icon(name, size=24, cls=""):
    body = ICONS.get(name, ICONS["check"])
    c = f' class="{cls}"' if cls else ""
    return (f'<svg viewBox="0 0 24 24" fill="none" width="{size}" height="{size}"{c} '
            f'aria-hidden="true">{body}</svg>')


def crumbs(items):
    """items: [(label, href|None)]"""
    lis = []
    for label, href in items:
        if href:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{label}</span></li>')
    return ('<nav class="crumbs" aria-label="مسار التنقل"><div class="container">'
            f'<ol>{"".join(lis)}</ol></div></nav>')


def page_head(tag, h1, lead):
    return f'''<header class="page-head">
    <div class="container">
        <span class="tag">{tag}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
    </div>
</header>'''


def cta_block(text="تحتاج مساعدة الآن؟", sub="فريقنا متاح يومياً من 2:30 مساءً حتى منتصف الليل بتوقيت الرياض.",
              label="تواصل عبر تيليجرام", href="https://t.me/KSA_hack01"):
    return f'''<div class="cta-inline">
    <h2>{text}</h2>
    <p>{sub}</p>
    <a href="{href}" target="_blank" rel="noopener">{label}</a>
</div>'''


def faq_block(pairs):
    items = []
    for q, a in pairs:
        items.append(f'''<details class="faq-item">
        <summary>{q}</summary>
        <div class="ans"><p>{a}</p></div>
    </details>''')
    return '<div class="faq-block">\n' + "\n".join(items) + "\n</div>"
