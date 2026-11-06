# -*- coding: utf-8 -*-
"""توليد الصفحات الرئيسية والمحورية."""
from layout import BASE, ORG, page, write, schema_faq, schema_breadcrumb
from gen_parts import icon, crumbs, page_head, cta_block, faq_block
from content_services import SERVICES, BY_SLUG
from content_guides import GUIDES


# ═══════════════════════════════════════════════ الرئيسية
def build_home():
    path = "/index.html"
    url = BASE + "/"

    # أهم 6 خدمات على الرئيسية
    top = [BY_SLUG["recover-stolen-account"], BY_SLUG["anti-blackmail"],
           BY_SLUG["recover-suspended-account"], BY_SLUG["osint-identity"],
           BY_SLUG["account-protection"], BY_SLUG["security-audit"]]
    svc_cards = "".join(f'''<article class="svc-card">
            <div class="svc-icon">{icon(s["icon"], 24)}</div>
            <h3>{s["h1"]}</h3>
            <p>{s["card_desc"]}</p>
            <a class="go" href="/services/{s['slug']}.html">التفاصيل {icon("arrow", 16)}</a>
        </article>''' for s in top)

    guides_rows = "".join(f'''<a class="guide-item" href="/guides/{g['slug']}.html">
            <h3>{g['h1']}</h3><p>{g['card_desc']}</p>
            <span class="date">{g['kicker']} · {g['read']}</span></a>''' for g in GUIDES[:3])

    home_faq = [
        ("من هو أبو نواف؟",
         "فريق سعودي متخصص في الأمن السيبراني وحماية الخصوصية الرقمية، يعمل من الرياض ويقدّم خدمات استعادة الحسابات، مكافحة الابتزاز الإلكتروني، تقييم البصمة الرقمية، والفحص الأمني، للأفراد والشركات داخل المملكة والخليج."),
        ("هل تستعيدون حساباً لا أملكه؟",
         "لا. نطلب إثبات ملكية الحساب قبل أي عمل. أي جهة تعرض العمل على حساب لا تملكه تعرّضك لمخاطر قانونية وتقنية معاً."),
        ("كيف يتم الدفع؟",
         "لا يُدفع شيء قبل استلام تقرير مكتوب يوضح المسار والمدة المتوقعة والرسوم. للعملاء الجدد قد نطلب ضماناً بسيطاً أو دفعة عند إتمام نصف العمل وتوثيقه."),
        ("ما أوقات العمل؟",
         "يومياً من 2:30 مساءً حتى منتصف الليل بتوقيت الرياض، والجمعة عطلة. الطلبات الطارئة (الابتزاز) تُعالج بأولوية."),
        ("هل تقدمون ضماناً بنتيجة 100%؟",
         "لا، ولن يقول لك ذلك أي طرف صادق: القرار النهائي في استعادة الحسابات يعود للمنصة، لا لنا ولا لأي جهة وسيطة."),
    ]

    body = f'''<header class="hero" role="banner">
    <div class="hero-bg-pattern"></div>
    <div class="hero-content">
        <span class="hero-badge">{icon("shield-check", 18)} فريق سعودي متخصص · الرياض</span>
        <h1 class="hero-title">حماية خصوصيتك الرقمية<br>تبدأ بإجراء صحيح</h1>
        <p class="hero-desc">
            فريق أبو نواف يعمل في الأمن السيبراني والاستجابة للحوادث: استعادة الحسابات المخترقة،
            التعامل مع الابتزاز الإلكتروني، وتأمين حساباتك قبل أن تُخترق.
            نُشرح المسار والمدة والحدود قبل البدء — بلا وعود مطلقة.
        </p>
        <div class="hero-actions">
            <a href="https://t.me/KSA_hack01" class="btn btn-primary btn-lg" target="_blank" rel="noopener">
                {icon("telegram", 20)} تواصل عبر تيليجرام
            </a>
            <a href="/pages/services.html" class="btn btn-outline btn-lg">استعراض الخدمات</a>
        </div>
        <div class="hero-stats">
            <div class="stat-item"><div class="stat-number">8</div><div class="stat-label">خدمات متخصصة</div></div>
            <div class="stat-item"><div class="stat-number">2–48</div><div class="stat-label">ساعة حسب الخدمة</div></div>
            <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">سرية تامة</div></div>
        </div>
    </div>
</header>

<section class="container" style="padding:64px 20px">
    <div class="prose" style="max-width:80ch">
        <h2 style="margin-top:0">ابدأ من هنا — الأكثر طلباً</h2>
        <div class="svc-grid">{svc_cards}</div>
        <div class="actions">
            <a href="/pages/services.html" class="btn btn-primary">كل الخدمات الثماني</a>
            <a href="/guides/" class="btn btn-outline">الأدلة المجانية</a>
        </div>
    </div>
</section>

<section class="container" style="padding:0 20px 64px">
    <div class="prose" style="max-width:80ch">
        <h2>أدلة مجانية قد تحل مشكلتك بنفسك</h2>
        <p>نكتب هذه الأدلة لأن كثيراً من الحالات كان يمكن تفاديها بإجراء صحيح في الوقت الصحيح. إن كان بوسعك حلها بنفسك، فهذا أفضل نتيجة.</p>
        <div class="guide-list">{guides_rows}</div>
    </div>
</section>

<section class="container" style="padding:0 20px 64px">
    <div class="prose" style="max-width:80ch">
        <h2>ثلاثة معايير نلتزم بها — تحقق منها عند أي جهة</h2>
        <div class="table-wrap"><table>
            <thead><tr><th>المعيار</th><th>ما نفعله</th><th>علامة الخطر</th></tr></thead>
            <tbody>
                <tr><td>إثبات الملكية</td><td>نطلب إثبات ملكية الحساب قبل أي عمل</td><td>من يعمل على حساب لا تملكه</td></tr>
                <tr><td>الشفافية في المدة</td><td>نطاق زمني واقعي، لا رقم مضلل</td><td>«ساعة مضمونة» لكل الحالات</td></tr>
                <tr><td>حدود الخدمة</td><td>نذكر ما لا نستطيعه في كل صفحة</td><td>وعود مطلقة وحماية كاملة</td></tr>
            </tbody>
        </table></div>

        <h2>أسئلة شائعة</h2>
        {faq_block(home_faq)}
        {cta_block("تحتاج مساعدة الآن؟", "اكتب لنا وصف المشكلة وسنقول بصراحة إن كانت قابلة للمعالجة أم لا.", "تواصل عبر تيليجرام")}
    </div>
</section>'''

    html = page(
        path=path,
        title="أبو نواف — أمن سيبراني وحماية خصوصية | الرياض",
        desc="فريق سعودي للأمن السيبراني: استعادة الحسابات المخترقة، مكافحة الابتزاز الإلكتروني، وتأمين الحسابات. تقرير مكتوب قبل البدء.",
        h1="حماية خصوصيتك الرقمية تبدأ بإجراء صحيح",
        body=body,
        schema_graph=[schema_faq(home_faq, url)],
        breadcrumb=[("الرئيسية", url)],
        og_image="og-default.jpg",
        active="/",
        container=False,
    )
    write(path, html)
    # النسخة النظيفة: /index.html يجب أن يحوّل إلى / (انظر vercel.json)
    return html


