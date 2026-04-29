const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); }
    });
}, { threshold: 0.1 });
reveals.forEach(r => observer.observe(r));