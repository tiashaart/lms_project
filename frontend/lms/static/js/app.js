document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('loadingOverlay');
  if (overlay) {
    window.addEventListener('load', () => overlay.classList.add('show'));
    setTimeout(() => overlay.classList.remove('show'), 500);
  }

  document.querySelectorAll('.menu-item').forEach((item) => {
    const href = item.getAttribute('href');
    if (href && window.location.pathname === new URL(href, window.location.origin).pathname) {
      item.classList.add('active');
    }
    item.addEventListener('click', () => {
      document.querySelectorAll('.menu-item').forEach((link) => link.classList.remove('active'));
      item.classList.add('active');
    });
  });

  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarToggleMobile = document.getElementById('sidebarToggleMobile');
  const sidebar = document.getElementById('sidebar');

  const toggleMobileSidebar = () => {
    if (!sidebar) return;
    sidebar.classList.toggle('open');
    let sidebarOverlay = document.querySelector('.sidebar-overlay');
    if (!sidebarOverlay) {
      sidebarOverlay = document.createElement('div');
      sidebarOverlay.className = 'sidebar-overlay';
      document.body.appendChild(sidebarOverlay);
      sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        sidebarOverlay.classList.remove('show');
      });
    }
    sidebarOverlay.classList.toggle('show');
  };

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('collapsed'));
  }
  if (sidebarToggleMobile) {
    sidebarToggleMobile.addEventListener('click', toggleMobileSidebar);
  }

  document.querySelectorAll('form:not([data-no-loading])').forEach((form) => {
    form.addEventListener('submit', () => {
      if (overlay) overlay.classList.add('show');
    });
  });

  document.querySelectorAll('[data-bs-toggle="modal"]').forEach((trigger) => {
    trigger.addEventListener('click', (e) => {
      const target = trigger.getAttribute('data-bs-target');
      if (target) {
        const modal = document.querySelector(target);
        if (modal) new bootstrap.Modal(modal).show();
      }
    });
  });
});
