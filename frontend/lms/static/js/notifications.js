document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.notification-item').forEach((item) => {
    item.addEventListener('click', () => {
      item.classList.remove('unread');
      const badge = document.getElementById('navNotifBadge');
      if (badge) {
        const count = parseInt(badge.textContent, 10) - 1;
        if (count <= 0) badge.remove();
        else badge.textContent = count;
      }
    });
  });

  document.querySelectorAll('.notification-mark-read').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const form = btn.closest('form');
      const id = btn.dataset.id;
      try {
        const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;
        await fetch(form.action, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/json' },
        });
        btn.textContent = 'Marked as Read';
        btn.disabled = true;
        btn.classList.replace('btn-primary', 'btn-secondary');
        const badge = document.getElementById('navNotifBadge');
        if (badge) {
          const count = parseInt(badge.textContent, 10) - 1;
          if (count <= 0) badge.remove();
          else badge.textContent = count;
        }
      } catch (err) {
        console.warn('Mark read failed (demo mode)', err);
      }
    });
  });
});
