async function enableNotifications() {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") return;

    const register = await navigator.serviceWorker.register("/static/sw.js");
    const response = await fetch("/vapidPublicKey");
    const publicKey = await response.text();

    const subscription = await register.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(publicKey)
    });

    await fetch("/subscribe", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(subscription)
    });

    alert("Notifications enabled!");
}

// --- Sensitivity slider ---

const LABELS = [
    { max: 500,  label: "Very High" },
    { max: 1500, label: "High" },
    { max: 2500, label: "Medium" },
    { max: 3500, label: "Low" },
    { max: 5000, label: "Very Low" },
];

function onSliderInput(value) {
    const v = parseInt(value);
    document.getElementById("threshold-val").textContent = v;

    const entry = LABELS.find(l => v <= l.max) || LABELS[LABELS.length - 1];
    document.getElementById("sensitivity-label").textContent = entry.label;
}

let sendTimer = null;
async function sendSensitivity(value) {
    // Debounce: wait 300ms after the user stops dragging
    clearTimeout(sendTimer);
    sendTimer = setTimeout(async () => {
        try {
            const res = await fetch("/setSensitivity", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ value: parseInt(value) })
            });
            if (res.ok) {
                document.getElementById("sensitivity-status").textContent =
                    "✓ Device updated  ·  threshold: " + value;
            }
        } catch (e) {
            document.getElementById("sensitivity-status").textContent =
                "⚠ Couldn't reach server";
        }
    }, 300);
}

// --- helper ---
function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
    const rawData = atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i)
        outputArray[i] = rawData.charCodeAt(i);
    return outputArray;
}