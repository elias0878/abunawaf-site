import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        tasks=[("live-home-desktop","/",{"width":1366,"height":900}),
               ("live-home-mobile","/",{"width":390,"height":844}),
               ("live-guides","/guides/",{"width":1366,"height":900}),
               ("live-404","/not-found-test",{"width":1366,"height":900})]
        for name,path,vp in tasks:
            ctx=await b.new_context(viewport=vp)
            pg=await ctx.new_page()
            await pg.goto("https://abunawaf.vercel.app"+path, wait_until="load", timeout=45000)
            await pg.wait_for_timeout(2000)
            await pg.screenshot(path=f"build/{name}.png")
            await ctx.close()
            print("shot", name)
        # perf
        ctx=await b.new_context(viewport={"width":390,"height":844})
        pg=await ctx.new_page()
        await pg.goto("https://abunawaf.vercel.app/", wait_until="load", timeout=45000)
        await pg.wait_for_timeout(2500)
        perf=await pg.evaluate("""()=>{const n=performance.getEntriesByType('navigation')[0]||{};
          const r=performance.getEntriesByType('resource');
          return {ttfb:Math.round(n.responseStart||0),load:Math.round(n.loadEventEnd||0),
                  requests:r.length+1, kb:Math.round((r.reduce((s,x)=>s+(x.transferSize||0),0)+(n.transferSize||0))/1024)};}""")
        print("perf:", perf)
        await b.close()
asyncio.run(main())
