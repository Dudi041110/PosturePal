async function enableNotifications() {

    const permission =
        await Notification.requestPermission();

    if (permission !== "granted") return;

    // register service worker
    const register =
        await navigator.serviceWorker.register("/static/sw.js");

    const response =
        await fetch("/vapidPublicKey");

    const publicKey = await response.text();

    const subscription =
        await register.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey:
                urlBase64ToUint8Array(publicKey)
        });

    await fetch("/subscribe", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(subscription)
    });

    alert("Notifications enabled!");
}


// helper
function urlBase64ToUint8Array(base64String) {

    const padding =
        "=".repeat((4 - base64String.length % 4) % 4);

    const base64 =
        (base64String + padding)
        .replace(/-/g, "+")
        .replace(/_/g, "/");

    const rawData = atob(base64);
    const outputArray =
        new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i)
        outputArray[i] = rawData.charCodeAt(i);

    return outputArray;
}