# ═══════════════════════════════════════════════ من نحن
def build_about():
    path = "/pages/about.html"
    url = BASE + path

    body = f'''{crumbs([("الرئيسية", "/"), ("من نحن", None)])}
{page_head("من نحن", "فريق أبو نواف للأمن السيبراني",
           "فريق سعودي يعمل في الأمن السيبراني والاستجابة للحوادث من الرياض، ويخدم الأفراد والشركات داخل المملكة والخليج.")}
<section class="container" style="padding:56px 20px">
    <div class="prose">
        <div class="about-hero">
            <img src="/assets/images/logo.jpg" alt="شعار فريق أبو نواف" width="132" height="132" loading="lazy">
            <div class="who">
                <h2>أبو نواف</h2>
                <p>أمن سيبراني · حماية خصوصية · استجابة للحوادث — الرياض، المملكة العربية السعودية</p>
            </div>
        </div>

        <h2>ما نفعله بالضبط</h2>
        <p>ثلاثة مسارات فقط، ونتقنها:</p>
        <ul>
            <li><strong>الاستجابة للحوادث:</strong> حساب مُخترق، بريد مسروق، أو تعرّض لابتزاز إلكتروني. هدفنا الأول احتواء الضرر وتوقفه، ثم الاستعادة الكاملة.</li>
            <li><strong>تقييم البصمة الرقمية:</strong> ما المعلومات المنشورة عنك أو عن شركتك بلا إذنك، ومن قد يستخدمها، وكيف تقللها.</li>
            <li><strong>الفحص الأمني والتأمين:</strong> تقييم أمني للأنظمة والمواقع، وتحصين الحسابات الشخصية والتجارية قبل وقوع الحادث.</li>
        </ul>

        <h2>كيف نعمل — وفلسفتنا في الحدود</h2>
        <p>في هذا المجال تحديداً، <strong>الشفافية عن الحدود هي ما يميّز العمل المهني</strong>. لذلك ستجد في كل صفحة خدمة قسماً بعنوان «ما لا نستطيع فعله». هذه ليست مجاملة: أي جهة تعد بحماية كاملة أو نتيجة مضمونة 100% تبيعك وهماً، والقرار النهائي في استعادة الحسابات يعود للمنصة.</p>
        <div class="callout callout-info">
            <strong>ثلاثة أشياء لا نفعلها أبداً</strong>
            <ul style="margin:.6em 0 0">
                <li>العمل على حساب لا يثبت العميل ملكيته له.</li>
                <li>اختراق أنظمة أو حسابات الغير — هذا جريمة، لا خدمة.</li>
                <li>طلب كلمات مرورك أو رموز التحقق (OTP) الخاصة بك.</li>
            </ul>
        </div>

        <h2>لماذا نكتب محتوى مجانياً؟</h2>
        <p>لأن جزءاً كبيراً من الحالات التي تصلنا كان يمكن تفاديها بإجراء صحيح في الوقت الصحيح. إخفاء المعلومة لبيع خدمة يجعل المجال أسوأ للجميع — والمجال سيئ بما يكفي بسبب من يبيعون الوعود الكاذبة.</p>
        <p>اقرأ <a href="/guides/">الأدلة والحلول</a> — إن حللت مشكلتك بنفسك، فهذا نجاح لا خسارة.</p>

        <h2>أوقات العمل والتواصل</h2>
        <div class="table-wrap"><table>
            <tbody>
                <tr><td><strong>الموقع</strong></td><td>الرياض، المملكة العربية السعودية</td></tr>
                <tr><td><strong>أوقات العمل</strong></td><td>يومياً من 2:30 مساءً إلى 12:00 منتصف الليل (مغلق الجمعة)</td></tr>
                <tr><td><strong>المنطقة الزمنية</strong></td><td>توقيت الرياض (UTC+3)</td></tr>
                <tr><td><strong>اللغات</strong></td><td>العربية والإنجليزية</td></tr>
                <tr><td><strong>القناة الرسمية</strong></td><td><a href="https://t.me/KSA_hack01" target="_blank" rel="noopener">تيليجرام @KSA_hack01</a></td></tr>
            </tbody>
        </table></div>
        <div class="callout callout-warn">
            <strong>الحسابات الرسمية فقط</strong>
            جميع قنواتنا منشورة في <a href="/pages/contact.html">صفحة التواصل</a>. لا نتواصل معك من حساب غير مذكور فيها.
        </div>
        {cta_block()}
    </div>
</section>'''

    org_extra = {
        "@type": "ContactPage",
        "@id": url + "#contactpage",
        "name": "من نحن",
        "url": url,
        "about": {"@id": BASE + "/#organization"},
    }

    html = page(
        path=path,
        title="من نحن — فريق أبو نواف للأمن السيبراني | الرياض",
        desc="من هو فريق أبو نواف: مسارات العمل الثلاثة، فلسفتنا في الحدود والشفافية، وأوقات التواصل الرسمية.",
        h1="فريق أبو نواف للأمن السيبراني",
        body=body,
        schema_graph=[org_extra],
        breadcrumb=[("الرئيسية", BASE + "/"), ("من نحن", url)],
        active="/pages/about.html",
    )
    write(path, html)


