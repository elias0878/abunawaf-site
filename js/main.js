/**
 * أبو نواف (ابونواف) ABU-NAWAF ETHICAL HACKER - JavaScript الرئيسي
 * الموقع الرسمي: https://ant.xo.je/
 * متوافق بالكامل مع عناكب محركات البحث (Googlebot / Bingbot SEO-Safe)
 */

// ========================================
// 1. تهيئة الموقع عند التحميل
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initStatusIndicator();
    initScrollTop();
    initCounters();
    initMobileMenu();
    initProblemsPreview();
    initGenericAccordions();
    setCurrentYear();
    initScrollAnimations();
});

// ========================================
// 2. شريط التنقل (Navbar)
// ========================================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });
}

// ========================================
// 3. قائمة الموبايل (Mobile Menu)
// ========================================
function initMobileMenu() {
    const menuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    const overlay = document.getElementById('mobileOverlay');
    
    if (!menuBtn || !navLinks) return;
    
    menuBtn.addEventListener('click', function() {
        const isActive = navLinks.classList.contains('active');
        
        navLinks.classList.toggle('active');
        menuBtn.classList.toggle('active');
        menuBtn.setAttribute('aria-expanded', !isActive);
        
        if (overlay) {
            overlay.classList.toggle('active');
        }
        
        document.body.style.overflow = isActive ? '' : 'hidden';
    });
    
    if (overlay) {
        overlay.addEventListener('click', function() {
            navLinks.classList.remove('active');
            menuBtn.classList.remove('active');
            menuBtn.setAttribute('aria-expanded', 'false');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    const links = navLinks.querySelectorAll('a');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
            menuBtn.classList.remove('active');
            menuBtn.setAttribute('aria-expanded', 'false');
            if (overlay) overlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
}

// ========================================
// 4. مؤشر حالة العمل (Status Indicator)
// ========================================
function initStatusIndicator() {
    const statusElem = document.getElementById('statusIndicator');
    if (!statusElem) return;
    
    function checkStatus() {
        // ← إصلاح: احسب دائماً بتوقيت الرياض (UTC+3) لا بتوقيت جهاز الزائر.
        // الرياض بلا توقيت صيفي، فإضافة 3 ساعات على UTC دقيقة دائماً.
        const now = new Date();
        const riyadh = new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (3 * 3600000));
        const hour = riyadh.getHours() + (riyadh.getMinutes() / 60);
        const day = riyadh.getDay(); // 0=الأحد, 5=الجمعة
        
        const isFriday = day === 5;
        // أوقات العمل: 2:30م (14:30) حتى 12:00ص (24:00/0:00)
        const isWorkingHours = (hour >= 14.5 && hour < 24);
        
        const textNode = statusElem.querySelector('.status-text');
        if (isFriday || !isWorkingHours) {
            statusElem.classList.add('offline');
            if (textNode) textNode.textContent = 'مغلق حالياً';
        } else {
            statusElem.classList.remove('offline');
            if (textNode) textNode.textContent = 'متاح الآن';
        }
    }
    
    checkStatus();
    setInterval(checkStatus, 60000);
}

// ========================================
// 5. زر العودة للأعلى (Scroll to Top)
// ========================================
function initScrollTop() {
    const scrollTopBtn = document.getElementById('scrollTop');
    if (!scrollTopBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 400) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    }, { passive: true });
    
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ========================================
// 6. عدادات الإحصائيات (Counters)
// ========================================
function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    if (counters.length === 0) return;
    
    if (!('IntersectionObserver' in window)) {
        counters.forEach(function(counter) {
            const target = parseInt(counter.getAttribute('data-target'), 10);
            counter.textContent = target + (target === 95 ? '%' : '+');
        });
        return;
    }

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });
    
    counters.forEach(function(counter) {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'), 10);
    const duration = 1800;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(function() {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current) + (target === 95 ? '%' : '+');
    }, 16);
}

// ========================================
// 7. معاينة المشكلات (Problems Preview)
// ========================================
function initProblemsPreview() {
    const preview = document.getElementById('problemsPreview');
    if (!preview) return;
    
    // إذا كانت العناصر موجودة مسبقاً في HTML لدعم محركات البحث، لا نعيد كتابتها إلا إذا كانت فارغة
    if (preview.children.length > 0) return;
    
    const problems = getProblemsData().slice(0, 5);
    preview.innerHTML = problems.map(function(problem) {
        return '<a href="pages/problems.html#problem-' + problem.id + '" class="problem-preview-item">' +
            '<div class="problem-preview-icon">' + problem.icon + '</div>' +
            '<div class="problem-preview-content">' +
                '<h4>' + problem.title + '</h4>' +
                '<p>' + problem.shortDesc + '</p>' +
            '</div>' +
            '<svg class="problem-preview-arrow" viewBox="0 0 24 24" fill="none"><path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
        '</a>';
    }).join('');
}

