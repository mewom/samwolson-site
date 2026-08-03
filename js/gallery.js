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

  /* ── Horizontal scrolling behaviour ────────────────────────
     Only applies on wide screens. Below 769px the strip is a
     vertical stack (see style.css), where hijacking the wheel
     would break normal page scrolling. Each handler checks the
     width itself so resizing and device rotation always behave. */
  const wide = window.matchMedia('(min-width: 769px)');

  strip.addEventListener('wheel', function (e) {
    if (!wide.matches) return;
    e.preventDefault();
    strip.scrollLeft += e.deltaY + e.deltaX;
  }, { passive: false });

  let isDown = false, startX, scrollLeft;

  strip.addEventListener('mousedown', function (e) {
    if (!wide.matches || e.button !== 0) return;
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
    if (!isDown || !wide.matches) return;
    e.preventDefault();
    const x = e.pageX - strip.offsetLeft;
    strip.scrollLeft = scrollLeft - (x - startX) * 1.2;
  });

  /* Dropping to stacked layout leaves a stale horizontal offset */
  wide.addEventListener('change', function () {
    if (!wide.matches) {
      isDown = false;
      strip.classList.remove('dragging');
      strip.scrollLeft = 0;
    }
  });
})();
