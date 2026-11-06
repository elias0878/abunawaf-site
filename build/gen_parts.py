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
}


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
