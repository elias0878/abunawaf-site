/**
 * أبو نواف (ابونواف) - JavaScript الخاص بصفحة المشكلات والحلول
 * يدعم المحتوى المضمن مسبقاً في HTML لأرشفة جوجل الفورية + البحث والتصفية التفاعلية
 */

document.addEventListener('DOMContentLoaded', function() {
    initProblemsPage();
});

function initProblemsPage() {
    const problems = getProblemsData();
    const accordion = document.getElementById('problemsAccordion');
    const searchInput = document.getElementById('problemsSearch');
    const filterBtns = document.querySelectorAll('.filter-btn');

    if (!accordion) return;

    // إذا كان المحتوى موجوداً مسبقاً في HTML (SSR)، نقوم فقط بربط الأحداث التفاعلية
    if (accordion.querySelectorAll('.accordion-item').length > 0) {
        bindAccordionEvents(accordion);
    } else {
        renderProblems(problems);
    }

    // دعم معامل البحث ?q= القادم من محرك بحث جوجل (Sitelinks Searchbox)
    const urlQuery = new URLSearchParams(window.location.search).get('q');
    if (urlQuery && searchInput) {
        searchInput.value = urlQuery;
        const qLower = urlQuery.trim().toLowerCase();
        const filtered = problems.filter(function(p) {
            return p.title.toLowerCase().includes(qLower) ||
                   p.shortDesc.toLowerCase().includes(qLower) ||
                   p.solution.toLowerCase().includes(qLower);
        });
        renderProblems(filtered);
    }

    // وظيفة البحث التفاعلي
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim().toLowerCase();
            const filtered = problems.filter(function(p) {
                return p.title.toLowerCase().includes(query) || 
                       p.shortDesc.toLowerCase().includes(query) ||
                       p.solution.toLowerCase().includes(query);
            });
            renderProblems(filtered);
        });
    }

    // وظيفة التصفية حسب التصنيف
    filterBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            filterBtns.forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            const filtered = filter === 'all' ? problems : problems.filter(function(p) {
                return p.category === filter;
            });
            renderProblems(filtered);
        });
    });

    // فتح المشكلة المحددة في الرابط (#problem-...)
    const hash = window.location.hash;
    if (hash) {
        setTimeout(function() {
            const target = document.querySelector(hash);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                target.classList.add('active');
                const header = target.querySelector('.accordion-header');
                if (header) header.setAttribute('aria-expanded', 'true');
                const body = target.querySelector('.accordion-body');
                if (body) {
                    body.style.maxHeight = body.scrollHeight + 'px';
                }
            }
        }, 350);
    }
}

function bindAccordionEvents(accordion) {
    const headers = accordion.querySelectorAll('.accordion-header');
    headers.forEach(function(header) {
        header.addEventListener('click', function() {
            const item = this.parentElement;
            const body = item.querySelector('.accordion-body');
            const isActive = item.classList.contains('active');

            accordion.querySelectorAll('.accordion-item.active').forEach(function(activeItem) {
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

function renderProblems(problems) {
    const accordion = document.getElementById('problemsAccordion');
    if (!accordion) return;

    if (problems.length === 0) {
        accordion.innerHTML = '<div class="empty-state"><svg viewBox="0 0 24 24" fill="none"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><h3>لا توجد نتائج مطابقة</h3><p>جرب البحث بكلمات مختلفة أو اختر تصنيفاً آخر</p></div>';
        return;
    }

    accordion.innerHTML = problems.map(function(problem) {
        return '<div class="accordion-item" id="problem-' + problem.id + '" data-category="' + problem.category + '">' +
            '<button class="accordion-header" aria-expanded="false" aria-controls="solution-' + problem.id + '">' +
                '<div class="accordion-icon">' + problem.icon + '</div>' +
                '<span class="accordion-title">' + problem.title + '</span>' +
                '<svg class="accordion-arrow" viewBox="0 0 24 24" fill="none"><path d="M19 9l-7 7-7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
            '</button>' +
            '<div class="accordion-body" id="solution-' + problem.id + '" role="region">' +
                '<div class="accordion-content">' +
                    problem.solution +
                    '<div class="help-more">' +
                        '<p>هل تحتاج مساعدة فورية من فريق أبو نواف؟</p>' +
                        '<a href="contact.html" class="btn btn-primary btn-sm">تواصل معنا الآن</a>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>';
    }).join('');

    bindAccordionEvents(accordion);
}
