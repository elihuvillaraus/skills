#!/usr/bin/env node
// Recorre una página guiada por scroll y la captura: stills por tramo (para el juez) o un video MP4 del recorrido.
//   usage: node tools/walk.mjs <url> <outDir> [--stops 12] [--width 1440] [--height 900] [--settle 900]
//                              [--video] [--fps 30] [--seconds 40] [--capture] [--mobile]
//   --stops N    N stills equiespaciados de 0 a 1 de la altura scrolleable (still-00.png ... ) y walk-report.json
//   --video      además arma walk.mp4 con N*fps frames (scroll lineal, sin pausas); necesita ffmpeg
//   --capture    añade ?capture a la URL (convención del patrón: sin suavizado de scroll ni intro)
//   --mobile     390x844 @2x, touch
//   --settle ms  espera tras cada salto de scroll (Lenis y GSAP suavizan; 900 ms basta casi siempre)
// Informa: errores de consola/página, renderer de WebGL (GPU o software) y peso transferido.
// Solo para sitios propios o de los que se pueda mostrar el resultado.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = (() => { try { return require('playwright'); } catch { return require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); } })();
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : d; };
const flag = (k) => { const i = args.indexOf(k); return i >= 0 ? (args.splice(i, 1), true) : false; };
const mobile = flag('--mobile'), video = flag('--video'), capture = flag('--capture');
const stops = Number(opt('--stops', 12)), settle = Number(opt('--settle', 900)), fps = Number(opt('--fps', 30)), seconds = Number(opt('--seconds', 40));
const width = Number(opt('--width', mobile ? 390 : 1440)), height = Number(opt('--height', mobile ? 844 : 900));
let [url, out] = args;
if (!url || !out) { console.error('usage: node tools/walk.mjs <url> <outDir> [--stops 12] [--video] [--capture] [--mobile]'); process.exit(2); }
if (capture) url += (url.includes('?') ? '&' : '?') + 'capture';
fs.mkdirSync(out, { recursive: true });
const gpuArgs = process.platform === 'darwin' ? ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] : ['--enable-gpu', '--ignore-gpu-blocklist'];
const browser = await chromium.launch({ args: gpuArgs });
const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: mobile ? 2 : 1, hasTouch: mobile, isMobile: mobile });
const page = await ctx.newPage();
const errors = []; let bytes = 0;
page.on('pageerror', (e) => errors.push('page: ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
page.on('response', async (r) => { try { bytes += Number(r.headers()['content-length'] || 0); } catch {} });
await page.goto(url, { waitUntil: 'load', timeout: 90000 });
await page.waitForTimeout(2500);
const gl = await page.evaluate(() => {
  const g = document.createElement('canvas').getContext('webgl2');
  if (!g) return { webgl2: false };
  const e = g.getExtension('WEBGL_debug_renderer_info');
  return { webgl2: true, renderer: String(e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER)) };
});
const max = () => page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
const total = await max();
const at = async (s) => { await page.evaluate((y) => window.scrollTo(0, y), Math.round(s * total)); };
const report = { url, viewport: `${width}x${height}${mobile ? ' mobile' : ''}`, scrollPx: total, gl, stills: [] };
for (let i = 0; i < stops; i++) {
  const s = stops === 1 ? 0 : i / (stops - 1);
  await at(s); await page.waitForTimeout(settle);
  const f = path.join(out, `still-${String(i).padStart(2, '0')}.png`);
  await page.screenshot({ path: f }); report.stills.push({ s: +s.toFixed(3), file: f });
}
if (video) {
  const n = Math.round(seconds * fps), dir = path.join(out, 'frames'); fs.mkdirSync(dir, { recursive: true });
  await at(0); await page.waitForTimeout(settle);
  for (let i = 0; i < n; i++) {
    await at(i / (n - 1)); await page.waitForTimeout(capture ? 60 : 120);
    await page.screenshot({ path: path.join(dir, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i "${dir}/f%05d.jpg" -c:v libx264 -pix_fmt yuv420p -crf 18 "${path.join(out, 'walk.mp4')}"`);
  report.video = path.join(out, 'walk.mp4');
}
report.errors = [...new Set(errors)].slice(0, 10); report.transferredMB = +(bytes / 1048576).toFixed(1);
fs.writeFileSync(path.join(out, 'walk-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify({ stills: report.stills.length, gl, scrollPx: total, errors: report.errors, transferredMB: report.transferredMB, video: report.video || null }, null, 1));
await browser.close();
