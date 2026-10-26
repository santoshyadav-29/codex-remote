const {chromium}=require('playwright');const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});try{
 const page=await browser.newPage({viewport:{width:1440,height:1100},acceptDownloads:true}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(process.env.BASE_URL||'http://127.0.0.1:8000');await page.waitForSelector('[data-bone="head"] path');await page.click('#play');
 assert.ok(await page.locator('#character path').count()>30);assert.ok((await page.locator('#character').boundingBox()).height>200);
 for(const character of ['boy','dog']){
  await page.click(`[data-character="${character}"]`);
  for(const clip of character==='boy'?['Idle','Walk','Run','Wave','Jump']:['Idle','Walk','Sit','Tilt']){await page.getByRole('button',{name:clip,exact:true}).click();await page.waitForTimeout(80);assert.equal(await page.locator('#poseName').textContent(),clip.toUpperCase());}
  await page.click('#reset');await page.click('#debugShortcut');await page.selectOption('#joint',character==='boy'?'elbowR':'earL');await page.locator('#angle').fill('35');assert.match(await page.locator(`[data-bone="${character==='boy'?'elbowR':'earL'}"]`).getAttribute('transform'),/rotate\(35\)/);
  const jsonEvent=page.waitForEvent('download');await page.click('#exportJSON');const jsonDownload=await jsonEvent;const jsonPath=await jsonDownload.path();
  await page.locator('#angle').fill('-25');await page.setInputFiles('#importJSON',jsonPath);await page.waitForTimeout(80);assert.match(await page.locator(`[data-bone="${character==='boy'?'elbowR':'earL'}"]`).getAttribute('transform'),/rotate\(35\)/);
  const svgEvent=page.waitForEvent('download');await page.click('#exportSVG');const svgDownload=await svgEvent;const svg=require('node:fs').readFileSync(await svgDownload.path(),'utf8');assert.ok(svg.includes('<path'));assert.ok(!svg.includes('bone-debug'));assert.ok(!svg.includes('<image'));
  await page.click('#debugShortcut');await page.click('#reset');await page.screenshot({path:`/tmp/atelier-${character}.png`,fullPage:true});
 }
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/atelier-mobile.png',fullPage:true});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);console.log('PASS: both characters, all nine clips, joint editing, JSON roundtrip, SVG export, mobile layout, no browser errors');
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
