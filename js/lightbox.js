/* ============================================================
   Sam Wolson Photography — Lightbox
   Vanilla JS, no dependencies
   ============================================================ */

(function () {
  'use strict';

  let images = [];
  let current = 0;

  const lb       = document.getElementById('lightbox');
  const lbImg    = document.getElementById('lb-img');
  const lbPrev   = document.getElementById('lb-prev');
  const lbNext   = document.getElementById('lb-next');
  const lbClose  = document.getElementById('lb-close');
  const lbCount  = document.getElementById('lb-counter');
  const lbCap    = document.getElementById('lb-caption');

  if (!lb) return;

  /* ── Collect all photo items ──────────────────────────── */
  function init() {
    const items = document.querySelectorAll('.photo-item');
    images = Array.from(items).map(el => {
      const img = el.querySelector('img');
      return { src: img.src, alt: img.alt, caption: img.dataset.caption || '' };
    });

    items.forEach((el, i) => {
      el.addEventListener('click', () => open(i));
    });
  }

  /* ── Open ─────────────────────────────────────────────── */
  function open(index) {
    current = index;
    show();
  }

  function show() {
    const { src, alt, caption } = images[current];
    lbImg.src = src;
    lbImg.alt = alt;
    lbCount.textContent = `${current + 1} / ${images.length}`;
    if (lbCap) {
      lbCap.textContent = caption;
      lbCap.style.display = caption ? 'block' : 'none';
    }
    lb.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  /* ── Close ────────────────────────────────────────────── */
  function close() {
    lb.classList.remove('active');
    document.body.style.overflow = '';
    lbImg.src = '';
  }

  /* ── Navigate ─────────────────────────────────────────── */
  function prev() {
    current = (current - 1 + images.length) % images.length;
    show();
  }

  function next() {
    current = (current + 1) % images.length;
    show();
  }

  /* ── Event listeners ──────────────────────────────────── */
  lbPrev.addEventListener('click', (e) => { e.stopPropagation(); prev(); });
  lbNext.addEventListener('click', (e) => { e.stopPropagation(); next(); });
  lbClose.addEventListener('click', close);

  lb.addEventListener('click', (e) => {
    if (e.target === lb || e.target.classList.contains('lb-inner')) close();
  });

  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('active')) return;
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   prev();
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown')  next();
    if (e.key === 'Escape') close();
  });

  let touchStartX = 0;
  lb.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) dx < 0 ? next() : prev();
  });

  /* ── Boot ─────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
