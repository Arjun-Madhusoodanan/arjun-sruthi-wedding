from playwright.sync_api import sync_playwright
from pathlib import Path
url='http://127.0.0.1:8923/index.html'
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
  for name,w,h in [('desktop',1440,960),('mobile',390,844)]:
    page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1,has_touch=name=='mobile',is_mobile=name=='mobile')
    errs=[]
    page.on('pageerror', lambda exc:errs.append(str(exc)))
    page.goto(url,wait_until='domcontentloaded')
    page.locator('#openInvite').click(force=True)
    page.wait_for_timeout(900)
    print(name,'title',page.title(),'hero img',page.locator('.hero-portrait img').count(),'gallery',page.locator('#gallery img').count(),'event cards',page.locator('#events .event-card').count())
    print(name,'JS errors',errs[:8], 'music?',page.locator('#bgMusic').evaluate('(e)=>({paused:e.paused,ready:e.readyState})'))
    page.screenshot(path=f'/mnt/data/{name}_premium_hero.png',animations='disabled',full_page=False)
    page.locator('#events').scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.screenshot(path=f'/mnt/data/{name}_premium_events.png',animations='disabled',full_page=False)
    page.locator('#gallery').scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.screenshot(path=f'/mnt/data/{name}_premium_gallery.png',animations='disabled',full_page=False)
    page.screenshot(path=f'/mnt/data/{name}_premium_full.png',full_page=True,animations='disabled')
    page.close()
  browser.close()
