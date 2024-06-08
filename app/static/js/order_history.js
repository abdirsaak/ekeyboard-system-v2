





// .............. history managemnt

document.addEventListener('DOMContentLoaded', (event) => {
    const historyButton = document.querySelector('.history-btn');
    const historyModal = document.getElementById('history-modal');
    const closeHistoryModal = document.getElementById('close-history-modal');

    historyButton.addEventListener('click', () => {
        historyModal.style.display = 'block';
    });

    closeHistoryModal.addEventListener('click', () => {
        historyModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === historyModal) {
            historyModal.style.display = 'none';
        }
    });
});







document.querySelector('.checkout-button').addEventListener('click', () => {
    window.location.href = '/E-keyboard/place-order';
});







