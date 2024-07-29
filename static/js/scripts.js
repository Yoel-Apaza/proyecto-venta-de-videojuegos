function showMore(id, btnId) {
    const element = document.getElementById(id);
    const btn = document.getElementById(btnId);
    if (element.classList.contains('truncated')) {
        element.classList.remove('truncated');
        btn.textContent = 'Ver menos';
    } else {
        element.classList.add('truncated');
        btn.textContent = 'Ver todos';
    }
}

document.querySelectorAll('.clickable-chart img').forEach(img => {
    img.addEventListener('click', () => {
        const fullscreen = document.getElementById('fullscreen');
        const fullscreenImg = document.getElementById('fullscreenImg');
        fullscreenImg.src = img.src;
        fullscreen.style.display = 'flex';
    });
});

document.getElementById('fullscreen').addEventListener('click', () => {
    const fullscreen = document.getElementById('fullscreen');
    fullscreen.style.display = 'none';
});