# ═══════════════════════════════════════════════ مشكلات وحلول
PROBLEMS = [
    ("hacked", "تم اختراق حسابي", "خطوات فورية لحماية واستعادة حسابك المخترق",
     "ابدأ من البريد المرتبط لا من الحساب نفسه. غيّر كلمة مرور البريد من جهاز نظيف، أنهِ كل الجلسات، وفعّل المصادقة الثنائية. ثم استخدم «نسيت كلمة المرور» الرسمي. لا تحذف التطبيق أو المحادثات لأنها دليلك.",
     "/guides/first-hour-after-account-hack.html", "first-hour-after-account-hack"),
    ("suspended", "حسابي موقوف بدون سبب", "كيف تستعيد حساباً موقوفاً أو محظوراً",
     "لا ترسل أكثر من استئناف أثناء انتظار الرد — التكرار يُغلق ملفك. استئناف واحد بذكر الوقائع والوقت والتفسير التقني أقوى بكثير من خمسة استئنافات عاطفية.",
     "/services/recover-suspended-account.html", "recover-suspended-account"),
    ("blackmail", "أتعرض لابتزاز إلكتروني", "إجراءات طارئة وفورية لحماية نفسك",
     "لا تدفع، ولا تحذف المحادثة، ولا ترسل صورة إضافية. وثّق كل شيء بلقطة أو تسجيل شاشة، وأمّن حساباتك، وأبلغ عبر قناة «التهديد والتحرش» في المنصة ثم المسار الرسمي.",
     "/services/anti-blackmail.html", "anti-blackmail"),
    ("weak-password", "كيف أنشئ كلمة مرور قوية؟", "أساسيات حماية حساباتك من الاختراق",
     "الطول أهم من التعقيد. 16 محرفاً عشوائياً من مدير كلمات مرور أفضل من كلمة معقدة تحفظها في ذاكرتك وتكررها في كل المواقع. والأهم: كلمة فريدة لكل حساب.",
     "/guides/two-factor-authentication-guide.html", "two-factor-authentication-guide"),
    ("deceased", "إغلاق حساب شخص متوفي", "خطوات إغلاق وحذف حسابات المتوفين رسمياً",
     "تحتاج شهادة وفاة رسمية (مترجمة عند تقديمها لمنصة أجنبية)، إثبات صلة قرابة، وهويات. الفرق بين «حذف» و«حساب تذكاري» جوهري ولا رجعة في الأول.",
     "/services/deceased-account.html", "deceased-account"),
    ("phishing", "وصلتني رسالة مشبوهة", "كيف تعرف التصيّد وتحتمي منه",
     "لا تضغط الرابط. افتح الخدمة بنفسك من التطبيق الرسمي. تحقق من مرسل الرسالة الحقيقي لا الاسم المعروض. أي جهة تطلب رمز تحقق أو كلمة مرور هي جهة احتيال — بلا استثناء.",
     "/guides/first-hour-after-account-hack.html", "first-hour-after-account-hack"),
    ("snapchat", "أشك أن سناب شات مخترق", "العلامات السبع الفعلية للاختراق الصامت",
     "أخطر الاختراقات ما يحدث بهدوء. راجع تنبيهات الدخول في بريدك، وسجل المحادثات، وبيانات الهاتف والبريد المرتبطين. ثم أعد تعيين كلمة المرور وأنهِ كل الجلسات.",
     "/guides/signs-your-snapchat-is-hacked.html", "signs-your-snapchat-is-hacked"),
    ("exif", "صوري تكشف موقعي", "كيف تحذف بيانات EXIF قبل النشر",
     "صور الهاتف تحمل إحداثيات GPS ووقت التصوير وطراز الجهاز. أوقف وسم الموقع من إعدادات الكاميرا، واحذف البيانات قبل النشر، أو استخدم لقطة شاشة بدلاً من الملف الأصلي.",
     "/guides/protect-photos-exif-location.html", "protect-photos-exif-location"),
    ("report", "أريد الإبلاغ عن جريمة إلكترونية", "المسار الرسمي في السعودية",
     "جهّز الملف قبل البلاغ: معرّف الجاني، نص التهديد، التاريخ والوقت، وإثبات ملكية الحساب. البلاغ الذي يُرفض غالباً ليس ضعفاً قانونياً بل ضعف توثيق.",
     "/guides/saudi-cybercrime-report-guide.html", "saudi-cybercrime-report-guide"),
    ("audit", "أريد فحص موقعي أمنياً", "تقييم أمني واختبار اختراق أخلاقي",
     "الفحص الأخلاقي يبدأ بتفويض مكتوب. القيمة الحقيقية في التقرير: ما الثغرة، ما أثرها على عملك، وما ترتيب إصلاحها بحسب الخطر لا بحسب سهولة اكتشافها.",
     "/services/security-audit.html", "security-audit"),
]


