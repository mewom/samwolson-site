#!/usr/bin/env python3
"""
Sam Wolson Photography — Static Site Generator
Reads actual image files from /images/ and produces index.html + galleries/*.html
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE, "images")
GALLERIES_DIR = os.path.join(BASE, "galleries")
os.makedirs(GALLERIES_DIR, exist_ok=True)

# ── Gallery definitions (title → folder slug) ──────────────────────────────
# Order determines homepage grid order.
# slug_override: the actual folder name on disk (where it differs from slugify(title))
GALLERIES = [
    {"title": "Portraiture",            "slug": "portraiture"},
    {"title": "How We Move",            "slug": "how-we-move"},
    {"title": "Tour Du Rwanda",         "slug": "tour-du-rwanda"},
    {"title": "This Life I Lead",       "slug": "this-life-i-lead"},
    {"title": "Moments",                "slug": "moments"},
    {"title": "Ivory Burn",             "slug": "ivory-burn"},
    {"title": "Tin Roofs",              "slug": "tin-roofs"},
    {"title": "Burn",                   "slug": "burn"},
    {"title": "Portraits + Singles",    "slug": "portraits-singles"},
    {"title": "Oakland Protest",        "slug": "oakland-protest"},
    {"title": "Xin",                    "slug": "xin"},
    {"title": "Diamond In The Rough",   "slug": "diamond-in-the-rough"},
    {"title": "Okavango Delta",         "slug": "okavango-delta"},
    {"title": "Rey",                    "slug": "rey"},
    {"title": "E-Waste",                "slug": "e-waste"},
    {"title": "Mines",                  "slug": "mines"},
    {"title": "Xinjiang Portraits",     "slug": "xinjiang-portraits"},
    {"title": "Nuba",                   "slug": "nuba"},
    {"title": "Cobalt Mines in DRC",    "slug": "cobalt-mines-in-drc"},
    {"title": "Bam",                    "slug": "bam"},
]

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".JPG", ".JPEG", ".PNG"}

def get_images(slug):
    folder = os.path.join(IMAGES_DIR, slug)
    if not os.path.isdir(folder):
        return []
    files = sorted([
        f for f in os.listdir(folder)
        if os.path.splitext(f)[1] in IMAGE_EXTS
    ])
    return files

# ── HTML helpers ────────────────────────────────────────────────────────────

LIGHTBOX_HTML = """
  <!-- Lightbox -->
  <div id="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
    <div class="lb-inner">
      <button id="lb-close" aria-label="Close">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
      <button class="lb-btn" id="lb-prev" aria-label="Previous photo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>
      <img id="lb-img" src="" alt="" draggable="false"/>
      <button class="lb-btn" id="lb-next" aria-label="Next photo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </button>
      <div id="lb-counter"></div>
    </div>
  </div>
"""

def page_shell(title, body, extra_css="", from_gallery=False, include_lightbox=False):
    root = "../" if from_gallery else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="{root}css/style.css">
  <meta name="description" content="Sam Wolson — Documentary and portrait photographer.">
</head>
<body>

  <header class="site-header">
    <a href="{root}index.html" class="site-logo">Sam Wolson</a>
    <nav>
      <ul class="nav-links">
        <li><a href="{root}index.html">Work</a></li>
        <li><a href="mailto:mr.wolson@gmail.com">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main class="page-content">
{body}
  </main>

  <footer class="site-footer">
    &copy; {2024} Sam Wolson. All rights reserved.
  </footer>
{"  " + LIGHTBOX_HTML if include_lightbox else ""}
{"  <script src=\"" + root + "js/lightbox.js\"></script>" if include_lightbox else ""}
</body>
</html>"""

# ── Build index.html ─────────────────────────────────────────────────────────

def build_index(galleries_data):
    cards = []
    for g in galleries_data:
        slug   = g["slug"]
        title  = g["title"]
        imgs   = g["images"]
        count  = len(imgs)
        if not imgs:
            print(f"  [WARN] No images found for {title} ({slug}) — skipping card")
            continue
        thumb  = imgs[0]
        thumb_path = f"images/{slug}/{thumb}"
        card = f"""    <a href="galleries/{slug}.html" class="gallery-card">
      <img src="{thumb_path}" alt="{title}" loading="lazy">
      <div class="gallery-card-overlay">
        <h2>{title}</h2>
        <span>{count} photographs</span>
      </div>
    </a>"""
        cards.append(card)

    grid_html = "\n".join(cards)
    body = f"""    <section class="home-intro">
      <h1>Sam Wolson</h1>
      <p>Documentary &amp; Portrait Photography</p>
    </section>

    <section class="gallery-grid">
{grid_html}
    </section>"""

    html = page_shell("Sam Wolson — Photography", body)
    out_path = os.path.join(BASE, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK]  index.html — {len(cards)} galleries")

# ── Build gallery pages ──────────────────────────────────────────────────────

def build_gallery(g):
    slug   = g["slug"]
    title  = g["title"]
    imgs   = g["images"]
    count  = len(imgs)

    if not imgs:
        print(f"  [SKIP] {title} — no images")
        return

    items = []
    for img in imgs:
        src = f"../images/{slug}/{img}"
        alt = img.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
        items.append(f'      <div class="photo-item"><img src="{src}" alt="{alt}" loading="lazy"></div>')

    grid_html = "\n".join(items)

    body = f"""    <div class="gallery-header">
      <a href="../index.html" class="back-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
        All work
      </a>
      <h1>{title}</h1>
      <p>{count} photographs</p>
    </div>

    <div class="photo-grid">
{grid_html}
    </div>"""

    html = page_shell(f"{title} — Sam Wolson", body, from_gallery=True, include_lightbox=True)
    out_path = os.path.join(GALLERIES_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK]  galleries/{slug}.html — {count} images")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Building Sam Wolson Photography site...")
    print()

    galleries_data = []
    for g in GALLERIES:
        imgs = get_images(g["slug"])
        galleries_data.append({**g, "images": imgs})

    print("Generating index.html...")
    build_index(galleries_data)

    print()
    print("Generating gallery pages...")
    for g in galleries_data:
        build_gallery(g)

    print()
    print("Done! Open index.html in your browser.")

if __name__ == "__main__":
    main()
