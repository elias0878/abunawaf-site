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
