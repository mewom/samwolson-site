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
     The strip deliberately has NO wheel handler. Vertical wheel
     and trackpad gestures are left alone so they scroll the page
     instead of dragging the photos sideways. Horizontal intent —
     a two-finger sideways swipe, shift+wheel, or the click-drag
     below — scrolls the strip through the browser's own
     overflow-x handling.

     Drag applies on wide screens only; below 769px the strip is a
     vertical stack (see style.css). The handlers check the width
     themselves so resizing and rotation always behave. */
  const wide = window.matchMedia('(min-width: 769px)');

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
