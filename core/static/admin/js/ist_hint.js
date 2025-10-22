// admin/js/ist_hint.js
document.addEventListener('DOMContentLoaded', function() {
    const dtInputs = document.querySelectorAll('input[type="datetime-local"]');
    dtInputs.forEach(input => {
        const hint = document.createElement('span');
        hint.style.marginLeft = '10px';
        hint.style.color = 'gray';
        hint.textContent = '+05:30 IST';
        input.parentNode.appendChild(hint);
    });
});