def build_problems():
    path = "/pages/problems.html"
    url = BASE + path

    items = "".join(
        f'<div class="svc-card" id="{p[0]}"><h3>{p[2]}</h3><p>{p[3]}</p>'
        f'<a class="go" href="{p[4]}">الحل الكامل {icon("arrow", 16)}</a></div>'
        for p in PROBLEMS)

    faq_pairs = []
    for pid, title, summary, detail, link, slug in PROBLEMS:
        faq_pairs.append((title, detail))

    body = f'''{crumbs([("الرئيسية", "/"), ("مشكلات وحلول", None)])}
{page_head("حلول سريعة", "مشكلات وحلول",
           "عشر مشكلات شائعة مع الحل المباشر لكل واحدة. ابدأ من هنا قبل التواصل — قد تُحل مشكلتك في دقيقتين.")}
<section class="container" style="padding:56px 20px">
    <div class="svc-grid">
        {items}
    </div>
    <div class="prose" style="margin-top:48px">
        <h2>القاعدة العامة في كل الحالات</h2>
        <ol>
            <li><strong>لا تتحرك بسرعة.</strong> أغلب الأخطاء تحدث في أول عشر دقائق من الذعر.</li>
            <li><strong>وثّق قبل أن تُصلح.</strong> الإصلاح المتعجل يمسح أدلتك.</li>
            <li><strong>لا تدفع ولا تسلّم بيانات</strong> لأي طرف لم تتحقق منه.</li>
            <li><strong>ابدأ من البريد الإلكتروني</strong> — فهو مفتاح كل الحسابات المرتبطة.</li>
        </ol>
        {cta_block("مشكلتك غير موجودة هنا؟", "اكتب لنا وصفاً مختصراً وسنوضح إن كان في وسعنا مساعدتك أو نوجهك للمسار الصحيح.", "تواصل معنا")}
    </div>
</section>'''

    html = page(
        path=path,
        title="مشكلات وحلول سريعة | أبو نواف",
        desc="عشر مشكلات شائعة وحلولها المباشرة: اختراق حساب، إيقاف، ابتزاز، تصيّد، EXIF، والإبلاغ عن جريمة إلكترونية.",
        h1="مشكلات وحلول",
        body=body,
        schema_graph=[schema_faq(faq_pairs, url)],
        breadcrumb=[("الرئيسية", BASE + "/"), ("مشكلات وحلول", url)],
        active="/pages/problems.html",
    )
    write(path, html)


