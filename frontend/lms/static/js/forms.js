document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.password-toggle .toggle-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const input = btn.closest('.password-toggle').querySelector('input');
      const icon = btn.querySelector('i');
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      icon.classList.toggle('fa-eye', !isPassword);
      icon.classList.toggle('fa-eye-slash', isPassword);
    });
  });

  document.querySelectorAll('[data-match]').forEach((input) => {
    const matchId = input.dataset.match;
    const matchInput = document.getElementById(matchId);
    if (!matchInput) return;

    const validate = () => {
      const match = input.value === matchInput.value;
      input.classList.toggle('is-invalid', input.value && !match);
      let feedback = input.parentElement.querySelector('.invalid-feedback');
      if (!feedback && input.value && !match) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = 'Passwords do not match.';
        input.parentElement.appendChild(feedback);
      } else if (feedback && match) {
        feedback.remove();
      }
    };

    input.addEventListener('input', validate);
    matchInput.addEventListener('input', validate);
  });

  document.querySelectorAll('form[novalidate]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      let valid = true;
      form.querySelectorAll('[required]').forEach((field) => {
        if (!field.value.trim()) {
          field.classList.add('is-invalid');
          valid = false;
        } else {
          field.classList.remove('is-invalid');
        }
      });

      const confirmField = form.querySelector('[data-match]');
      if (confirmField) {
        const matchInput = document.getElementById(confirmField.dataset.match);
        if (matchInput && confirmField.value !== matchInput.value) {
          confirmField.classList.add('is-invalid');
          valid = false;
        }
      }

      if (!valid) e.preventDefault();
    });
  });

  document.querySelectorAll('[data-preview]').forEach((input) => {
    input.addEventListener('change', () => {
      const previewId = input.dataset.preview;
      const preview = document.getElementById(previewId);
      if (preview && input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => { preview.src = e.target.result; };
        reader.readAsDataURL(input.files[0]);
      }
    });
  });
});
