// ── Scroll reveal ──────────────────────────────────────────────
const reveals = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) e.target.classList.add('visible');
    });
}, { threshold: 0.08 });
reveals.forEach(r => revealObserver.observe(r));


// ── Live device mockup simulation ──────────────────────────────
const angleVal  = document.getElementById('angleVal');
const angleBar  = document.getElementById('angleBar');
const statusEl  = document.querySelector('.screen-status');
const s1Val     = document.getElementById('s1');
const s2Val     = document.getElementById('s2');
const topSensor = document.getElementById('topSensor');
const botSensor = document.getElementById('botSensor');

// Smoothly oscillates between "good" and "bad" posture states
let angle = 4;
let target = 4;
let direction = 1;
let badTimer = 0;

function pickNewTarget() {
    // Occasionally simulate a bad posture event
    const gosBad = Math.random() < 0.3;
    return gosBad
        ? Math.floor(Math.random() * 10) + 14   // 14–24° — bad
        : Math.floor(Math.random() * 10) + 2;   // 2–12° — good
}

function updateMockup() {
    // Drift angle toward target
    const diff = target - angle;
    angle += diff * 0.04;

    const rounded = Math.round(angle * 10) / 10;
    const isBad = rounded > 12;

    // Angle value
    angleVal.textContent = rounded.toFixed(1) + '°';

    // Bar fill: map 0–30° to 0–100%
    const pct = Math.min(100, (rounded / 30) * 100);
    angleBar.style.width = pct + '%';
    angleBar.style.background = isBad
        ? 'linear-gradient(to right, #ffb347, #ff6b6b)'
        : 'linear-gradient(to right, var(--accent), var(--accent2))';

    // Angle value colour
    angleVal.style.color = isBad ? 'var(--accent3)' : 'var(--accent)';

    // Status badge
    statusEl.textContent = isBad ? '● Alert' : '● Good';
    statusEl.className = 'screen-status ' + (isBad ? 'bad' : 'good');

    // Sensor status labels
    s1Val.textContent = isBad ? 'SLIP' : 'OK';
    s1Val.style.color = isBad ? 'var(--accent3)' : 'var(--accent)';
    s2Val.textContent = isBad ? 'SLIP' : 'OK';
    s2Val.style.color = isBad ? 'var(--accent3)' : 'var(--accent)';

    // Sensor dots on mini spine
    if (topSensor && botSensor) {
        topSensor.style.boxShadow = isBad
            ? '0 0 10px var(--accent3)'
            : '0 0 10px var(--accent)';
        botSensor.style.boxShadow = isBad
            ? '0 0 10px var(--accent3)'
            : '0 0 10px var(--accent2)';
    }

    // Pick a new target once we're close enough
    if (Math.abs(diff) < 0.3) {
        target = pickNewTarget();
    }
}

setInterval(updateMockup, 50);