# ═══════════════════════════════════════════════ تواصل
SOCIALS = [
    ("تيليجرام", "@KSA_hack01", "https://t.me/KSA_hack01", "الأسرع — القناة الرسمية والموصى بها"),
    ("سناب شات", "ant_ceh", "https://www.snapchat.com/add/ant_ceh", "متاح"),
    ("إنستقرام", "@ksa_hack01", "https://www.instagram.com/ksa_hack01", "متاح"),
    ("تيك توك", "@ksa_hack01", "https://www.tiktok.com/@ksa_hack01", "متاح"),
    ("إكس (تويتر)", "@ksa_hack2", "https://twitter.com/ksa_hack2", "متاح"),
    ("فيسبوك", "صفحتنا الرسمية", "https://www.facebook.com/profile.php?id=61554330014413", "متاح"),
    ("GitHub", "elias0878", "https://github.com/elias0878", "مشاريع مفتوحة"),
]


def build_contact():
    path = "/pages/contact.html"
    url = BASE + path

    cards = "".join(f'''<a class="svc-card" href="{url_}" target="_blank" rel="noopener">
            <h3>{name}</h3>
            <div class="meta">{handle}</div>
            <p>{note}</p>
            <span class="go">فتح القناة {icon("arrow", 16)}</span>
        </a>''' for name, handle, url_, note in SOCIALS)

    body = f'''{crumbs([("الرئيسية", "/"), ("تواصل", None)])}
{page_head("قنوات رسمية", "تواصل معنا",
           "هذه هي قنواتنا الرسمية الوحيدة. أي حساب يتواصل معك باسم الفريق وغير مذكور هنا ليس تابعاً لنا.")}
<section class="container" style="padding:56px 20px">
    <div class="svc-grid">
        {cards}
    </div>
    <div class="prose" style="margin-top:48px">
        <h2>قبل أن ترسل — جهّز هذه المعلومات</h2>
        <p>رسالة منظمة توفر ساعة كاملة من الأسئلة، وتساعدنا على إعطائك تقييماً واقعياً من أول رد:</p>
        <ul>
            <li><strong>نوع المشكلة:</strong> اختراق، إيقاف، ابتزاز، فحص أمني… إلخ.</li>
            <li><strong>المنصة:</strong> سناب شات، إنستغرام، إكس، موقعك الخاص… إلخ.</li>
            <li><strong>متى بدأت:</strong> التاريخ والوقت التقريبي.</li>
            <li><strong>هل البريد المرتبط ما زال تحت سيطرتك؟</strong> (سؤال يحدد المسار كله)</li>
            <li><strong>هل وثّقت الأدلة؟</strong> نعم/لا.</li>
        </ul>
        <div class="callout callout-danger">
            <strong>لا ترسل لنا أبداً</strong>
            كلمات مرورك، رموز التحقق (OTP)، صور هويتك الكاملة، أو أي بيانات دفع عبر تطبيق مراسلة عادي. لا نطلبها في أي مرحلة من العمل.
        </div>

        <h2>أوقات العمل</h2>
        <div class="table-wrap"><table>
            <thead><tr><th>اليوم</th><th>الوقت (توقيت الرياض)</th></tr></thead>
            <tbody>
                <tr><td>الأحد – الخميس</td><td>2:30 مساءً – 12:00 منتصف الليل</td></tr>
                <tr><td>السبت</td><td>2:30 مساءً – 12:00 منتصف الليل</td></tr>
                <tr><td>الجمعة</td><td>مغلق</td></tr>
                <tr><td>حالات الابتزاز</td><td>تُعالج بأولوية حتى خارج نطاق العمل</td></tr>
            </tbody>
        </table></div>
        {cta_block("أسرع قناة للتواصل", "تيليجرام هو الأسرع والأكثر أماناً للأسئلة التقنية.", "فتح تيليجرام @KSA_hack01")}
    </div>
</section>'''

    contact = {
        "@type": "ContactPage",
        "@id": url + "#contactpage",
        "name": "تواصل معنا",
        "url": url,
        "about": {"@id": BASE + "/#organization"},
    }
    html = page(
        path=path,
        title="تواصل معنا — القنوات الرسمية | أبو نواف",
        desc="القنوات الرسمية الوحيدة للتواصل مع فريق أبو نواف: تيليجرام، سناب شات، إنستقرام، تيك توك، إكس. أوقات العمل بتوقيت الرياض.",
        h1="تواصل معنا",
        body=body,
        schema_graph=[contact],
        breadcrumb=[("الرئيسية", BASE + "/"), ("تواصل معنا", url)],
        active="/pages/contact.html",
    )
    write(path, html)


