#!/usr/bin/env python3
"""Nari Nikhar — conversion-focused storefront.
   python3 build2.py artifact OUT  |  python3 build2.py site OUT
Every purchase action is the same green WhatsApp button; everything else supports it.
"""
import sys, urllib.parse, html, json

WA = "919870278767"
def wa(msg): return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)
def rs(n): return "₹{:,}".format(n)
E = html.escape

# slug: (name, look description, label, price)   — descriptions only state what the photo shows
P = {
 "lilac-cape-coord": ("Lilac Cape Co-ord Set", "Embroidered sheer cape over a matching kurta and palazzo", "New", 3999),
 "gold-embroidered-suit": ("Golden Embroidered Suit Set", "All-over embroidery with a blush sheer dupatta", "Wedding pick", 3799),
 "lavender-bandhani-dhoti": ("Shimmer Kurti & Bandhani Dhoti", "Shimmer top with a purple bandhani drape dhoti", "Indo-western", 3499),
 "lavender-embroidered-palazzo": ("Lavender Embroidered Palazzo Set", "Bead and thread work down a flowy front-slit kurta", "", 3299),
 "steel-blue-organza-suit": ("Steel Blue Embroidered Suit", "Embroidered yoke with a shimmer sheer dupatta", "", 2999),
 "beige-floral-suit": ("Beige Watercolour Floral Suit", "Soft neutrals with a painterly printed dupatta", "", 2599),
 "aqua-floral-suit": ("Aqua Floral Suit Set", "Bold blooms, contrast yoke and beaded hem", "", 2499),
 "blue-blockprint-sharara": ("Blue Printed Sharara Set", "Gathered kurta, tiered sharara and dupatta", "", 2399),
 "pink-anarkali-leheriya": ("Pink Anarkali with Leheriya Dupatta", "Floral Anarkali with lace trims", "Festive pick", 2299),
 "black-embroidered-suit": ("Black Embroidered Suit Set", "Floral sleeve embroidery and a printed dupatta", "", 2299),
 "white-orange-printed-suit": ("Ivory & Orange Printed Suit", "Ivory base with a vivid orange yoke and border", "", 2199),
 "black-ikat-suit": ("Black Ikat Print Suit Set", "Monochrome ikat print with striped pants", "", 2099),
 "rust-geometric-suit": ("Rust Geometric Salwar Suit", "Statement circles and chevrons with a dotted salwar", "", 2099),
 "navy-embroidered-salwar": ("Navy Embroidered Salwar Suit", "Embroidered sleeves and salwar hem", "", 1999),
 "brown-mustard-suit": ("Brown Suit with Mustard Dupatta", "Tassel yoke kurta and printed mustard dupatta", "", 1899),
 "plum-salwar-suit": ("Plum Salwar Suit Set", "Pintuck yoke and embroidered salwar hem", "", 1899),
}
def order_msg(slug):
    n, _, _, p = P[slug]
    return f"Hi Nari Nikhar! I want to order the {n} ({rs(p)}) from your website. Is it available in my size?"

ROWS = [  # highest prices first in the first row: sets the price anchor for the rest of the page
 ("party", "Party &amp; Festive Wear", "For weddings, Navratri and every function where you want to be noticed", "rose",
  ["lilac-cape-coord","gold-embroidered-suit","lavender-bandhani-dhoti","lavender-embroidered-palazzo","steel-blue-organza-suit"]),
 ("printed", "Printed Suit Sets", "Suit sets with dupatta in prints you will want in every colour", "violet",
  ["pink-anarkali-leheriya","aqua-floral-suit","blue-blockprint-sharara","beige-floral-suit","white-orange-printed-suit","black-ikat-suit","rust-geometric-suit"]),
 ("everyday", "Everyday Suits", "Easy, comfortable sets for office, college and family visits", "teal",
  ["brown-mustard-suit","plum-salwar-suit","navy-embroidered-salwar","black-embroidered-suit"]),
]
CIRCLES = [("Party Wear","gold-embroidered-suit","party"),("Co-ord Sets","lilac-cape-coord","party"),
 ("Indo-Western","lavender-bandhani-dhoti","party"),("Anarkali","pink-anarkali-leheriya","printed"),
 ("Sharara Sets","blue-blockprint-sharara","printed"),("Everyday","navy-embroidered-salwar","everyday")]
REVIEWS = ["Amazing quality at such a reasonable price! Totally satisfied with my purchases.",
           "Nice collection with reasonable prices.", "Collection is so awesome."]
GOOGLE = "https://www.google.com/maps/search/?api=1&query=Narinikhar+Women%27s+clothing+store+Hathras&query_place_id=ChIJcY-oTACFdDkRjd9rpPw1vOM"
MAPS = "https://www.google.com/maps/search/?api=1&query=Maheshwari+Dharamshala%2C+Subji+Mandi%2C+Naya+Ganj%2C+Hathras%2C+Uttar+Pradesh"

ICON = {
 "ship":'<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
 "video":'<rect x="3" y="6" width="12" height="12" rx="2"/><path d="M15 10l6-3v10l-6-3z"/>',
 "size":'<path d="M3 8h18v8H3z"/><path d="M7 8v3M11 8v4M15 8v3M19 8v4"/>',
 "swap":'<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
 "pin":'<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "phone":'<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
 "insta":'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>',
 "check":'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "shield":'<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "chev":'<path d="M9 6l6 6-6 6"/>',
}
def ic(n, c="ic"): return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{ICON[n]}</svg>'
WAI = '<svg class="wa" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
MANDALA = ('<svg class="mandala" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.7">'
  '<circle cx="32" cy="32" r="5"/><circle cx="32" cy="32" r="10"/>'
  + "".join(f'<path transform="rotate({a} 32 32)" d="M32 22c-4-6-4-12 0-18 4 6 4 12 0 18z"/>' for a in range(0,360,45))
  + "".join(f'<path transform="rotate({a} 32 32)" d="M32 22c-2.5-3-6-5-9-5 1 3.5 3.5 6 7 7"/>' for a in range(22,382,45)) + '</g></svg>')
STARS = '<span class="stars" aria-hidden="true">★★★★★</span>'

def img(slug, lazy=True, alt=None):
    return f'<img src="images/{slug}.jpg" alt="{E(alt or P[slug][0])}"{" loading=\"lazy\"" if lazy else ""}>'
def btn_wa(msg, label="Order on WhatsApp", cls="btn-wa"):
    return f'<a class="{cls}" href="{wa(msg)}" target="_blank" rel="noopener">{WAI}<span>{label}</span></a>'

def card(slug):
    n, d, lab, p = P[slug]
    b = f'<span class="label">{lab}</span>' if lab else ""
    return f'''<li class="prod">
 <button class="prod-img" type="button" data-zoom="{slug}" aria-label="See {E(n)} larger">{b}{img(slug)}<span class="tag">{rs(p)}</span></button>
 <div class="prod-info"><h3>{E(n)}</h3><p class="prod-desc">{E(d)}</p>
  <div class="prod-buy"><span class="price">{rs(p)}</span>{btn_wa(order_msg(slug), "Order", "btn-wa sm")}</div>
  <p class="assure">{ic("swap","mi")}5-day size exchange</p></div>
</li>'''

