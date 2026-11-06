import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        # desktop home full hero
        ctx=await b.new_context(viewport={"width":1366,"height":900}, device_scale_factor=1)
        pg=await ctx.new_page()
        await pg.goto("http://localhost:8080/", wait_until="load", timeout=30000)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path="build/v2-home-hero.png")
        # scroll to why-us
        await pg.evaluate("document.querySelector('.why-us').scrollIntoView()")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path="build/v2-whyus.png")
        await ctx.close()
        # mobile
        ctx=await b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg=await ctx.new_page()
        await pg.goto("http://localhost:8080/", wait_until="load", timeout=30000)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path="build/v2-home-mobile.png")
        # contact page desktop
        await pg.set_viewport_size({"width":1366,"height":900})
        await pg.goto("http://localhost:8080/pages/contact.html", wait_until="load", timeout=30000)
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path="build/v2-contact.png")
        await b.close()
        print("done")
asyncio.run(main())