# ═══════════════════════════════════════════════ الشروط
def build_terms():
    path = "/pages/terms.html"
    url = BASE + path

    body = f'''{crumbs([("الرئيسية", "/"), ("الشروط والأحكام", None)])}
{page_head("الشروط والأحكام", "شروط الخدمة ونظام العمل",
           "ما تلتزم به وما تطلبه منك، وما لا نقدّمه إطلاقاً. هذه الشروط جزء من العقد لا ملحق تجميلي.")}
<section class="container" style="padding:56px 20px">
    <div class="prose">
        <p style="color:#94a3b8;font-size:.88rem">آخر تحديث: 2026-11-06</p>

        <h2>1. نطاق الخدمة</h2>
        <p>نقدّم خدمات تقنية في الأمن السيبراني وحماية الخصوصية والاستجابة للحوادث، للأفراد والشركات. لا نقدّم استشارات قانونية، ولا نعمل بديلاً عن الجهات الرسمية المختصة.</p>

        <h2>2. ما لا نقدّمه — بشكل قاطع</h2>
        <div class="callout callout-danger">
            <ul style="margin:0">
                <li>اختراق أي حساب أو نظام لا يملكه العميل أو لا يملك تفويضاً كتابياً به.</li>
                <li>الوصول إلى بيانات خاصة لأطراف ثالثة.</li>
                <li>كشف هوية شخص بهدف الإيذاء أو الانتقام أو التشهير.</li>
                <li>حذف محتوى من الإنترنت مقابل ضمان — لا أحد يستطيع ذلك فعلياً.</li>
                <li>أي عمل يتعارض مع نظام مكافحة الجرائم المعلوماتية في المملكة العربية السعودية.</li>
            </ul>
        </div>
        <p>الطلب الذي يقع في هذه الفئة يُرفض فوراً، ويُعاد أي مبلغ دُفع مقابله.</p>

        <h2>3. إثبات الملكية</h2>
        <p>قبل أي عمل على حساب أو نظام، يجب إثبات ملكيته أو تقديم تفويض رسمي. نطلب عادة أدلة من نوع: بريد الإنشاء، رقم هاتف سابق، إيصالات دفع، أو تفويض موقّع من مالك النظام. بلا هذا الإثبات لا يبدأ العمل.</p>

        <h2>4. التقييم والرسوم</h2>
        <ul>
            <li>نقدّم تقريراً مكتوباً قبل البدء يوضح المدة المتوقعة ودرجة الاحتمال والرسوم.</li>
            <li>لا يبدأ التنفيذ قبل موافقة صريحة على التقرير.</li>
            <li>العملاء الجدد: قد نطلب ضماناً بسيطاً أو دفعة عند إتمام نصف العمل وتوثيقه.</li>
            <li>الرسوم تُحدد في التقرير، ولا تُضاف مبالغ مفاجئة لاحقاً.</li>
        </ul>

        <h2>5. حدود النتائج</h2>
        <div class="callout callout-warn">
            <strong>لا نضمن نتيجة بنسبة 100%</strong>
            في استعادة الحسابات، القرار النهائي يعود للمنصة لا لنا. في الفحص الأمني، قد تكون النتيجة «لا ثغرات حرجة». ما نضمنه هو بذل العمل وفق أفضل الممارسات، وتقديم تقرير صادق بالنتيجة الفعلية.
        </div>

        <h2>6. السرية</h2>
        <p>لا نشارك بيانات العميل أو تفاصيل قضيته مع أي طرف ثالث. لا نحتفظ بالأدلة الحساسة بعد انتهاء العمل. يمكن إبرام اتفاقية عدم إفصاح (NDA) مكتوبة عند الحاجة.</p>

        <h2>7. الاستخدام المقبول</h2>
        <p>تلتزم بعدم استخدام أي خدمة أو أداة أو معلومة تُقدَّم لك في نشاط غير مشروع، وبتقديم معلومات صحيحة عن ملكية الأصول المطلوب العمل عليها.</p>

        <h2>8. الإبلاغ عن الجرائم</h2>
        <p>نشجّع وبقوة على تقديم البلاغ الرسمي للجهات المختصة في حالات الاختراق والابتزاز. تسجيل الواقعة رسمياً يحمي حقوقك ويجعل معالجة الملف أكثر فاعلية.</p>

        <h2>9. التعديلات</h2>
        <p>قد تُحدّث هذه الشروط. النسخة السارية هي المنشورة على هذه الصفحة، مع تاريخ التحديث أعلاه.</p>

        <h2>10. التواصل</h2>
        <p>أي استفسار عن هذه الشروط عبر <a href="https://t.me/KSA_hack01" target="_blank" rel="noopener">القناة الرسمية</a>.</p>
        {cta_block()}
    </div>
</section>'''

    html = page(
        path=path,
        title="الشروط والأحكام ونظام العمل | أبو نواف",
        desc="شروط الخدمة: نطاق العمل، إثبات الملكية، الرسوم، حدود النتائج، السرية، وما لا نقدّمه بشكل قاطع.",
        h1="شروط الخدمة ونظام العمل",
        body=body,
        schema_graph=[],
        breadcrumb=[("الرئيسية", BASE + "/"), ("الشروط والأحكام", url)],
    )
    write(path, html)