def row(sid, title, sub, tone, slugs):
    lo = min(P[s][3] for s in slugs)
    return f'''<section class="sec row tone-{tone}" id="{sid}" aria-labelledby="{sid}-h">
 <div class="wrap">
  <div class="row-head"><div><h2 id="{sid}-h">{title}</h2><p>{sub} · <b>from {rs(lo)}</b></p></div>
   <div class="row-ctrl"><button type="button" data-scroll="{sid}" data-dir="-1" aria-label="Scroll {title} left">‹</button><button type="button" data-scroll="{sid}" data-dir="1" aria-label="Scroll {title} right">›</button></div></div>
  <ul class="prods" data-row="{sid}">
{chr(10).join(card(s) for s in slugs)}
  </ul>
 </div>
</section>'''

CSS = r'''
/* Layout: conversion storefront — trust strip, header with one green action, price-led hero with photo collage, category circles, product rows anchored high-to-low, social proof between rows, style finder, 3-step "how to order", objections FAQ, closing call to action, sticky mobile order bar. Single bright theme by design.
   Colour roles: green = order (only purchase buttons use it), rani pink = brand & headings, marigold = ratings/highlights, purple = premium service band, ink = text. */
:root{
  --bg:#FFFFFF; --blush:#FFF0F6; --ink:#17060F; --muted:#4A3242; --line:rgba(23,6,15,.14);
  --rose:#D9006C; --rose-2:#A80054; --marigold:#FFBC0A; --sun:#FFE066; --violet:#5E1FB8; --teal:#00796B;
  --green:#0B8A44; --green-2:#086E36; --wa:#25D366;
  --f-display:"Rozha One","Noto Serif Devanagari",Georgia,serif;
  --f-ui:"Hanken Grotesk",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --f-hand:"Kalam","Segoe Print",cursive;
  --r:18px; color-scheme:light;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-ui);font-size:16.5px;line-height:1.6;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit}
h1,h2,h3{margin:0;text-wrap:balance}
p{margin:0}
.wrap{max-width:1240px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
.ic{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;flex:none}
.mi{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.wa{width:20px;height:20px;flex:none}
:focus-visible{outline:3px solid var(--marigold);outline-offset:3px}
.stars{color:var(--marigold);letter-spacing:.08em}
.toran{height:24px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='24'%3E%3Cpath d='M0 0h200v3H0z' fill='%2317060F'/%3E%3Cpath d='M0 3h40L20 24z' fill='%23D9006C'/%3E%3Cpath d='M40 3h40L60 24z' fill='%23FFBC0A'/%3E%3Cpath d='M80 3h40l-20 21z' fill='%235E1FB8'/%3E%3Cpath d='M120 3h40l-20 21z' fill='%2300796B'/%3E%3Cpath d='M160 3h40l-20 21z' fill='%23FF6A2B'/%3E%3C/svg%3E") repeat-x 0 0/200px 24px}
.dots{background-image:radial-gradient(circle,rgba(255,255,255,.22) 2px,transparent 2.6px),radial-gradient(circle,rgba(255,255,255,.12) 2px,transparent 2.6px);background-size:20px 20px;background-position:0 0,10px 10px}

/* the one purchase button */
.btn-wa{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:var(--green);color:#fff;text-decoration:none;font-weight:800;font-size:1.02rem;letter-spacing:.01em;padding:15px 26px;border-radius:999px;border:0;box-shadow:0 6px 0 var(--green-2),0 12px 24px -10px rgba(11,138,68,.6);transition:transform .15s,box-shadow .15s;white-space:nowrap}
.btn-wa:hover{transform:translateY(-2px);box-shadow:0 8px 0 var(--green-2),0 16px 28px -10px rgba(11,138,68,.7)}
.btn-wa:active{transform:translateY(3px);box-shadow:0 3px 0 var(--green-2)}
.btn-wa.sm{padding:9px 16px;font-size:.9rem;box-shadow:0 4px 0 var(--green-2)}
.btn-wa.sm .wa{width:17px;height:17px}
.btn-wa.lg{padding:18px 34px;font-size:1.12rem}
.btn-ghost{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:700;padding:14px 22px;border-radius:999px;border:2px solid var(--ink);color:var(--ink);background:#fff}
.btn-ghost:hover{background:var(--ink);color:#fff}

/* strip + header */
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);background:#fff;z-index:60}
.strip{background:var(--ink);color:#fff;font-size:.82rem;font-weight:700;overflow:hidden}
.strip-in{display:flex;gap:40px;justify-content:center;padding-block:9px;white-space:nowrap}
.strip-in span{display:inline-flex;align-items:center;gap:8px}
.strip .stars{font-size:.85rem}
.strip b{color:var(--sun)}
header.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:50;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);box-shadow:0 1px 0 var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:12px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}
.logo-img{width:56px;height:56px;border-radius:50%;flex:none;box-shadow:0 0 0 2px #fff,0 0 0 3px rgba(217,0,108,.35)}
.foot-logo .logo-img{width:96px;height:96px;box-shadow:none}
.logo-name{display:block;font-family:var(--f-display);font-size:1.75rem;line-height:1}
.logo-sub{display:block;font-size:.62rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--rose);margin-top:4px}
nav.main ul{list-style:none;margin:0;padding:0;display:flex;gap:4px}
nav.main a{display:block;padding:8px 12px;border-radius:999px;text-decoration:none;font-weight:700;font-size:.94rem}
nav.main a:hover{background:var(--blush);color:var(--rose)}
.bar .btn-wa{padding:11px 20px;font-size:.95rem;box-shadow:0 4px 0 var(--green-2)}
.menu-btn{display:none;align-items:center;gap:6px;border:2px solid var(--ink);background:#fff;border-radius:999px;padding:8px 14px;font:700 .9rem var(--f-ui);color:var(--ink);cursor:pointer}

/* hero */
.hero{background:linear-gradient(135deg,#FFF0F6 0%,#FFF7E0 100%);position:relative;overflow:hidden}
.hero::before{content:"";position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(255,188,10,.35),transparent 65%)}
.hero-in{display:grid;grid-template-columns:1fr 1.05fr;gap:44px;align-items:center;padding-block:48px 56px;position:relative}
.hero-copy{min-width:0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:6px 14px;font-size:.82rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--rose)}
.hero h1{font-family:var(--f-display);font-weight:400;font-size:clamp(2.7rem,5.6vw,4.6rem);line-height:1.02;margin-top:18px;letter-spacing:-.01em}
.hero h1 em{font-style:normal;color:var(--rose)}
.hero h1 .price-hl{white-space:nowrap;background:linear-gradient(transparent 62%,var(--sun) 62%)}
.hero .lede{font-size:1.15rem;color:var(--muted);margin-top:16px;max-width:42ch}
.hero-cta{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-top:28px}
.proof{display:flex;flex-wrap:wrap;gap:10px 20px;margin-top:24px;list-style:none;padding:0}
.proof li{display:flex;align-items:center;gap:7px;font-weight:700;font-size:.92rem}
.proof .ic{width:19px;height:19px;color:var(--green)}
.proof a{text-decoration:none}
.proof a:hover{text-decoration:underline}
.collage{position:relative;display:grid;grid-template-columns:1.15fr 1fr;grid-template-rows:1fr 1fr;gap:14px;height:560px;min-width:0}
.ph{position:relative;border-radius:var(--r);overflow:hidden;box-shadow:0 18px 40px -18px rgba(23,6,15,.5);background:var(--blush);cursor:zoom-in;border:0;padding:0}
.ph img{width:100%;height:100%;object-fit:cover;object-position:center top;transition:transform .6s}
.ph:hover img{transform:scale(1.04)}
.ph.big{grid-row:1/3}
.ptag{position:absolute;left:12px;bottom:12px;background:#fff;color:var(--ink);border-radius:999px;padding:6px 12px;font-weight:800;font-size:.88rem;box-shadow:0 4px 12px rgba(0,0,0,.18);display:flex;gap:6px;align-items:center}
.ptag i{font-style:normal;color:var(--rose)}
.sticker{position:absolute;z-index:3;right:-6px;top:-10px;background:var(--rose);color:#fff;font-family:var(--f-hand);font-weight:700;font-size:1.05rem;line-height:1.1;text-align:center;width:118px;height:118px;border-radius:50%;display:grid;place-items:center;transform:rotate(10deg);box-shadow:0 0 0 5px #fff,0 10px 24px -8px rgba(217,0,108,.6)}

/* categories */
.sec{padding-block:60px}
.sec-head{text-align:center;max-width:640px;margin:0 auto 32px}
.sec-head h2{font-family:var(--f-display);font-weight:400;font-size:clamp(2rem,3.8vw,2.9rem);line-height:1.05}
.sec-head p{color:var(--muted);margin-top:8px}
.kick{display:block;font-size:.78rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--rose);margin-bottom:8px}
.circles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,1fr);gap:18px}
.circles a{display:flex;flex-direction:column;align-items:center;gap:10px;text-decoration:none;font-weight:800;font-size:.92rem;text-align:center}
.ring{width:100%;max-width:150px;aspect-ratio:1;border-radius:50%;padding:5px;background:conic-gradient(var(--rose) 0 25%,var(--marigold) 0 50%,var(--violet) 0 75%,var(--teal) 0);transition:transform .25s}
.ring img{width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:center 12%;border:3px solid #fff}
.circles a:hover .ring{transform:translateY(-4px) rotate(-3deg)}
.circles small{display:block;font-weight:600;color:var(--muted);font-size:.8rem}

/* product rows */
.row{position:relative}
.tone-rose{background:var(--blush)} .tone-rose{--c:var(--rose)}
.tone-violet{background:#F3EDFF;--c:var(--violet)}
.tone-teal{background:#E6F6F3;--c:var(--teal)}
.row-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:24px}
.row-head h2{font-family:var(--f-display);font-weight:400;font-size:clamp(2rem,3.6vw,2.7rem);line-height:1.05;color:var(--c)}
.row-head p{color:var(--muted);margin-top:4px}
.row-head b{color:var(--ink)}
.row-ctrl{display:flex;gap:8px;flex:none}
.row-ctrl button{width:44px;height:44px;border-radius:50%;border:2px solid var(--ink);background:#fff;font-size:1.3rem;line-height:1;cursor:pointer;color:var(--ink)}
.row-ctrl button:hover{background:var(--ink);color:#fff}
.prods{list-style:none;margin:0;padding:4px 4px 16px;display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 3*20px)/4.3);gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:thin}
.prod{scroll-snap-align:start;background:#fff;border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;box-shadow:0 1px 0 var(--line),0 12px 28px -18px rgba(23,6,15,.45);transition:transform .2s,box-shadow .2s;min-width:0}
.prod:hover{transform:translateY(-4px);box-shadow:0 1px 0 var(--line),0 20px 36px -18px rgba(23,6,15,.55)}
.prod-img{position:relative;display:block;width:100%;padding:0;border:0;background:var(--blush);aspect-ratio:2/3;overflow:hidden;cursor:zoom-in}
.prod-img img{width:100%;height:100%;object-fit:cover;object-position:center top;transition:transform .6s}
.prod-img:hover img{transform:scale(1.05)}
.label{position:absolute;top:10px;left:10px;z-index:2;background:var(--ink);color:var(--sun);font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:5px 10px;border-radius:999px}
.tag{position:absolute;right:10px;bottom:10px;background:#fff;color:var(--ink);font-weight:800;font-size:.88rem;padding:5px 11px;border-radius:999px;box-shadow:0 4px 10px rgba(0,0,0,.15)}
.prod-info{padding:14px 14px 14px;display:flex;flex-direction:column;gap:6px;flex:1}
.prod-info h3{font-size:1.02rem;font-weight:800;line-height:1.3}
.prod-desc{color:var(--muted);font-size:.86rem;line-height:1.45}
.prod-buy{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:auto;padding-top:8px}
.price{font-size:1.3rem;font-weight:800;color:var(--c,var(--rose));font-variant-numeric:tabular-nums}
.assure{display:flex;align-items:center;gap:6px;font-size:.78rem;font-weight:600;color:var(--muted)}
.assure .mi{color:var(--green)}

/* reviews */
.reviews{background:var(--rose);color:#fff}
.reviews .sec-head h2{color:#fff}
.reviews .kick{color:var(--sun)}
.rev-grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:18px}
.score{background:var(--ink);border-radius:var(--r);padding:26px;display:flex;flex-direction:column;gap:6px;min-width:0}
.score .num{font-family:var(--f-display);font-size:4.2rem;line-height:1;color:var(--sun)}
.score .stars{font-size:1.3rem}
.score p{opacity:.85}
.score a{margin-top:auto;color:var(--sun);font-weight:800;text-decoration:none}
.score a:hover{text-decoration:underline}
.rev{margin:0;background:#fff;color:var(--ink);border-radius:var(--r);padding:24px;display:flex;flex-direction:column;gap:12px;min-width:0}
.rev blockquote{margin:0;font-size:1.12rem;line-height:1.45;font-weight:500}
.rev figcaption{margin-top:auto;display:flex;align-items:center;gap:8px;font-size:.8rem;font-weight:700;color:var(--muted)}
.gdot{width:22px;height:22px;border-radius:50%;background:conic-gradient(#4285F4 0 25%,#34A853 0 50%,#FBBC05 0 75%,#EA4335 0);flex:none}

/* style finder */
.finder{background:var(--ink);color:#fff;border-radius:28px;padding:40px;display:grid;grid-template-columns:1.15fr .85fr;gap:36px;position:relative;overflow:hidden}
.finder>*{position:relative;min-width:0}
.finder h2{font-family:var(--f-display);font-weight:400;font-size:clamp(2rem,3.8vw,2.8rem);line-height:1.05}
.finder h2 em{font-style:normal;color:var(--sun)}
.finder .intro{color:rgba(255,255,255,.78);margin-top:8px}
.q{margin-top:22px}
.q-l{display:block;font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--sun);margin-bottom:9px}
.opts{display:flex;flex-wrap:wrap;gap:8px}
.opt{font:700 .92rem var(--f-ui);padding:9px 15px;border-radius:999px;border:1.5px solid rgba(255,255,255,.35);background:transparent;color:#fff;cursor:pointer;display:inline-flex;align-items:center;gap:7px}
.opt:hover{border-color:#fff}
.opt[aria-pressed="true"]{background:#fff;color:var(--ink);border-color:#fff}
.sw{width:13px;height:13px;border-radius:50%;flex:none;border:1px solid rgba(255,255,255,.6)}
.chat{background:#ECE5DD;border-radius:22px;padding:18px;display:flex;flex-direction:column;gap:12px;align-self:center;color:var(--ink)}
.chat-top{display:flex;align-items:center;gap:10px;font-weight:800}
.chat-top .av{width:36px;height:36px;border-radius:50%;flex:none}
.chat-top small{display:block;font-weight:600;color:var(--muted);font-size:.75rem}
.bubble{align-self:flex-end;background:#DCF8C6;border-radius:14px 14px 4px 14px;padding:12px 14px;font-size:.98rem;line-height:1.45;box-shadow:0 1px 0 rgba(0,0,0,.12);max-width:100%}
.chat .btn-wa{width:100%}

/* steps + guarantee */
.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:20px;counter-reset:s}
.step{background:#fff;border:2px solid var(--ink);border-radius:var(--r);padding:26px;position:relative;min-width:0}
.step::before{counter-increment:s;content:counter(s);position:absolute;top:-18px;left:22px;width:40px;height:40px;border-radius:50%;background:var(--marigold);color:var(--ink);font-family:var(--f-display);font-size:1.4rem;display:grid;place-items:center;border:2px solid var(--ink)}
.step h3{font-size:1.15rem;font-weight:800;margin-top:10px}
.step p{color:var(--muted);margin-top:6px}
.guarantee{margin-top:26px;display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-radius:var(--r);overflow:hidden;background:#fff;box-shadow:0 0 0 2px var(--ink)}
.g{display:flex;gap:12px;padding:20px;min-width:0}
.g+.g{border-left:2px solid var(--ink)}
.g .ic{width:28px;height:28px;color:var(--rose)}
.g b{display:block;font-weight:800}
.g span{color:var(--muted);font-size:.88rem}

/* video promo */
.promo{background-color:var(--violet);color:#fff}
.promo-in{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;padding-block:56px}
.promo h2{font-family:var(--f-display);font-weight:400;font-size:clamp(2.1rem,4vw,3.2rem);line-height:1.05}
.promo p{opacity:.9;margin-top:12px;max-width:44ch}
.fee{font-family:var(--f-display);font-size:3.2rem;line-height:1;color:var(--sun);margin-top:18px}
.fee small{font-family:var(--f-ui);font-size:.88rem;color:#fff;font-weight:700;margin-left:8px}
.promo .btn-wa{margin-top:22px}
.promo-pics{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.promo-pics img{width:100%;aspect-ratio:2/3;object-fit:cover;object-position:center top;border-radius:var(--r);border:4px solid #fff}
.promo-pics img:last-child{margin-top:34px}

/* faq */
.faq{max-width:820px;margin:0 auto;display:grid;gap:12px}
.faq details{background:#fff;border:2px solid var(--ink);border-radius:16px;padding:0 20px}
.faq summary{cursor:pointer;list-style:none;font-weight:800;font-size:1.05rem;padding:18px 0;display:flex;justify-content:space-between;gap:12px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:1.5rem;line-height:1;color:var(--rose);flex:none}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 0 18px;color:var(--muted)}

/* visit */
.visit{display:grid;grid-template-columns:.8fr 1.2fr;gap:50px;align-items:center}
.visit-pic{position:relative}
.visit-pic img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center top;border-radius:220px 220px 22px 22px}
.visit-pic::after{content:"";position:absolute;inset:16px -16px -16px 16px;border-radius:220px 220px 22px 22px;background:var(--marigold);z-index:-1}
.visit h2{font-family:var(--f-display);font-weight:400;font-size:clamp(2.1rem,4vw,3.1rem);line-height:1.06}
.visit h2 em{font-style:normal;color:var(--rose)}
.visit .copy>p{color:var(--muted);margin-top:14px;max-width:54ch}
.info{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:24px}
.vi{display:flex;gap:12px;min-width:0}
.vi .ic{color:var(--rose)}
.vi b{display:block;font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
.vi span{color:var(--muted);font-size:.95rem}
.visit-cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}

/* closing CTA */
.close{background-color:var(--rose);color:#fff;text-align:center}
.close .wrap{padding-block:64px}
.close h2{font-family:var(--f-display);font-weight:400;font-size:clamp(2.2rem,4.6vw,3.6rem);line-height:1.05}
.close p{opacity:.92;margin:12px auto 0;max-width:46ch;font-size:1.1rem}
.close .btn-wa{margin-top:26px;background:#fff;color:var(--green);box-shadow:0 6px 0 rgba(0,0,0,.25)}
.close .btn-wa:hover{box-shadow:0 8px 0 rgba(0,0,0,.25)}
.close small{display:block;margin-top:14px;opacity:.85;font-weight:600}

/* footer */
footer{background:var(--ink);color:rgba(255,255,255,.8);font-size:.93rem}
.foot{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.2fr;gap:32px;padding-block:50px 36px}
footer .logo{color:#fff}
footer .logo-sub{color:var(--sun)}
footer h4{margin:0 0 12px;color:var(--sun);font-size:.8rem;letter-spacing:.14em;text-transform:uppercase}
footer ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
footer a{text-decoration:none}
footer a:hover{color:#fff;text-decoration:underline}
.copyline{border-top:1px solid rgba(255,255,255,.14)}
.copyline .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;padding-block:16px;font-size:.82rem}

/* floating + sticky order bar */
.fab{position:fixed;right:calc(20px + env(safe-area-inset-right,0px));bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:70;display:flex;align-items:center;gap:10px;background:var(--wa);color:#073B1C;text-decoration:none;font-weight:800;padding:12px 18px 12px 14px;border-radius:999px;box-shadow:0 10px 28px -6px rgba(0,0,0,.35)}
.fab .wa{width:28px;height:28px}
.fab .ping{position:absolute;inset:0;border-radius:999px;box-shadow:0 0 0 0 rgba(37,211,102,.7);animation:ping 2.4s ease-out infinite;pointer-events:none}
@keyframes ping{70%{box-shadow:0 0 0 14px rgba(37,211,102,0)}100%{box-shadow:0 0 0 0 rgba(37,211,102,0)}}
.mbar{display:none}
.dup{display:none}

/* lightbox */
.lb{position:fixed;inset:0;z-index:90;background:rgba(23,6,15,.86);display:none;align-items:center;justify-content:center;padding:calc(18px + env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) calc(18px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}
.lb.open{display:flex}
.lb-box{background:#fff;border-radius:22px;overflow:auto;display:grid;grid-template-columns:auto 330px;max-width:1000px;max-height:100%}
.lb-box img{max-height:86vh;width:auto;object-fit:contain}
.lb-side{padding:30px 26px;display:flex;flex-direction:column;gap:10px}
.lb-side h3{font-family:var(--f-display);font-weight:400;font-size:1.9rem;line-height:1.1}
.lb-side p{color:var(--muted)}
.lb-side .price{font-size:1.8rem;color:var(--rose)}
.lb-side ul{list-style:none;padding:0;margin:6px 0 0;display:grid;gap:6px;font-size:.9rem;font-weight:600}
.lb-side li{display:flex;gap:8px;align-items:center}
.lb-side li .mi{color:var(--green)}
.lb-side .btn-wa{margin-top:10px}
.lb-close{position:absolute;top:calc(14px + env(safe-area-inset-top,0px));right:calc(14px + env(safe-area-inset-right,0px));width:46px;height:46px;border-radius:50%;border:0;background:#fff;font-size:1.5rem;cursor:pointer;color:var(--ink)}

@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}html{scroll-behavior:auto}}

/* responsive */
@media (max-width:1080px){
  nav.main{display:none}
  nav.main.open{display:block;position:absolute;left:0;right:0;top:100%;background:#fff;box-shadow:0 10px 20px -10px rgba(0,0,0,.3)}
  nav.main.open ul{flex-direction:column;padding:10px max(18px,env(safe-area-inset-right,0px)) 16px max(18px,env(safe-area-inset-left,0px))}
  .menu-btn{display:inline-flex}
  .prods{grid-auto-columns:calc((100% - 2*16px)/3.25);gap:16px}
  .rev-grid{grid-template-columns:1fr 1fr}
  .guarantee{grid-template-columns:1fr 1fr}
  .g:nth-child(3){border-left:0}
  .g:nth-child(n+3){border-top:2px solid var(--ink)}
  .foot{grid-template-columns:1fr 1fr}
}
@media (max-width:860px){
  .hero-in,.finder,.promo-in,.visit{grid-template-columns:1fr}
  .hero-in{padding-block:28px 40px;gap:30px}
  .collage{height:440px}
  .circles{grid-template-columns:repeat(3,1fr)}
  .steps{grid-template-columns:1fr;gap:28px}
  .lb-box{grid-template-columns:1fr}
  .lb-box img{width:100%;max-height:60vh}
  .lb-side{padding:20px}
  .fab{display:none}
  .mbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:70;gap:10px;background:#fff;box-shadow:0 -6px 20px -8px rgba(0,0,0,.25);padding:10px max(12px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px))}
  .mbar .btn-wa{flex:1;padding:13px 16px;box-shadow:0 4px 0 var(--green-2)}
  .mbar .call{display:inline-flex;align-items:center;justify-content:center;gap:6px;border:2px solid var(--ink);border-radius:999px;padding:0 16px;font-weight:800;text-decoration:none}
  body{padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
  .bar .btn-wa{display:none}
}
@media (max-width:560px){
  body{font-size:16px}
  .strip-in{justify-content:flex-start;animation:tick 22s linear infinite;width:max-content}
  @keyframes tick{to{transform:translateX(-50%)}}
  .dup{display:contents}
  .logo-name{font-size:1.4rem}.logo-img{width:46px;height:46px}.logo-sub{letter-spacing:.12em;font-size:.56rem}
  .hero .lede{font-size:1.05rem}
  .hero-cta .btn-wa{width:100%}
  .hero-cta .btn-ghost{width:100%;justify-content:center}
  .collage{height:400px;gap:10px}
  .sticker{width:92px;height:92px;font-size:.85rem}
  .sec{padding-block:46px}
  .row-ctrl{display:none}
  .prods{grid-auto-columns:calc((100% - 12px)/1.75);gap:12px}
  .prod-desc{display:none}
  .prod-info h3{font-size:.95rem}
  .price{font-size:1.15rem}
  .prod-buy{flex-direction:column;align-items:stretch}
  .prod-buy .btn-wa{width:100%}
  .rev-grid{grid-template-columns:1fr}
  .finder{padding:26px 18px;border-radius:22px}
  .guarantee{grid-template-columns:1fr}
  .g{border-left:0!important;border-top:2px solid var(--ink)}
  .g:first-child{border-top:0}
  .info{grid-template-columns:1fr}
  .foot{grid-template-columns:1fr}
  .promo-pics img:last-child{margin-top:20px}
}

/* ===== Logo theme: charcoal + hot pink brush ring, high contrast ===== */
:root{--char:#2B2B2F;--char-2:#38383D;--char-3:#1E1E21;--pink:#FF2E8B;--rose:#E0006E;--rose-2:#B0005A;--pink-soft:#FFE4F1;--blush:#FFF0F7;
  --f-display:"Poppins","Hanken Grotesk",system-ui,sans-serif}
h1,h2,.logo-name,.fee,.score .num,.step::before{font-family:var(--f-display)!important;font-weight:800!important;letter-spacing:-.015em}
.logo-name{letter-spacing:.02em;text-transform:uppercase;font-size:1.35rem}
/* brush divider replaces the bunting */
.toran{height:14px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='14' viewBox='0 0 400 14'%3E%3Cpath d='M0 8 C60 2 120 12 200 7 S330 3 400 8' fill='none' stroke='%23FF2E8B' stroke-width='5' stroke-linecap='round'/%3E%3Cpath d='M0 10 C80 6 150 13 220 9 S350 6 400 11' fill='none' stroke='%23FF2E8B' stroke-opacity='.45' stroke-width='2'/%3E%3C/svg%3E") repeat-x 0 0/400px 14px}
/* strip + header in logo colours */
.strip{background:var(--pink);color:#fff}
.strip b{color:#fff;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:3px}
.strip .stars{color:#fff}
body::before{background:var(--char)}
header.top{background:var(--char);box-shadow:none}
header.top .logo{color:#fff}
.logo-sub{color:var(--pink)}
.logo-img{box-shadow:0 0 0 2px var(--pink)}
nav.main a{color:#fff}
nav.main a:hover{background:var(--pink);color:#fff}
.menu-btn{background:var(--char);color:#fff;border-color:#fff}
@media (max-width:1080px){nav.main.open{background:var(--char)}}
/* hero: charcoal stage, pink brush circle behind the photos */
.hero{background:radial-gradient(circle at 78% 40%,#3A3A40 0,var(--char) 55%,var(--char-3) 100%);color:#fff}
.hero::before{display:none}
.eyebrow{background:rgba(255,46,139,.14);border-color:var(--pink);color:#fff}
.hero h1{color:#fff}
.hero h1 em{color:var(--pink)}
.hero h1 .price-hl{background:none;color:var(--pink);text-decoration:underline;text-decoration-color:var(--pink);text-decoration-thickness:5px;text-underline-offset:8px}
.hero .lede{color:rgba(255,255,255,.82)}
.proof li{color:#fff}
.proof .ic{color:var(--pink)}
.hero .btn-ghost{background:transparent;color:#fff;border-color:#fff}
.hero .btn-ghost:hover{background:#fff;color:var(--char)}
.collage{isolation:isolate}
.collage::before{content:"";position:absolute;z-index:-1;inset:-34px -26px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cg fill='none' stroke='%23FF2E8B' stroke-linecap='round'%3E%3Cellipse cx='100' cy='100' rx='93' ry='90' stroke-width='3.2' stroke-dasharray='420 30 40 12'/%3E%3Cellipse cx='101' cy='99' rx='90' ry='93' stroke-width='1.4' stroke-opacity='.6' stroke-dasharray='300 20 60 25'/%3E%3Cellipse cx='99' cy='101' rx='95' ry='88' stroke-width='.8' stroke-opacity='.45'/%3E%3C/g%3E%3C/svg%3E") center/contain no-repeat}
.ph{box-shadow:0 0 0 3px var(--char),0 18px 40px -16px rgba(0,0,0,.7)}
.ptag i{color:var(--rose)}
.sticker{background:var(--pink);box-shadow:0 0 0 5px var(--char),0 10px 24px -8px rgba(255,46,139,.7)}
/* section headings with a pink brush underline */
.sec-head h2::after,.row-head h2::after{content:"";display:block;width:110px;height:10px;margin-top:10px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='110' height='10'%3E%3Cpath d='M3 6 C30 2 70 9 107 4' fill='none' stroke='%23FF2E8B' stroke-width='5' stroke-linecap='round'/%3E%3C/svg%3E") no-repeat}
.sec-head h2::after{margin-inline:auto}
.kick{color:var(--rose)}
/* category rings in pink brush tones */
.ring{background:conic-gradient(var(--pink) 0 30%,var(--char) 0 34%,var(--pink) 0 64%,#FF8CC0 0 70%,var(--pink) 0 96%,var(--char) 0)}
.circles a{color:var(--char)}
.circles a:hover{color:var(--rose)}
/* product rows: alternate charcoal / white / pink for contrast */
.tone-rose{background:var(--char);--c:var(--pink)}
.tone-rose .row-head h2{color:#fff}
.tone-rose .row-head p{color:rgba(255,255,255,.78)}
.tone-rose .row-head b{color:var(--pink)}
.tone-rose .row-ctrl button{background:transparent;border-color:#fff;color:#fff}
.tone-rose .row-ctrl button:hover{background:var(--pink);border-color:var(--pink)}
.tone-violet{background:#fff;--c:var(--rose)}
.tone-violet .row-head h2,.tone-teal .row-head h2{color:var(--char)}
.tone-teal{background:var(--pink-soft);--c:var(--rose)}
.prod{box-shadow:0 0 0 2px var(--char),0 14px 28px -16px rgba(0,0,0,.45)}
.tone-rose .prod{box-shadow:0 0 0 2px var(--pink),0 16px 30px -14px rgba(0,0,0,.8)}
.prod:hover{box-shadow:0 0 0 3px var(--pink),0 20px 36px -16px rgba(0,0,0,.5)}
.label{background:var(--pink);color:#fff}
.price{color:var(--rose)}
/* reviews on hot pink, charcoal score */
.reviews{background-color:var(--pink)}
.reviews .kick{color:#fff}
.reviews .sec-head h2::after{filter:brightness(0) invert(1)}
.score{background:var(--char)}
.score .num,.score a{color:var(--pink)}
.score .stars{color:var(--sun)}
.rev{box-shadow:0 0 0 2px var(--char)}
/* finder */
.finder{background:var(--char)}
.finder h2 em,.finder .kick,.q-l{color:var(--pink)!important}
.opt[aria-pressed="true"]{background:var(--pink);border-color:var(--pink);color:#fff}
/* steps & guarantee */
#how{background:var(--pink-soft)!important}
.step{border-color:var(--char)}
.step::before{background:var(--pink);color:#fff;border-color:var(--char)}
.g .ic{color:var(--rose)}
.guarantee{box-shadow:0 0 0 2px var(--char)}
.g+.g{border-color:var(--char)}
/* video promo: charcoal with pink */
.promo{background-color:var(--char)}
.promo .kick,.fee{color:var(--pink)!important}
.promo-pics img{border-color:var(--pink)}
/* faq + visit */
.faq details{border-color:var(--char)}
.faq summary::after{color:var(--pink)}
.visit h2 em{color:var(--rose)}
.visit-pic::after{background:var(--pink)}
.vi .ic{color:var(--rose)}
/* closing CTA + footer */
.close{background-color:var(--pink)}
footer{background:var(--char-3)}
footer h4,footer .logo-sub{color:var(--pink)}
footer .logo{color:#fff}
.copyline{border-color:rgba(255,46,139,.35)}
.lb-side .price{color:var(--rose)}
@media (max-width:560px){.logo-name{font-size:1.1rem}.collage::before{inset:-18px -12px}}
'''

