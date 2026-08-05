document.addEventListener('DOMContentLoaded', () => {
  const chartColors = {
    primary: '#2563EB',
    secondary: '#1E40AF',
    accent: '#F59E0B',
    muted: '#94A3B8',
  };

  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,.05)' } },
      x: { grid: { display: false } },
    },
  };

  const progressChart = document.getElementById('progressChart');
  if (progressChart) {
    new Chart(progressChart, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Progress',
          data: [20, 35, 45, 55, 68, 82],
          borderColor: chartColors.primary,
          backgroundColor: 'rgba(37,99,235,.1)',
          fill: true,
          tension: 0.4,
        }],
      },
      options: defaultOptions,
    });
  }

  const instructorChart = document.getElementById('instructorChart');
  if (instructorChart) {
    new Chart(instructorChart, {
      type: 'bar',
      data: {
        labels: ['UI/UX', 'Design Systems', 'Prototyping', 'Research'],
        datasets: [{
          label: 'Completion Rate',
          data: [92, 88, 85, 90],
          backgroundColor: [chartColors.primary, chartColors.secondary, chartColors.accent, chartColors.muted],
          borderRadius: 8,
        }],
      },
      options: { ...defaultOptions, scales: { y: { beginAtZero: true, max: 100 } } },
    });
  }

  const adminUserChart = document.getElementById('adminUserChart');
  if (adminUserChart) {
    new Chart(adminUserChart, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Users',
          data: [8500, 9200, 10100, 10800, 11500, 12450],
          borderColor: chartColors.primary,
          backgroundColor: 'rgba(37,99,235,.1)',
          fill: true,
          tension: 0.4,
        }],
      },
      options: defaultOptions,
    });
  }

  const adminEnrollmentChart = document.getElementById('adminEnrollmentChart');
  if (adminEnrollmentChart) {
    new Chart(adminEnrollmentChart, {
      type: 'doughnut',
      data: {
        labels: ['Design', 'Development', 'Business', 'Data Science'],
        datasets: [{
          data: [35, 40, 15, 10],
          backgroundColor: [chartColors.primary, chartColors.secondary, chartColors.accent, chartColors.muted],
        }],
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } },
    });
  }
});
