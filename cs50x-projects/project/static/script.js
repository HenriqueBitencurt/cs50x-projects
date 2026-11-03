document.addEventListener('DOMContentLoaded', () => {
    const timerDisplay = document.getElementById('timer');
    if (!timerDisplay) return;

    let timerInterval;
    let timeLeft = 25 * 60;
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resetBtn = document.getElementById('reset-btn');

    function updateDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    startBtn.addEventListener('click', () => {
        if (!timerInterval) {
            timerInterval = setInterval(() => {
                if (timeLeft > 0) {
                    timeLeft--;
                    updateDisplay();
                } else {
                    clearInterval(timerInterval);
                    timerInterval = null;
                    alert('Tempo de estudo concluído! Descansa um pouco.');
                }
            }, 1000);
        }
    });

    pauseBtn.addEventListener('click', () => {
        clearInterval(timerInterval);
        timerInterval = null;
    });

    resetBtn.addEventListener('click', () => {
        clearInterval(timerInterval);
        timerInterval = null;
        timeLeft = 25 * 60;
        updateDisplay();
    });

    updateDisplay();
});
