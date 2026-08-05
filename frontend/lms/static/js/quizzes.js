document.addEventListener('DOMContentLoaded', () => {
  const timerEl = document.getElementById('quizTimer');
  const progressEl = document.getElementById('quizProgress');
  const questions = document.querySelectorAll('.quiz-question');
  const totalQuestions = questions.length;

  if (timerEl) {
    let timeLeft = parseInt(timerEl.dataset.time || '600', 10);
    const interval = setInterval(() => {
      const minutes = Math.floor(timeLeft / 60);
      const seconds = timeLeft % 60;
      timerEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
      if (timeLeft <= 60) timerEl.classList.add('warning');
      timeLeft -= 1;
      if (timeLeft < 0) {
        clearInterval(interval);
        timerEl.textContent = 'Time up';
        document.getElementById('quizForm')?.requestSubmit();
      }
    }, 1000);
  }

  document.querySelectorAll('.quiz-option input').forEach((input) => {
    input.addEventListener('change', () => {
      const options = input.closest('.quiz-options').querySelectorAll('.quiz-option');
      options.forEach((opt) => opt.classList.remove('selected'));
      input.closest('.quiz-option').classList.add('selected');
      updateProgress();
    });
  });

  function updateProgress() {
    if (!progressEl || !totalQuestions) return;
    const answered = document.querySelectorAll('.quiz-option input:checked').length;
    progressEl.style.width = `${(answered / totalQuestions) * 100}%`;
  }
});
