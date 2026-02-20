// ══════════════════════════════════════
//  BEST4YOU — Main JS
// ══════════════════════════════════════

// Auto-dismiss flash messages after 4 seconds
document.querySelectorAll('.flash').forEach(function(el) {
  setTimeout(function() {
    el.style.transition = 'opacity 0.4s';
    el.style.opacity = '0';
    setTimeout(function() { el.remove(); }, 400);
  }, 4000);
});

// Highlight active nav category link
(function() {
  var params = new URLSearchParams(window.location.search);
  var cat = params.get('category');
  if (!cat) return;
  document.querySelectorAll('.nav-center a').forEach(function(a) {
    if (a.href.includes('category=' + cat)) {
      a.style.color = 'var(--text)';
      a.style.fontWeight = '800';
    }
  });
})();

// Confirm delete on any delete form (extra safety)
document.querySelectorAll('form[action*="delete"]').forEach(function(form) {
  form.addEventListener('submit', function(e) {
    if (!confirm('Are you sure you want to delete this post? This cannot be undone.')) {
      e.preventDefault();
    }
  });
});