lo_all = min(v[3] for v in P.values())
HEAD_NAV = [("#party","Party Wear"),("#printed","Suit Sets"),("#everyday","Everyday"),("#how","How to Order"),("#reviews","Reviews"),("#visit","Visit Store")]
STRIP = f'<span>{STARS} <b>4.6</b> on Google</span><span>Suit sets from <b>{rs(lo_all)}</b></span><span>5-day size exchange</span><span>Sizes up to 3XL+</span><span>Worldwide shipping</span>'

BODY = f'''
<div class="strip"><div class="strip-in">{STRIP}<span class="dup" aria-hidden="true"></span></div></div>
<header class="top">
 <div class="wrap bar" style="position:relative">
  <a class="logo" href="#top" aria-label="Nari Nikhar home"><img class="logo-img" src="images/logo-192.png" alt="Nari Nikhar logo" width="56" height="56"><span><span class="logo-name">Nari Nikhar</span><span class="logo-sub">Quality makes the difference</span></span></a>
  <nav class="main" id="mainNav" aria-label="Main"><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in HEAD_NAV)}</ul></nav>
  <div style="display:flex;gap:10px;align-items:center">
   {btn_wa("Hi Nari Nikhar! I would like to order an outfit.", "Order on WhatsApp")}
   <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mainNav"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Menu</button>
  </div>
 </div>
 <div class="toran" aria-hidden="true"></div>
</header>

<main id="top">
<section class="hero">
 <div class="wrap hero-in">
  <div class="hero-copy">
   <span class="eyebrow">{ic("pin","mi")} Hathras · New festive collection</span>
   <h1>Designer suit sets <span class="price-hl">from {rs(lo_all)}</span>. <em>Be the best dressed at every function.</em></h1>
   <p class="lede">Party wear, printed suit sets and co-ords. Pick your favourite here, send it to us on WhatsApp, and we'll confirm your size and colour.</p>
   <div class="hero-cta">
    {btn_wa("Hi Nari Nikhar! I saw your website. Please help me choose an outfit.", "Order on WhatsApp", "btn-wa lg")}
    <a class="btn-ghost" href="#party">See the collection ↓</a>
   </div>
   <ul class="proof">
    <li><a href="{GOOGLE}" target="_blank" rel="noopener">{STARS} <b>4.6</b> · 21 Google reviews</a></li>
    <li>{ic("check")}5-day size exchange</li>
    <li>{ic("check")}Sizes up to 3XL+</li>
    <li>{ic("check")}Worldwide shipping</li>
   </ul>
  </div>
  <div class="collage">
   <button class="ph big" type="button" data-zoom="lilac-cape-coord" aria-label="See Lilac Cape Co-ord Set larger">{img("lilac-cape-coord", lazy=False)}<span class="ptag">Lilac Cape Co-ord <i>{rs(3999)}</i></span></button>
   <button class="ph" type="button" data-zoom="pink-anarkali-leheriya" aria-label="See Pink Anarkali larger">{img("pink-anarkali-leheriya", lazy=False)}<span class="ptag"><i>{rs(2299)}</i></span></button>
   <button class="ph" type="button" data-zoom="brown-mustard-suit" aria-label="See Brown Suit with Mustard Dupatta larger">{img("brown-mustard-suit", lazy=False)}<span class="ptag"><i>{rs(1899)}</i></span></button>
   <div class="sticker">New<br>festive<br>edit ✦</div>
  </div>
 </div>
</section>

<section class="sec">
 <div class="wrap">
  <div class="sec-head"><span class="kick">Shop by style</span><h2>What are you shopping for?</h2></div>
  <ul class="circles">
{chr(10).join(f'<li><a href="#{t}"><span class="ring">{img(s, alt=n)}</span>{n}</a></li>' for n,s,t in CIRCLES)}
  </ul>
 </div>
</section>

{row(*ROWS[0])}

<section class="sec reviews dots" id="reviews">
 <div class="wrap">
  <div class="sec-head"><span class="kick">Real customers · Google reviews</span><h2>What our customers say</h2></div>
  <div class="rev-grid">
   <div class="score"><div class="num">4.6</div>{STARS}<p>Average from 21 reviews on Google</p><a href="{GOOGLE}" target="_blank" rel="noopener">Read all reviews →</a></div>
{chr(10).join(f'   <figure class="rev">{STARS}<blockquote>{E(r)}</blockquote><figcaption><span class="gdot" aria-hidden="true"></span>Google review</figcaption></figure>' for r in REVIEWS)}
  </div>
 </div>
</section>

{row(*ROWS[1])}

<section class="sec" id="finder">
 <div class="wrap">
  <div class="finder dots">
   <div>
    <span class="kick" style="color:var(--sun)">Free style help</span>
    <h2>Not sure what to pick? <em>Tell us three things.</em></h2>
    <p class="intro">Tap your answers and we'll write the WhatsApp message for you. Our team replies with outfits that match.</p>
    <div class="q"><span class="q-l">1 · The occasion</span><div class="opts" data-q="occasion">
     <button class="opt" type="button" aria-pressed="true">Wedding</button><button class="opt" type="button" aria-pressed="false">Navratri / Dandiya</button><button class="opt" type="button" aria-pressed="false">Diwali &amp; festivals</button><button class="opt" type="button" aria-pressed="false">Party</button><button class="opt" type="button" aria-pressed="false">Office / daily</button>
    </div></div>
    <div class="q"><span class="q-l">2 · Your size</span><div class="opts" data-q="size">
     <button class="opt" type="button" aria-pressed="false">S</button><button class="opt" type="button" aria-pressed="true">M</button><button class="opt" type="button" aria-pressed="false">L</button><button class="opt" type="button" aria-pressed="false">XL</button><button class="opt" type="button" aria-pressed="false">2XL</button><button class="opt" type="button" aria-pressed="false">3XL+</button>
    </div></div>
    <div class="q"><span class="q-l">3 · Budget</span><div class="opts" data-q="budget">
     <button class="opt" type="button" aria-pressed="false">Under ₹2,000</button><button class="opt" type="button" aria-pressed="true">₹2,000 – ₹3,000</button><button class="opt" type="button" aria-pressed="false">₹3,000 – ₹4,000</button><button class="opt" type="button" aria-pressed="false">Show me everything</button>
    </div></div>
   </div>
   <div class="chat">
    <div class="chat-top"><img class="av" src="images/logo-192.png" alt="" width="36" height="36"><span>Nari Nikhar<small>+91 98702 78767</small></span></div>
    <div class="bubble" id="bubble" aria-live="polite">Hi Nari Nikhar! I'm looking for a wedding outfit in size M, budget ₹2,000 – ₹3,000. Please show me what you have.</div>
    <a class="btn-wa" id="finderBtn" href="#" target="_blank" rel="noopener">{WAI}<span>Send on WhatsApp</span></a>
   </div>
  </div>
 </div>
</section>

{row(*ROWS[2])}

<section class="sec" id="how" style="background:var(--blush)">
 <div class="wrap">
  <div class="sec-head"><span class="kick">Simple &amp; safe</span><h2>How to order in 3 easy steps</h2></div>
  <ol class="steps">
   <li class="step"><h3>Pick your outfit</h3><p>Tap "Order" on any outfit you like, or send us a screenshot.</p></li>
   <li class="step"><h3>Chat on WhatsApp</h3><p>We confirm your size, colour and price, and answer any questions.</p></li>
   <li class="step"><h3>Collect or get it delivered</h3><p>Pick it up from our Hathras store, or we ship it to you, anywhere in the world.</p></li>
  </ol>
  <div class="guarantee">
   <div class="g">{ic("swap")}<div><b>5-day size exchange</b><span>Not the right fit? Exchange it.</span></div></div>
   <div class="g">{ic("size")}<div><b>Sizes up to 3XL+</b><span>Extended sizes in selected styles.</span></div></div>
   <div class="g">{ic("ship")}<div><b>Worldwide shipping</b><span>Across India and abroad.</span></div></div>
   <div class="g">{ic("shield")}<div><b>Real shop in Hathras</b><span>Visit us any day of the week.</span></div></div>
  </div>
 </div>
</section>

<section class="promo dots" id="video">
 <div class="wrap promo-in">
  <div>
   <span class="kick" style="color:var(--sun)">Live from the boutique</span>
   <h2>Shop on a video call, from anywhere</h2>
   <p>Living in another city or abroad? We'll show you every outfit live: the colour, the fabric, the fall. Choose with confidence before you buy.</p>
   <div class="fee">₹300<small>booking fee, adjusted in your bill</small></div>
   {btn_wa("Hi Nari Nikhar! I would like to book a video shopping call.", "Book a video call")}
  </div>
  <div class="promo-pics">{img("lavender-embroidered-palazzo")}{img("gold-embroidered-suit")}</div>
 </div>
</section>

<section class="sec" id="faq">
 <div class="wrap">
  <div class="sec-head"><span class="kick">Questions</span><h2>Before you order</h2></div>
  <div class="faq">
   <details open><summary>How do I order?</summary><p>Tap "Order on WhatsApp" on the outfit you like. A message with the outfit name and price opens in WhatsApp. Send it, and we'll confirm your size and colour.</p></details>
   <details><summary>What if the size doesn't fit?</summary><p>You can exchange your size within 5 days. Just message us on WhatsApp.</p></details>
   <details><summary>Do you have plus sizes?</summary><p>Yes. Many styles come in sizes up to 3XL+. Tell us your size and we'll show you what fits.</p></details>
   <details><summary>Do you deliver outside Hathras?</summary><p>Yes, we ship across India and worldwide. Ask us on WhatsApp for delivery options to your city.</p></details>
   <details><summary>Can I see the outfit before buying?</summary><p>Visit our store in Naya Ganj, or book a video call (₹300, adjusted in your bill) and we'll show you the outfit live.</p></details>
   <details><summary>Are more colours available?</summary><p>Many designs come in more colours, and the collection keeps changing. Ask us on WhatsApp for today's options.</p></details>
  </div>
 </div>
</section>

<section class="sec" id="visit" style="padding-top:20px">
 <div class="wrap visit">
  <div class="visit-pic">{img("navy-embroidered-salwar", alt="Navy embroidered salwar suit at Nari Nikhar")}</div>
  <div class="copy">
   <span class="kick">Visit the boutique</span>
   <h2>Come try it on in <em>Naya Ganj, Hathras</em></h2>
   <p>Clothes are lovely, but feeling lovely is everything. Walk in and our team will help you find the outfit that feels like you, in your size.</p>
   <div class="info">
    <div class="vi">{ic("pin")}<div><b>Address</b><span>Naya Ganj, Subji Mandi, Opp. Maheshwari Dharamshala, Hathras</span></div></div>
    <div class="vi">{ic("clock")}<div><b>Store hours</b><span>Mon – Sat: 11 AM – 8 PM<br>Sunday: 12 PM – 6 PM</span></div></div>
    <div class="vi">{ic("phone")}<div><b>Call / WhatsApp</b><span>+91 98702 78767</span></div></div>
    <div class="vi">{ic("insta")}<div><b>Instagram</b><span>@narinikhar</span></div></div>
   </div>
   <div class="visit-cta">
    <a class="btn-ghost" href="{MAPS}" target="_blank" rel="noopener">{ic("pin","mi")} Get directions</a>
    {btn_wa("Hi Nari Nikhar! I am planning to visit your store.", "Message before you visit")}
   </div>
  </div>
 </div>
</section>

<section class="close dots">
 <div class="wrap">
  <h2>Found something you love?</h2>
  <p>Send it to us on WhatsApp. We'll check your size and colour for you.</p>
  {btn_wa("Hi Nari Nikhar! I would like to order from your website.", "Order on WhatsApp", "btn-wa lg")}
  <small>5-day size exchange · Sizes up to 3XL+ · Worldwide shipping</small>
 </div>
</section>
</main>

<footer>
 <div class="toran" aria-hidden="true"></div>
 <div class="wrap foot">
  <div><a class="logo foot-logo" href="#top"><img class="logo-img" src="images/logo-320.png" alt="Nari Nikhar logo" width="96" height="96" loading="lazy"><span><span class="logo-name">Nari Nikhar</span><span class="logo-sub">Quality makes the difference</span></span></a>
   <p style="margin-top:14px;max-width:34ch">Party wear, suit sets with dupatta, co-ords and everyday suits. Shop in Hathras or on WhatsApp.</p></div>
  <div><h4>Shop</h4><ul><li><a href="#party">Party &amp; Festive Wear</a></li><li><a href="#printed">Printed Suit Sets</a></li><li><a href="#everyday">Everyday Suits</a></li><li><a href="#video">Video Shopping</a></li></ul></div>
  <div><h4>Help</h4><ul><li><a href="#how">How to order</a></li><li><a href="#faq">Size exchange</a></li><li><a href="#faq">Shipping</a></li><li><a href="#reviews">Reviews</a></li></ul></div>
  <div><h4>Visit us</h4><p>Naya Ganj, Subji Mandi<br>Opp. Maheshwari Dharamshala, Hathras</p><p style="margin-top:10px">+91 98702 78767<br>Mon – Sat · 11 AM – 8 PM<br>Sunday · 12 PM – 6 PM</p><p style="margin-top:10px"><a href="https://www.instagram.com/narinikhar/" target="_blank" rel="noopener">Instagram ↗</a></p></div>
 </div>
 <div class="copyline"><div class="wrap"><span>© <span data-year>2026</span> Nari Nikhar, Hathras</span><span>Quality makes the difference.</span></div></div>
</footer>

<a class="fab" href="{wa('Hi Nari Nikhar! I would like help choosing an outfit.')}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><span class="ping"></span>{WAI}<span>Chat with us</span></a>
<div class="mbar">{btn_wa("Hi Nari Nikhar! I would like to order an outfit.", "Order on WhatsApp")}<a class="call" href="tel:+919870278767">{ic("phone","mi")}Call</a></div>

<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-labelledby="lbTitle">
 <button class="lb-close" id="lbClose" type="button" aria-label="Close">×</button>
 <div class="lb-box">
  <img id="lbImg" src="images/lilac-cape-coord.jpg" alt="">
  <div class="lb-side"><span class="kick" style="display:flex;align-items:center;gap:8px"><img src="images/logo-192.png" alt="" width="32" height="32" style="border-radius:50%">Nari Nikhar</span><h3 id="lbTitle">Outfit</h3><p id="lbDesc"></p><span class="price" id="lbPrice"></span>
   <a class="btn-wa" id="lbWa" href="#" target="_blank" rel="noopener">{WAI}<span>Order on WhatsApp</span></a>
   <ul><li>{ic("check","mi")}5-day size exchange</li><li>{ic("check","mi")}Sizes up to 3XL+ in selected styles</li><li>{ic("check","mi")}Worldwide shipping</li></ul>
  </div>
 </div>
</div>
'''

