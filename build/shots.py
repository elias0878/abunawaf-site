import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,path,vp in [("home-desktop","/",{"width":1366,"height":900}),
                             ("home-mobile","/",{"width":390,"height":844}),
                             ("svc-desktop","/services/anti-blackmail.html",{"width":1366,"height":900})]:
            ctx=await b.new_context(viewport=vp)
            pg=await ctx.new_page()
            await pg.goto("http://127.0.0.1:8080"+path, wait_until="load", timeout=30000)
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f"build/{name}.png")
            await ctx.close()
        await b.close()
asyncio.run(main())
