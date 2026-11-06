# -*- coding: utf-8 -*-
"""توليد صفحات الخدمات الثماني + صفحة محور الخدمات."""
import json
from layout import (BASE, page, write, schema_faq, schema_breadcrumb, ORG)
from gen_parts import icon, crumbs, page_head, cta_block, faq_block
from content_services import SERVICES, BY_SLUG


def build_service(s):
    path = f"/services/{s['slug']}.html"
    url = BASE + path

    # ── جسم الصفحة
    body_parts = [crumbs([("الرئيسية", "/"), ("الخدمات", "/pages/services.html"), (s["h1"], None)]),
                  page_head(s["kicker"], s["h1"], s["lead"])]

    prose = ['<section class="container" style="padding:56px 20px">', '<div class="prose">']
    for head, html in s["sections"]:
        prose.append(f"<h2>{head}</h2>\n{html}")
    prose.append("</div>")

    # FAQ
    prose.append('<div class="prose"><h2>أسئلة شائعة</h2>')
    prose.append(faq_block(s["faq"]))
    prose.append("</div>")

    # CTA + مرتبطة
    prose.append('<div class="prose">')
    prose.append(cta_block())
    rel = [BY_SLUG[r] for r in s["related"] if r in BY_SLUG]
    if rel:
        cards = []
        for r in rel:
            cards.append(f'''<a class="guide-item" href="/services/{r['slug']}.html">
            <h3>{r['h1']}</h3>
            <p>{r['card_desc']}</p>
            <span class="date">خدمة ذات صلة</span>
        </a>''')
        prose.append('<h2>خدمات ذات صلة</h2><div class="guide-list">' + "".join(cards) + "</div>")
    prose.append("</div></section>")
    body_parts.append("\n".join(prose))

    # ── Schema
    service_schema = {
        "@type": "Service",
        "@id": url + "#service",
        "name": s["h1"],
        "serviceType": s["h1"],
        "description": s["desc"],
        "provider": {"@id": BASE + "/#organization"},
        "areaServed": {"@type": "Country", "name": "المملكة العربية السعودية"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": url,
            "availableLanguage": "ar",
        },
        "termsOfService": BASE + "/pages/terms.html",
    }
    faq_schema = schema_faq(s["faq"], url)

    html = page(
        path=path,
        title=s["title"],
        desc=s["desc"],
        h1=s["h1"],
        body="\n".join(body_parts),
        schema_graph=[service_schema, faq_schema],
        breadcrumb=[("الرئيسية", BASE + "/"),
                    ("الخدمات", BASE + "/pages/services.html"),
                    (s["h1"], url)],
        og_image="og-services.jpg",
        active="/pages/services.html",
    )
    write(path, html)


def build_hub():
    """صفحة محور الخدمات /pages/services.html"""
    path = "/pages/services.html"
    url = BASE + path

    cards = []
    for s in SERVICES:
        cards.append(f'''<article class="svc-card">
            <div class="svc-icon">{icon(s["icon"], 24)}</div>
            <div class="meta">{s["meta"]}</div>
            <h3>{s["h1"]}</h3>
            <p>{s["card_desc"]}</p>
            <a class="go" href="/services/{s['slug']}.html">تفاصيل الخدمة {icon("arrow", 16)}</a>
        </article>''')

    body = f'''{crumbs([("الرئيسية", "/"), ("الخدمات", None)])}
{page_head("ثماني خدمات متخصصة", "خدمات الأمن السيبراني",
           "كل خدمة لها صفحة مستقلة تشرح المسار والحدود والمدة المتوقعة. لا نعرض ما لا نستطيع فعله، ونقول ذلك صراحةً قبل أن تطلب.")}
<section class="container" style="padding:56px 20px">
    <div class="svc-grid">
        {"".join(cards)}
    </div>

    <div class="prose" style="margin-top:56px">
        <h2>قبل أن تطلب أي خدمة</h2>
        <p>ثلاثة معايير نلتزم بها في كل تعامل، ونطلب منك أن تتحقق منها عند التعامل مع أي جهة في هذا المجال:</p>
        <div class="table-wrap"><table>
            <thead><tr><th>المعيار</th><th>ما نفعله</th><th>علامة الخطر عند الآخرين</th></tr></thead>
            <tbody>
                <tr><td>إثبات الملكية</td><td>نطلب إثبات ملكية الحساب قبل أي عمل</td><td>من يقبل العمل على حساب لا تملكه</td></tr>
                <tr><td>الشفافية في المدة</td><td>نعطي نطاقاً زمنياً واقعياً لا رقماً دقيقاً مضللاً</td><td>«خلال ساعة مضمونة» لكل الحالات</td></tr>
                <tr><td>حدود الخدمة</td><td>نذكر ما لا نستطيعه في كل صفحة</td><td>وعود مطلقة وحماية كاملة</td></tr>
            </tbody>
        </table></div>

        <h2>كيف نعمل؟</h2>
        <ol>
            <li><strong>تسمعنا المشكلة:</strong> نفهم الحالة والمنصة وقيود الوقت.</li>
            <li><strong>تقييم أولي:</strong> نحدد إن كانت الحالة قابلة للمعالجة وما المسار الواقعي.</li>
            <li><strong>تقرير مكتوب:</strong> المدة المتوقعة، درجة الاحتمال، والرسوم — قبل البدء.</li>
            <li><strong>موافقتك:</strong> لا يبدأ أي عمل قبل موافقة صريحة على التقرير.</li>
            <li><strong>التنفيذ والمتابعة:</strong> مع نقاط تحديث واضحة خلال العمل.</li>
        </ol>
        <div class="callout callout-info">
            <strong>الدفع</strong>
            لا يُدفع شيء قبل رؤية التقرير والموافقة عليه. بالنسبة للعملاء الجدد قد نطلب ضماناً بسيطاً أو دفعة عند إتمام نصف العمل وتوثيقه.
        </div>
        {cta_block()}
    </div>
</section>'''

    item_list = {
        "@type": "ItemList",
        "@id": url + "#services",
        "name": "خدمات فريق أبو نواف للأمن السيبراني",
        "itemListElement": [{
            "@type": "ListItem",
            "position": i,
            "name": s["h1"],
            "url": f"{BASE}/services/{s['slug']}.html",
        } for i, s in enumerate(SERVICES, start=1)],
    }

    html = page(
        path=path,
        title="خدمات الأمن السيبراني | أبو نواف",
        desc="ثماني خدمات متخصصة: استعادة الحسابات، مكافحة الابتزاز، OSINT، فحص أمني، تأمين الحسابات. تقرير مكتوب قبل البدء.",
        h1="خدمات الأمن السيبراني",
        body=body,
        schema_graph=[item_list],
        breadcrumb=[("الرئيسية", BASE + "/"), ("الخدمات", url)],
        og_image="og-services.jpg",
        active="/pages/services.html",
    )
    write(path, html)


if __name__ == "__main__":
    print("توليد صفحات الخدمات:")
    build_hub()
    for s in SERVICES:
        build_service(s)