JS = '''<script>
(function(){
 var P=%s, WA="%s";
 function waUrl(m){return 'https://wa.me/'+WA+'?text='+encodeURIComponent(m)}
 document.querySelectorAll('[data-year]').forEach(function(e){e.textContent=new Date().getFullYear()});
 /* mobile strip: duplicate content for a seamless ticker */
 var si=document.querySelector('.strip-in'),dup=si.querySelector('.dup');dup.innerHTML=si.innerHTML.replace('<span class="dup" aria-hidden="true"></span>','');
 var mb=document.getElementById('menuBtn'),nav=document.getElementById('mainNav');
 mb.addEventListener('click',function(){var o=mb.getAttribute('aria-expanded')==='true';mb.setAttribute('aria-expanded',String(!o));nav.classList.toggle('open',!o)});
 nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');mb.setAttribute('aria-expanded','false')})});
 document.querySelectorAll('[data-scroll]').forEach(function(b){b.addEventListener('click',function(){
  var r=document.querySelector('[data-row="'+b.dataset.scroll+'"]');r.scrollBy({left:r.clientWidth*0.75*Number(b.dataset.dir),behavior:'smooth'})})});
 /* style finder */
 var bub=document.getElementById('bubble'),fb=document.getElementById('finderBtn');
 function pick(q){var b=document.querySelector('[data-q="'+q+'"] [aria-pressed="true"]');return b?b.textContent.trim():''}
 function upd(){var o=pick('occasion'),s=pick('size'),b=pick('budget');
  var occ={'Wedding':'a wedding outfit','Navratri / Dandiya':'a Navratri / Dandiya outfit','Diwali & festivals':'a festive outfit','Party':'a party outfit','Office / daily':'an outfit for office / daily wear'}[o]||'an outfit';
  var bud=b==='Show me everything'?'any budget':'budget '+b;
  var m="Hi Nari Nikhar! I'm looking for "+occ+" in size "+s+", "+bud+". Please show me what you have.";
  bub.textContent=m;fb.href=waUrl(m)}
 document.querySelectorAll('.opts').forEach(function(g){g.addEventListener('click',function(e){var b=e.target.closest('.opt');if(!b)return;
  g.querySelectorAll('.opt').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});upd()})});
 upd();
 /* lightbox */
 var lb=document.getElementById('lb'),last;
 function open(slug){var p=P[slug];if(!p)return;last=document.activeElement;
  var im=document.getElementById('lbImg');im.src='images/'+slug+'.jpg';im.alt=p[0];
  document.getElementById('lbTitle').textContent=p[0];document.getElementById('lbDesc').textContent=p[1];document.getElementById('lbPrice').textContent=p[2];
  document.getElementById('lbWa').href=waUrl('Hi Nari Nikhar! I want to order the '+p[0]+' ('+p[2]+') from your website. Is it available in my size?');
  lb.hidden=false;lb.classList.add('open');document.body.style.overflow='hidden';document.getElementById('lbClose').focus()}
 function close(){lb.classList.remove('open');lb.hidden=true;document.body.style.overflow='';if(last)last.focus()}
 document.querySelectorAll('[data-zoom]').forEach(function(b){b.addEventListener('click',function(){open(b.dataset.zoom)})});
 document.getElementById('lbClose').addEventListener('click',close);
 lb.addEventListener('click',function(e){if(e.target===lb)close()});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('open'))close()});
})();
</script>''' % (json.dumps({k:[v[0],v[1],rs(v[3])] for k,v in P.items()}), WA)

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Hanken+Grotesk:wght@400;500;600;700;800&family=Kalam:wght@700&display=swap">'
DESC = f"Designer suit sets from {rs(lo_all)} at Nari Nikhar, Hathras. Party wear, printed suits and co-ords. 4.6★ on Google. Order on WhatsApp, 5-day size exchange."

