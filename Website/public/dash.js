document.querySelectorAll('.item').forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.2)';
    });

    item.addEventListener('mouseleave', () => {
        item.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    });
});
