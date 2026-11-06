# -*- coding: utf-8 -*-
"""توليد صفحة فهرس الأدلة + صفحات الأدلة الخمس."""
from layout import BASE, page, write, schema_faq
from gen_parts import icon, crumbs, page_head, cta_block, faq_block
from content_guides import GUIDES
from content_services import BY_SLUG

GUIDE_BY_SLUG = {g["slug"]: g for g in GUIDES}


def build_index():
    path = "/guides/index.html"
    url = BASE + path

    items = []
    for g in GUIDES:
        items.append(f'''<a class="guide-item" href="/guides/{g['slug']}.html">
        <h3>{g['h1']}</h3>
        <p>{g['card_desc']}</p>
        <span class="date">{g['kicker']} · {g['read']}</span>
    </a>''')

    body = f'''{crumbs([("الرئيسية", "/"), ("الأدلة", None)])}
{page_head("محتوى تقني مجاني", "الأدلة والحلول",
           "كل ما في هذه الصفحة مكتوب ليكون مفيداً بغض النظر عن اشتراكك بخدمة. إن كان في وسعك حل مشكلتك بنفسك، فهذا أفضل لك — وهذا هو المقصود.")}
<section class="container" style="padding:56px 20px">
    <div class="guide-list">
        {"".join(items)}
    </div>
    <div class="prose" style="margin-top:40px">
        <h2>لماذا نكتب هذه الأدلة مجاناً؟</h2>
        <p>لأن نسبة كبيرة من الحالات التي تصل إلينا كان يمكن تفاديها بالإجراء الصحيح في الوقت الصحيح. المعلومة الجيدة تمنع المشكلة، وإخفاؤها لبيع خدمة يجعل المجال أسوأ للجميع.</p>
        <div class="callout callout-info">
            <strong>تعاون على التحديث</strong>
            هذه الأدلة تُراجع دورياً. إن لاحظت خطأ أو تغيّرت إجراءات منصة، أخبرنا عبر تيليجرام وسنصحح.
        </div>
        {cta_block("لم تجد ما تبحث عنه؟", "اكتب لنا وصف مشكلتك وسنوجهك للدليل المناسب أو نوضح إن كنت تحتاج تدخلاً تقنياً.", "تواصل معنا")}
    </div>
</section>'''

    item_list = {
        "@type": "CollectionPage",
        "@id": url + "#collection",
        "name": "الأدلة والحلول",
        "hasPart": [{
            "@type": "Article",
            "headline": g["h1"],
            "url": f"{BASE}/guides/{g['slug']}.html",
            "datePublished": g["date"],
            "dateModified": "2026-11-06",
        } for g in GUIDES],
    }

    html = page(
        path=path,
        title="أدلة الأمن السيبراني والحماية الرقمية | أبو نواف",
        desc="أدلة عملية مجانية: أول ساعة بعد الاختراق، علامات اختراق سناب شات، المصادقة الثنائية، حذف EXIF، والإبلاغ عن الجرائم الإلكترونية.",
        h1="الأدلة والحلول",
        body=body,
        schema_graph=[item_list],
        breadcrumb=[("الرئيسية", BASE + "/"), ("الأدلة", url)],
        og_image="og-guides.jpg",
        active="/guides/",
    )
    write(path, html)


def build_guide(g):
    path = f"/guides/{g['slug']}.html"
    url = BASE + path

    parts = [crumbs([("الرئيسية", "/"), ("الأدلة", "/guides/"), (g["h1"], None)]),
             page_head(g["kicker"], g["h1"], g["lead"])]

    prose = ['<section class="container" style="padding:56px 20px">', '<div class="prose">']
    prose.append(f'<p style="color:#94a3b8;font-size:.88rem;margin-bottom:2em">'
                 f'نُشر في {g["date"]} · آخر تحديث 2026-11-06 · {g["read"]}</p>')
    for head, html in g["sections"]:
        prose.append(f"<h2>{head}</h2>\n{html}")

    prose.append('<h2>أسئلة شائعة</h2>')
    prose.append(faq_block(g["faq"]))

    # خدمة مرتبطة
    svc = BY_SLUG.get(g.get("related_service"))
    if svc:
        prose.append(f'''<div class="callout callout-info">
        <strong>خدمة ذات صلة</strong>
        <p style="margin:.4em 0 0">إن احتجت تدخلاً تقنياً، اقرأ صفحة
        <a href="/services/{svc['slug']}.html">{svc['h1']}</a> — تشرح المسار والحدود بوضوح.</p>
        </div>''')

    # أدلة أخرى
    others = [x for x in GUIDES if x["slug"] != g["slug"]][:3]
    cards = "".join(f'''<a class="guide-item" href="/guides/{o['slug']}.html">
        <h3>{o['h1']}</h3><p>{o['card_desc']}</p><span class="date">{o['read']}</span></a>''' for o in others)
    prose.append(f'<h2>اقرأ أيضاً</h2><div class="guide-list">{cards}</div>')
    prose.append(cta_block())
    prose.append("</div></section>")
    parts.append("\n".join(prose))   # ← إصلاح: دمج جسم المقال في الصفحة

    article = {
        "@type": "Article",
        "@id": url + "#article",
        "headline": g["h1"],
        "description": g["desc"],
        "url": url,
        "datePublished": g["date"],
        "dateModified": "2026-11-06",
        "inLanguage": "ar",
        "author": {"@id": BASE + "/#organization"},
        "publisher": {"@id": BASE + "/#organization"},
        "mainEntityOfPage": {"@id": url + "#webpage"},
        "image": BASE + "/assets/images/og-guides.jpg",
    }
    faq_schema = schema_faq(g["faq"], url)

    html = page(
        path=path,
        title=g["title"],
        desc=g["desc"],
        h1=g["h1"],
        body="\n".join(parts),
        schema_graph=[article, faq_schema],
        breadcrumb=[("الرئيسية", BASE + "/"), ("الأدلة", BASE + "/guides/"), (g["h1"], url)],
        og_image="og-guides.jpg",
        og_type="article",
        active="/guides/",
    )
    write(path, html)


if __name__ == "__main__":
    print("توليد الأدلة:")
    build_index()
    for g in GUIDES:
        build_guide(g)