# ═══════════════════════════════════════════════ الخصوصية
def build_privacy():
    path = "/pages/privacy.html"
    url = BASE + path

    body = f'''{crumbs([("الرئيسية", "/"), ("سياسة الخصوصية", None)])}
{page_head("الخصوصية", "سياسة الخصوصية",
           "ما نجمعه من بيانات عند استخدامك هذا الموقع، ولماذا، وكيف يُخزَّن — مكتوبة بلغة واضحة لا بلغة قانونية مطاطة.")}
<section class="container" style="padding:56px 20px">
    <div class="prose">
        <p style="color:#94a3b8;font-size:.88rem">آخر تحديث: 2026-11-06</p>

        <h2>1. ما لا نجمعه</h2>
        <div class="callout callout-success">
            <ul style="margin:0">
                <li>لا يوجد نموذج تسجيل ولا حسابات مستخدمين على هذا الموقع.</li>
                <li>لا نجمع أسماء أو عناوين بريد أو أرقام هواتف عبر الموقع.</li>
                <li>لا نستخدم أدوات تتبّع إعلانية.</li>
                <li>لا نبيع أي بيانات — لا توجد بيانات نبيعها.</li>
            </ul>
        </div>

        <h2>2. ما قد يُسجَّل تلقائياً</h2>
        <p>مزوّد الاستضافة (Vercel) قد يسجّل بيانات تشغيل قياسية مثل: عنوان IP، وقت الطلب، المسار المطلوب، ونوع المتصفح. هذه سجلات تقنية تُستخدم لسلامة الخدمة ومنع الإساءة، وليست للتحليل التجاري.</p>

        <h2>3. الخطوط والموارد الخارجية</h2>
        <p>نستخدم خط Google Fonts لتحسين مظهر النصوص العربية. عند تحميل الخط، يتصل متصفحك بخوادم Google التي قد تسجّل عنوان IP وفق سياسة الخصوصية الخاصة بها. لا نستخدم أي موارد خارجية أخرى.</p>

        <h2>4. الروابط الخارجية</h2>
        <p>الموقع يحتوي روابط لقنوات مراسلة ومنصات تواصل خارجية (تيليجرام، سناب شات، إنستقرام، إكس… إلخ). بمجرد انتقالك إليها، تُطبَّق سياسات تلك المنصات لا سياستنا. ننصحك بمراجعتها.</p>

        <h2>5. إذا تواصلت معنا</h2>
        <p>عند مراسلتنا، تشارك أنت ببيانات التواصل معنا (اسم مستخدم، تفاصيل المشكلة، وقد تتضمن أدلة). نلتزم بما يلي:</p>
        <ul>
            <li>عدم مشاركة هذه البيانات مع أي طرف ثالث.</li>
            <li>عدم الاحتفاظ بالأدلة الحساسة بعد انتهاء العمل.</li>
            <li>إتلاف ما نحتفظ به عند طلبك، ما لم يكن هناك التزام نظامي يمنع ذلك.</li>
        </ul>

        <h2>6. ملفات تعريف الارتباط (Cookies)</h2>
        <p>لا يستخدم هذا الموقع ملفات تعريف ارتباط للتتبّع أو الإعلانات. أي ملفات قد تُخزَّن من مزوّد الاستضافة هي لأغراض تقنية بحتة.</p>

        <h2>7. حقوقك</h2>
        <p>يمكنك طلب معرفة ما نحتفظ به عنك، أو طلب حذفه. راسلنا عبر <a href="https://t.me/KSA_hack01" target="_blank" rel="noopener">القناة الرسمية</a>.</p>

        <h2>8. الأطفال</h2>
        <p>الخدمات موجّهة لمن هم 18 عاماً فأكثر. لا نجمع بيانات عن أطفال عن قصد. إن كنت ولي أمر وتعتقد أن طفلاً شارك بيانات معنا، تواصل معنا لإزالتها.</p>
        {cta_block("لديك سؤال عن الخصوصية؟", "راسلنا وسنوضح أي نقطة تحتاج إيضاحاً.", "تواصل معنا")}
    </div>
</section>'''

    html = page(
        path=path,
        title="سياسة الخصوصية | أبو نواف",
        desc="سياسة خصوصية واضحة: ما لا نجمعه، السجلات التقنية، الموارد الخارجية، وحقوقك في الحذف.",
        h1="سياسة الخصوصية",
        body=body,
        schema_graph=[],
        breadcrumb=[("الرئيسية", BASE + "/"), ("سياسة الخصوصية", url)],
    )
    write(path, html)


