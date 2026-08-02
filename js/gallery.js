/* Horizontal strip — wheel redirect + click-drag + captions */
(function () {
  const strip = document.querySelector('.photo-strip');
  if (!strip) return;

  /* ── Insert captions under ALL images when any have data-caption ── */
  let hasCaptions = false;
  strip.querySelectorAll('.photo-item img').forEach(img => {
    if (img.dataset.caption) hasCaptions = true;
  });

  if (hasCaptions) {
    strip.classList.add('has-captions');
    strip.querySelectorAll('.photo-item').forEach(item => {
      const img = item.querySelector('img');
      const div = document.createElement('div');
      div.className = 'photo-caption';
      div.textContent = (img && img.dataset.caption) ? img.dataset.caption : '';
      item.appendChild(div);
    });
  }

  /* ── Redirect vertical wheel to horizontal scroll ─────── */
  strip.addEventListener('wheel', function (e) {
    e.preventDefault();
    strip.scrollLeft += e.deltaY + e.deltaX;
  }, { passive: false });

  /* ── Click-drag scrolling ──────────────────────────────── */
  let isDown = false, startX, scrollLeft;

  strip.addEventListener('mousedown', function (e) {
    if (e.button !== 0) return;
    isDown = true;
    strip.classList.add('dragging');
    startX = e.pageX - strip.offsetLeft;
    scrollLeft = strip.scrollLeft;
  });

  document.addEventListener('mouseup', function () {
    isDown = false;
    strip.classList.remove('dragging');
  });

  strip.addEventListener('mousemove', function (e) {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - strip.offsetLeft;
    strip.scrollLeft = scrollLeft - (x - startX) * 1.2;
  });
})();
