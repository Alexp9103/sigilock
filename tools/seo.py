"""SEO de sigilock.com: regenera sitemap.xml con todas las páginas y avisa a los buscadores por IndexNow.
Uso (desde la carpeta sigilock-web, después de hacer push):
  py tools/seo.py            -> reescribe sitemap.xml (fecha = último commit de cada página)
  py tools/seo.py --ping     -> además avisa a IndexNow (Bing, Yandex, Seznam, Naver...) de todas las URL
Cada guía nueva (/algo/index.html) entra sola en el sitemap."""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "sigilock.com"
KEY = "5f3c9a1e7b2d4c8f9a6e1b3d7c5f2a90"   # archivo de verificación: /<KEY>.txt
SKIP = {"tools"}

pages = sorted(p for p in ROOT.rglob("index.html") if not (set(p.relative_to(ROOT).parts) & SKIP) and ".git" not in p.parts)


def url(p):
    rel = p.parent.relative_to(ROOT).as_posix()
    return f"https://{HOST}/" + ("" if rel == "." else rel + "/")


def lastmod(p):
    d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(p)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return d or "2026-11-26"


urls = [url(p) for p in pages]
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p, u in zip(pages, urls):
    xml += ["  <url>", f"    <loc>{u}</loc>", f"    <lastmod>{lastmod(p)}</lastmod>", "  </url>"]
xml.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
(ROOT / f"{KEY}.txt").write_text(KEY, encoding="utf-8")
print(f"sitemap.xml: {len(urls)} páginas")
for u in urls:
    print(" ", u)

if "--ping" in sys.argv:
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow:", r.status, "(200/202 = recibido)")
    except urllib.error.HTTPError as e:
        print("IndexNow:", e.code, e.read().decode()[:200])