# ═══════════════════════════════════════════════ 404
def build_404():
    path = "/404.html"
    top = [BY_SLUG["recover-stolen-account"], BY_SLUG["anti-blackmail"], BY_SLUG["account-protection"]]
    cards = "".join(f'''<a class="guide-item" href="/services/{s['slug']}.html">
        <h3>{s['h1']}</h3><p>{s['card_desc']}</p></a>''' for s in top)

    body = f'''<section class="container" style="padding:80px 20px;text-align:center">
    <div style="max-width:640px;margin:0 auto">
        <div style="font-size:5rem;font-weight:900;color:#d6b256;line-height:1">404</div>
        <h1 style="font-size:1.9rem;color:#1a365d;margin:16px 0">الصفحة غير موجودة</h1>
        <p style="color:#64748b;line-height:1.9">
            الصفحة التي تبحث عنها نُقلت أو لم تعد موجودة. هذا خطأنا لا خطأك —
            يمكنك البدء من أحد الروابط التالية، أو إخبارنا عبر تيليجرام.
        </p>
        <div class="actions" style="justify-content:center;margin-bottom:2.5em">
            <a href="/" class="btn btn-primary">الصفحة الرئيسية</a>
            <a href="/pages/services.html" class="btn btn-outline">الخدمات</a>
            <a href="/guides/" class="btn btn-outline">الأدلة</a>
        </div>
        <div class="guide-list" style="text-align:right">{cards}</div>
    </div>
</section>'''

    html = page(
        path=path,
        title="الصفحة غير موجودة | أبو نواف",
        desc="الصفحة المطلوبة غير موجودة. ابدأ من الصفحة الرئيسية أو تصفّح الخدمات والأدلة.",
        h1="الصفحة غير موجودة",
        body=body,
        schema_graph=[],
        noindex=True,
        container=False,
    )
    write(path, html)


if __name__ == "__main__":
    print("توليد الصفحات:")
    build_home()
    build_about()
    build_problems()
    build_contact()
    build_terms()
    build_privacy()
    build_404()
