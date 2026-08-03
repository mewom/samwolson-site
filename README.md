# samwolson.com

Portfolio site for Sam Wolson — visual journalist, director, photographer.

Static HTML/CSS/JS. No build step. Deployed via Netlify on push to `main`.

## Structure

```
new-yorker.html      homepage — Timeline + Grid views, tag/publication filters
landing.html         alternate landing page
galleries/           one page per photo series
images/              web-optimized assets (max 2400px, JPEG q82)
css/style.css        shared styles
js/gallery.js        gallery strips + captions
js/lightbox.js       fullscreen image viewer
```

Project pages (`reeducated.html`, `we-who-remain.html`, `oka.html`, `volum.html`,
`atf.html`) live at the root.

## Local preview

```bash
cd ~/Desktop/Website && python3 -m http.server 8765
```

Then open http://localhost:8765/new-yorker.html

## Images

Full-resolution originals are kept locally in `images_originals/` and are
excluded from git. The versions in `images/` are downscaled for web delivery —
re-export from the originals if you ever need print quality.
