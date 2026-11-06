# موقع فريق أبو نواف للأمن السيبراني

موقع رسمي — أمن سيبراني، حماية خصوصية، واستجابة للحوادث.
مبني كموقع ثابت (HTML/CSS/JS) ومنشور على Vercel.

## البنية

```
/                     الصفحة الرئيسية
/pages/services.html  محور الخدمات (8 خدمات)
/services/*.html      صفحات الخدمات المستقلة
/guides/              فهرس الأدلة
/guides/*.html        الأدلة الخمسة
/pages/about.html     من نحن
/pages/problems.html  مشكلات وحلول (10 مشاكل)
/pages/contact.html   القنوات الرسمية
/pages/privacy.html   سياسة الخصوصية
/pages/terms.html     الشروط والأحكام
/404.html             صفحة 404 (بترميز 404 حقيقي)
```

## نظام البناء

مجلد `build/` يحتوي مولّدات بايثون تُنتج الصفحات من قوالب وبيانات موحّدة
(مصدر واحد للحقيقة للوسوم والـSchema والروابط الداخلية).

```bash
cd build
python3 gen_services.py    # صفحات الخدمات
python3 gen_guides.py      # صفحات الأدلة
python3 gen_pages.py       # الرئيسية والصفحات المحورية
python3 gen_root.py        # robots / sitemap / manifest
python3 verify.py          # فحص شامل: H1، canonical، Schema، الروابط
```

## المعايير المطبّقة

- HTML5 دلالي · `lang="ar" dir="rtl"`
- H1 واحد لكل صفحة، تسلسل H2/H3 سليم
- canonical + hreflang على كل صفحة
- Open Graph + Twitter Cards بصور 1200×630 حقيقية
- Schema.org: Organization, WebSite, WebPage, Service, Article, FAQPage, BreadcrumbList, ItemList
- صور بـ alt وأبعاد محددة و lazy loading
- صفحة 404 بترميز HTTP 404 حقيقي
- robots.txt + sitemap.xml (21 عنواناً)
- رؤوس أمان + HSTS + كاش immutable للأصول (عبر vercel.json)

## ملاحظة

لا يستخدم الموقع أي أدوات تتبّع إعلانية.


---

## 🔄 تحديث 2026-11-06 — الجاذبية والتواصل وSEO

### ما أُضيف
- **شريط أيقونات التواصل الاجتماعي** في أعلى الصفحة الرئيسية (Hero) وفي صفحة التواصل وفي الفوتر — كل أيقونة برابطها الرسمي: واتساب، تيليجرام، سناب شات، إنستقرام، تيك توك، إكس، فيسبوك.
- **زر واتساب عائم** في كل الصفحات مربوط بالرقم `+966572851032` (`https://wa.me/966572851032`) مع رسالةافتتاحية جاهزة.
- **زر واتساب رئيسي في Hero** مع عرض الرقم، وزر اتصال `tel:` في صفحة التواصل.
- **قسم "لماذا أبو نواف؟"** بأربع بطاقات (أخلاقيات، تقرير قبل البدء، خصوصية، استجابة سريعة) — إشارات ثقة/مصداقية.
- **شرائح ثقة** في Hero + كرات ضوئية متحركة + خط Tajawal مع `display=swap`.

### SEO — ما تم تنفيذه تقنياً
- `ContactPoint` + `telephone: +966572851032` في Schema الخاص بـ Organization، ورابط واتساب في `sameAs`.
- `sitemap.xml` أصبح يحتوي على `<image:image>` لكل صفحة + `xhtml:link hreflang`.
- Meta: `google-site-verification` و`msvalidate.01` (placeholders — استبدلهما برموزك)، `og:updated_time`، `twitter:creator`، `mobile-web-app-capable`، `color-scheme`.
- Preload لـ CSSolute وlogo مع `fetchpriority="high"`، preconnect لـ wa.me و t.me، dns-prefetch.
- Skip-link لإمكانية الوصول، `fetchpriority`، `decoding` على الصور.

### ⏳ خطوات SEO outside الكود (تحتاج حسابك)
1. **Google Search Console**: أضف `ant.xo.je` → تحقق عبر DNS TXT أو استبدل `GOOGLE_VERIFICATION_CODE_HERE` في `build/layout.py` برمز HTML tag ثم أعد النشر. ثم أرسل `sitemap.xml`.
2. **Bing Webmaster Tools**: نفس الشيء — استبدل `BING_VERIFICATION_CODE_HERE` ثم أرسل السitemap.
3. **DNS**: وجّه `ant.xo.je` إلى Vercel (A: `216.198.79.1`, `64.29.17.1` + TXT `_vercel`).
