document.addEventListener('DOMContentLoaded', function() {
    // Message close functionality
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        const closeBtn = message.querySelector('.close-message');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                message.remove();
            });
        }
    });

    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('show');
        });
    }
});