// ========================================
// 7-ب. تفعيل الأكورديون العام (مثل الأسئلة الشائعة في الرئيسية)
// ========================================
function initGenericAccordions() {
    const faqContainer = document.getElementById('homeFaqAccordion');
    if (!faqContainer) return;

    const headers = faqContainer.querySelectorAll('.accordion-header');
    headers.forEach(function(header) {
        header.addEventListener('click', function() {
            const item = this.parentElement;
            const body = item.querySelector('.accordion-body');
            const isActive = item.classList.contains('active');

            faqContainer.querySelectorAll('.accordion-item.active').forEach(function(activeItem) {
                if (activeItem !== item) {
                    activeItem.classList.remove('active');
                    const activeBody = activeItem.querySelector('.accordion-body');
                    if (activeBody) activeBody.style.maxHeight = '0';
                    const activeHeader = activeItem.querySelector('.accordion-header');
                    if (activeHeader) activeHeader.setAttribute('aria-expanded', 'false');
                }
            });

            if (isActive) {
                item.classList.remove('active');
                if (body) body.style.maxHeight = '0';
                this.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('active');
                if (body) body.style.maxHeight = body.scrollHeight + 'px';
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

function getProblemsData() {
    return [
        {
            id: 'account-hacked',
            title: 'تم اختراق حسابي',
            shortDesc: 'خطوات فورية لحماية واسترجاع حسابك المخترق أو المسروق',
            category: 'accounts',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>الخطوات الفورية لاسترجاع الحساب المخترق:</h4><ol><li>قم بتغيير كلمة المرور فوراً على جميع حساباتك المرتبطة</li><li>فعّل المصادقة الثنائية (2FA) إذا لم تكن مفعّلة</li><li>افحص الأجهزة والجلسات المتصلة بحسابك وأزل أي جهاز غير معروف</li><li>تحقق من سجل النشاط والبريد الإلكتروني ورقم الهاتف المرتبطين بالحساب</li><li>إذا لم تتمكن من الدخول، استخدم نموذج استرداد الحساب الرسمي للمنصة مع البريد البديل</li><li>تواصل مع فريق أبو نواف (ابونواف هكر أخلاقي) لاستعادة الحساب المسروق خلال 2-6 ساعات</li></ol>'
        },
        {
            id: 'account-suspended',
            title: 'حسابي موقوف بدون سبب',
            shortDesc: 'كيف تستعيد حسابك الموقوف أو المحظور نهائياً',
            category: 'accounts',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>خطوات استعادة الحساب الموقوف (فك الحظر):</h4><ol><li>تحقق من بريدك الإلكتروني لمعرفة سبب الإيقاف أو الحظر</li><li>قدم طلب استئناف رسمي عبر نموذج المنصة المعتمد</li><li>أرفق وثائق إثبات الهوية والملكية إذا طُلب منك ذلك</li><li>انتظر 24-48 ساعة لمراجعة الطلب من الدعم الفني</li><li>تجنب إنشاء حساب جديد بنفس الرقم أو البريد أثناء فترة المراجعة</li><li>إذا رُفض الطلب أو تأخر الرد، تواصل مع فريق ابونواف لفك إيقاف الحساب خلال 6-24 ساعة</li></ol>'
        },
        {
            id: 'being-blackmailed',
            title: 'أتعرض لابتزاز إلكتروني',
            shortDesc: 'إجراءات طارئة وفورية لحماية نفسك من المبتز',
            category: 'blackmail',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>إجراءات فورية لمكافحة الابتزاز الإلكتروني:</h4><ol><li>لا تدفع أي مبالغ مالية للمبتز إطلاقاً - الدفع لا يوقف الابتزاز بل يزيده</li><li>احفظ جميع الأدلة الرقمية (لقطات شاشة، رسائل، معرفات، روابط الحسابات)</li><li>أوقف التواصل مع المبتز ولا ترضخ لتهديداته</li><li>قدم بلاغاً رسمياً لدى الجهات المختصة بمكافحة الجرائم المعلوماتية</li><li>تواصل فوراً مع فريق أبو نواف (خدمة طارئة 1-3 ساعات) لحذف المحتوى وإغلاق حسابات المبتز وكشف هويته بسرية تامة</li></ol>'
        },
        {
            id: 'weak-password',
            title: 'كيف أنشئ كلمة مرور قوية؟',
            shortDesc: 'نصائح الأمن السيبراني لحماية حساباتك من الاختراق',
            category: 'security',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>نصائح إنشاء كلمة مرور قوية وآمنة:</h4><ol><li>استخدم 12 إلى 16 حرفاً على الأقل</li><li>ادمج بين الحروف الكبيرة والصغيرة والأرقام والرموز الخاصة</li><li>لا تستخدم معلومات شخصية يسهل تخمينها (الاسم، رقم الجوال، تاريخ الميلاد)</li><li>استخدم كلمة مرور فريدة ومختلفة لكل حساب ومنصة</li><li>اعتمد على مدير كلمات مرور موثوق ومشفر</li><li>فعّل المصادقة الثنائية (2FA) عبر تطبيق المصادقة وليس الرسائل النصية فقط</li></ol>'
        },
        {
            id: 'deceased-account',
            title: 'إغلاق حساب شخص متوفي',
            shortDesc: 'خطوات إغلاق وحذف حسابات المتوفين رسمياً',
            category: 'accounts',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>الخطوات المطلوبة لإغلاق حساب متوفي:</h4><ol><li>تجهيز شهادة الوفاة الرسمية أو الوثائق الثبوتية</li><li>حصر جميع الحسابات الإلكترونية للمتوفي (سناب شات، إنستغرام، إكس، تيك توك، فيسبوك)</li><li>تقديم طلب رسمي عبر نموذج إغلاق حسابات المتوفين الخاص بكل منصة</li><li>إرفاق الوثائق المطلوبة لإثبات صلة القرابة أو الصفة القانونية</li><li>تواصل مع فريق ابونواف لإتمام إغلاق وحذف حساب المتوفي بشكل كامل خلال 24-48 ساعة</li></ol>'
        },
        {
            id: 'phishing-attack',
            title: 'وقعت ضحية تصيد احتيالي',
            shortDesc: 'ماذا تفعل فوراً بعد إدخال بياناتك في رابط مزيف أو مشبوه',
            category: 'security',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>إجراءات طارئة عند الوقوع في التصيد الاحتيالي (Phishing):</h4><ol><li>غيّر كلمة المرور فوراً من جهاز آمن لجميع الحسابات المرتبطة</li><li>سجّل الخروج من جميع الجلسات والأجهزة المتصلة في إعدادات الأمان</li><li>إذا أدخلت بيانات بطاقة بنكية، أوقف البطاقة وتواصل مع البنك فوراً</li><li>افحص جهازك من البرمجيات الخبيثة وملفات التجسس</li><li>فعّل المصادقة الثنائية (2FA) وراجع البريد الإلكتروني ورقم الاسترداد</li></ol>'
        },
        {
            id: 'stalker-account',
            title: 'شخص يتابعني ويتحرش بي',
            shortDesc: 'حماية نفسك من المتابعة والمضايقات وكشف الحسابات الوهمية',
            category: 'privacy',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>خطوات الحماية من التحرش والملاحقة الإلكترونية:</h4><ol><li>اضبط خصوصية حساباتك إلى (حساب خاص) وأخفِ قوائم المتابعين والموقع الجغرافي</li><li>وثّق جميع الرسائل والتعليقات المسيئة بلقطات شاشة وروابط مباشرة</li><li>احظر الحساب المسيء وبلّغ عنه من داخل المنصة</li><li>لا تفتح أي روابط أو ملفات مرسلة من حسابات مجهولة</li><li>تواصل مع فريق أبو نواف لجمع المعلومات التقنية (OSINT) وكشف هوية الحساب المجهول خلال 2-8 ساعات</li></ol>'
        },
        {
            id: 'leaked-data',
            title: 'بياناتي مسربة على الإنترنت',
            shortDesc: 'كيف تتعامل مع تسريب بياناتك الشخصية أو صورك',
            category: 'privacy',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>خطوات التعامل مع تسريب البيانات:</h4><ol><li>حدد نوع البيانات المسربة والمنصات التي ظهرت فيها</li><li>غيّر جميع كلمات المرور للحسابات المرتبطة بالبريد أو الرقم المسرب</li><li>فعّل التحقق بخطوتين لجميع حساباتك البريدية والاجتماعية</li><li>راقب الحسابات المالية والبنكية لأي نشاط غير معتاد</li><li>تواصل مع فريق ابونواف هكر أخلاقي للمساعدة في حذف وإزالة البيانات والصور المسربة وحماية خصوصيتك</li></ol>'
        },
        {
            id: 'fake-identity',
            title: 'شخص ينتحل هويتي',
            shortDesc: 'التعامل الحاسم مع انتحال الشخصية وسرقة الهوية الرقمية',
            category: 'privacy',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>إجراءات إغلاق حسابات انتحال الشخصية:</h4><ol><li>وثّق الحساب المنتحل بالرابط المباشر والمعرّف ولقطات الشاشة</li><li>قدّم بلاغ انتحال شخصية رسمي (Impersonation Report) لإدارة المنصة</li><li>نبّه جهات اتصالك ومتابعيك بعدم التعامل مع الحساب المنتحل</li><li>راجع إعدادات الأمان في حساباتك الأصلية</li><li>تواصل مع فريق أبو نواف لإغلاق الحساب المنتحل وكشف بيانات صاحبه</li></ol>'
        },
        {
            id: 'phone-hacked',
            title: 'أعتقد أن هاتفي مخترق',
            shortDesc: 'علامات اختراق الهاتف الذكي وطرق الفحص والتأمين الشامل',
            category: 'security',
            icon: '<svg viewBox="0 0 24 24" fill="none"><path d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
            solution: '<h4>علامات اختراق الهاتف:</h4><ol><li>استنزاف البطارية وارتفاع حرارة الجهاز بشكل غير طبيعي</li><li>ظهور تطبيقات أو ملفات تعريف (Profiles) غير مألوفة</li><li>استهلاك بيانات إنترنت مرتفع في الخلفية</li><li>وصول رموز تحقق لم تطلبها أو نشاط غريب في حساباتك</li></ol><h4>خطوات الحل والتأمين:</h4><ol><li>افصل الإنترنت واحذف أي تطبيقات أو ملفات تعريف مشبوهة فوراً</li><li>حدّث نظام التشغيل (iOS / Android) إلى آخر إصدار أمني</li><li>غيّر كلمات المرور من جهاز آخر آمن وفعّل المصادقة الثنائية</li><li>تواصل مع فريق ابونواف لطلب فحص أمني شامل وتأمين هاتفك وحساباتك</li></ol>'
        }
    ];
}

// ========================================
// 8. السنة الحالية في التذييل
// ========================================
function setCurrentYear() {
    const yearElem = document.getElementById('currentYear');
    if (yearElem) {
        yearElem.textContent = new Date().getFullYear();
    }
}

// ========================================
// 9. تأثيرات التمرير المتوافقة مع محركات البحث (SEO-Safe Scroll Animations)
// ========================================
function initScrollAnimations() {
    // لا تقم بإخفاء أي عنصر إذا كان الزائر عنكبوت بحث (Googlebot/Bingbot) أو يفضل تقليل الحركة
    const ua = navigator.userAgent || '';
    const isBot = /bot|googlebot|crawler|spider|robot|crawling|lighthouse|headless|inspect/i.test(ua) || navigator.webdriver;
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (isBot || prefersReducedMotion || !('IntersectionObserver' in window)) {
        return;
    }

    const observerOptions = {
        threshold: 0.08,
        rootMargin: '0px 0px -20px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '';
                entry.target.style.transform = '';
                entry.target.classList.add('animate-fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.service-card, .feature-item, .social-card, .tool-card, .why-card, .svc-card, .guide-item').forEach(function(el) {
        observer.observe(el);
    });
}

// ========================================
// 10. وظائف مساعدة (Utility Functions)
// ========================================
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal-overlay.active');
        if (activeModal) {
            activeModal.classList.remove('active');
            document.body.style.overflow = '';
        }
        
        const navLinks = document.getElementById('navLinks');
        const menuBtn = document.getElementById('mobileMenuBtn');
        if (navLinks && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            if (menuBtn) menuBtn.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getProblemsData, getQueryParam };
}

/* ============================================================
   زر مشاركة الصفحة — Web Share API مع بديل النسخ
   أُضيف 2026-11-06
   ============================================================ */
(function initShareButtons() {
    const buttons = document.querySelectorAll('[data-share]');
    if (!buttons.length) return;

    const payload = () => ({
        title: document.title,
        text: (document.querySelector('meta[name="description"]') || {}).content || document.title,
        url: (document.querySelector('link[rel="canonical"]') || {}).href || location.href
    });

    buttons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const data = payload();
            try {
                if (navigator.share) {
                    await navigator.share(data);
                    return;
                }
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(data.url);
                    btn.setAttribute('data-copied', '1');
                    const old = btn.getAttribute('title');
                    btn.setAttribute('title', 'تم نسخ الرابط');
                    setTimeout(() => { btn.setAttribute('title', old || 'مشاركة'); }, 2000);
                    return;
                }
                window.prompt('انسخ الرابط:', data.url);
            } catch (err) {
                /* المستخدم أغلق نافذة المشاركة — لا إجراء */
            }
        });
    });
})();

/* ============================================================
   نقل مؤشر الحالة إلى شريط التواصل العلوي
   ============================================================ */
(function moveStatusIntoSocialbar() {
    var slot = document.getElementById('socialbarSlot');
    var st = document.getElementById('statusIndicator');
    if (slot && st) slot.appendChild(st);
})();
