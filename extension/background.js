setInterval(() => {
    // VERVANG DE LINK HIERONDER DOOR JOUW ECHTE RENDER LINK!
    fetch("https://mijn-stripe-app.onrender.com")
    .then(response => response.json())
    .then(data => {
        if (data.status === "found") {
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icon.png',
                title: 'Geld Terug Gevonden! 🎉',
                message: 'Je hebt €' + data.deals[0].cashback + ' verdiend bij ' + data.deals[0].shop,
                priority: 2
            });
        }
    })
    .catch(error => console.log("Nog geen data gevonden..."));
}, 60000); // Checkt elke minuut
