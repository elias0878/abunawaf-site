import asyncio, json, sys, os, re
from playwright.async_api import async_playwright
from urllib.parse import urljoin

BASE="http://127.0.0.1:8080"
pages=[]
for root,_,files in os.walk("/home/user/site"):
    if "/build" in root or "/_source" in root: continue
    for f in files:
        if f.endswith(".html"):
            rel=os.path.relpath(os.path.join(root,f),"/home/user/site")
            pages.append("/"+rel.replace("index.html","").replace("\\","/"))
pages=sorted(set(p for p in pages if "tools.html" not in p))
errors=[]; warnings=[]; results={}

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":1366,"height":900})
        pg=await ctx.new_page()
        all_links=set()
        for path in pages:
            url=BASE+path
            r=await pg.goto(url, wait_until="domcontentloaded", timeout=30000)
            d=await pg.evaluate("""()=>{
              const q=s=>document.querySelector(s), all=s=>[...document.querySelectorAll(s)];
              const ld=all('script[type="application/ld+json"]');
              let types=[], parseErr=null;
              for(const s of ld){ try{ const j=JSON.parse(s.textContent); (j['@graph']||[j]).forEach(n=>types.push(Array.isArray(n['@type'])?n['@type'].join('+'):n['@type'])); }catch(e){ parseErr=e.message } }
              return {
                title:document.title, tlen:document.title.length,
                desc:(q('meta[name=description]')||{}).content||'',
                dlen:((q('meta[name=description]')||{}).content||'').length,
                canonical:(q('link[rel=canonical]')||{}).href||'',
                robots:(q('meta[name=robots]')||{}).content||'',
                h1:all('h1').map(e=>e.innerText.trim()),
                ogimg:(q('meta[property="og:image"]')||{}).content||'',
                imgsNoAlt:all('img').filter(i=>!i.hasAttribute('alt')).length,
                links:all('a[href]').map(a=>a.getAttribute('href')),
                schemaTypes:types, schemaErr:parseErr,
                textLen:document.body.innerText.replace(/\\s+/g,' ').trim().length,
                tw:all('h2').length, th:all('h3').length,
              };
            }""")
            st=r.status
            results[path]=d
            if st!=200: errors.append(f"{path} → HTTP {st}")
            if d["h1"] and len(d["h1"])!=1: errors.append(f"{path} → {len(d['h1'])} H1")
            if not d["h1"]: errors.append(f"{path} → لا يوجد H1")
            if not d["canonical"]: errors.append(f"{path} → لا يوجد canonical")
            if d["schemaErr"]: errors.append(f"{path} → JSON-LD خطأ: {d['schemaErr']}")
            if not d["schemaTypes"] and "404" not in path: warnings.append(f"{path} → لا يوجد Schema")
            if d["tlen"]>62: warnings.append(f"{path} → title {d['tlen']} حرف (>{62})")
            if d["dlen"]>165 and d["dlen"]>0: warnings.append(f"{path} → desc {d['dlen']} حرف")
            if d["imgsNoAlt"]: errors.append(f"{path} → {d['imgsNoAlt']} صورة بلا alt")
            if d["textLen"]<300: warnings.append(f"{path} → نص {d['textLen']} حرف فقط")
            for l in d["links"]+[d["ogimg"]]:
                if l and not l.startswith(("http","#","mailto","tel","javascript")):
                    all_links.add((path, l))
            print(f"{st} {path:48} h1={len(d['h1'])} txt={d['textLen']:5} schema={len(d['schemaTypes'])}", flush=True)

        # فحص الروابط الداخلية
        broken=set()
        cache={}
        for src, link in sorted(all_links):
            if link.startswith("http"): continue
            target=urljoin(BASE+src, link).split("#")[0]
            if target in cache:
                ok=cache[target]
            else:
                try:
                    rr=await ctx.request.get(target)
                    ok=rr.status==200; cache[target]=ok
                except Exception: ok=False; cache[target]=False
            if not ok: broken.add((src,link,target))
        print("\n=== روابط داخلية مكسورة:", len(broken))
        for s,l,t in sorted(broken)[:20]: print("  ",s,"→",l, "=>", t)
        await b.close()

    print("\n=== أخطاء:", len(errors))
    for e in errors: print("  ✗", e)
    print("\n=== تحذيرات:", len(warnings))
    for w in warnings: print("  ⚠", w)
    json.dump({"pages":results,"errors":errors,"warnings":warnings,
               "broken":[[s,l,t] for s,l,t in sorted(broken)]},
              open("/home/user/site/build/verify.json","w"), ensure_ascii=False, indent=1)
asyncio.run(main())
