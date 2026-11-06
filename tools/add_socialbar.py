# -*- coding: utf-8 -*-
"""إدراج شريط التواصل الثابت أسفل شريط التنقل في كل الصفحات."""
import glob
import os
import re
import sys

sys.path.insert(0, "/home/user/site/tools")
from icons import WA

ROOT = "/home/user/site"
from upgrade import CHANNELS, _rel, WA_NUMBER, WA_TEXT

WT = "السلام عليكم، تواصلت معكم من موقع أبو نواف."


def icons(size=18):
    out = []
    for ch in CHANNELS:
        out.append(
            f'<a class="social-btn social-btn-bar" style="--brand:{ch["brand"]}" '
            f'href="{ch["url"]}" target="_blank" rel="{_rel(ch)}" '
            f'aria-label="{ch["name"]} — {ch["handle"]}" title="{ch["name"]} · {ch["handle"]}">'
            f'<svg viewBox="0 0 24 24" fill="none" width="{size}" height="{size}" aria-hidden="true">'
            f'{ch["icon"]}</svg></a>')
    out.append('<button type="button" class="social-btn social-btn-bar social-share" data-share '
               'style="--brand:#d6b256" aria-label="مشاركة هذه الصفحة" title="مشاركة الصفحة">'
               f'<svg viewBox="0 0 24 24" fill="none" width="{size}" height="{size}" aria-hidden="true">'
               '<circle cx="18" cy="5" r="3" stroke="currentColor" stroke-width="1.9"/>'
               '<circle cx="6" cy="12" r="3" stroke="currentColor" stroke-width="1.9"/>'
               '<circle cx="18" cy="19" r="3" stroke="currentColor" stroke-width="1.9"/>'
               '<path d="M8.6 10.6l6.8-4M8.6 13.4l6.8 4" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
               '</svg></button>')
    return "".join(out)


BAR = f'''
    <div class="socialbar" id="socialbar" role="region" aria-label="قنوات التواصل الرسمية">
        <div class="socialbar-inner">
            <span class="socialbar-slot" id="socialbarSlot"></span>
            <div class="socialbar-icons">{icons()}</div>
            <a class="socialbar-cta" href="https://wa.me/{WA_NUMBER}?text={WT}" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" fill="none" width="17" height="17" aria-hidden="true">{WA}</svg>
                <span>تواصل مباشر</span>
            </a>
        </div>
    </div>
'''


def main():
    files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if "/tools/" not in f and "/.git/" not in f and "/pages/tools.html" not in f]
    for f in sorted(files):
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        h = open(f, encoding="utf-8").read()
        if 'id="socialbar"' in h:
            print(f"  – {rel} موجود مسبقاً")
            continue
        m = re.search(r'<\/nav>\s*\n', h)
        if not m:
            print(f"  ✗ {rel}: لم أجد </nav>")
            continue
        h = h[:m.end()] + BAR + h[m.end():]
        open(f, "w", encoding="utf-8").write(h)
        print(f"  ✓ {rel}")


if __name__ == "__main__":
    main()