mode, out = sys.argv[1], sys.argv[2]
if mode == "artifact":
    page = f'<title>Nari Nikhar Boutique</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n<style>{CSS}</style>\n{BODY}\n{JS}\n'
else:
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Nari Nikhar | Designer Suit Sets from {rs(lo_all)} · Hathras</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#2B2B2F">
<meta property="og:title" content="Nari Nikhar | Designer Suit Sets from {rs(lo_all)}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://prashanttyagi3112.github.io/narinikhar/images/lilac-cape-coord.jpg">
<meta property="og:image" content="https://prashanttyagi3112.github.io/narinikhar/images/share-card.jpg">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"ClothingStore","name":"Nari Nikhar","telephone":"+91 98702 78767","address":{"@type":"PostalAddress","streetAddress":"Naya Ganj, Subji Mandi, Opp. Maheshwari Dharamshala","addressLocality":"Hathras","addressRegion":"Uttar Pradesh","addressCountry":"IN"},"openingHours":["Mo-Sa 11:00-20:00","Su 12:00-18:00"],"priceRange":f"{rs(lo_all)} - {rs(3999)}","logo":"https://prashanttyagi3112.github.io/narinikhar/images/logo.png","slogan":"Quality makes the difference","sameAs":["https://www.instagram.com/narinikhar/"]})}</script>
{FONTS}
<style>{CSS}</style>
</head>
<body>
{BODY}
{JS}
</body>
</html>
'''
open(out, "w", encoding="utf-8").write(page)
print("wrote", out, len(page))
