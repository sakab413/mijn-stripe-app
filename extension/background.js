// Luister of een tabblad wordt bijgewerkt
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    
    // We checken of de gebruiker op een ondersteunde shop zit (bijv. Nike of Adidas)
    if (tab.url.includes("nike.com") || tab.url.includes("adidas.nl")) {
      
      console.log("Webshop herkend! Live data ophalen van Render...");

      // Jouw specifieke Render URL met de API-route erachter
      const apiUrl = 'https://mijn-stripe-app.onrender.com/api/check-cashback';

      fetch(apiUrl)
        .then(response => {
          if (!response.ok) throw new Error('Netwerk reageert niet');
          return response.json();
        })
        .then(data => {
          if (data.status === 'found') {
            // Maak de notificatie die de gebruiker te zien krijgt
            chrome.notifications.create({
              type: 'basic',
              iconUrl: 'icon.png',
              title: 'Cashback Alert! 💰',
              message: `Bij ${data.shop} krijg je nu €${data.amount} terug via EasyCashBack!`,
              priority: 2
            });
            console.log("Notificatie verstuurd voor:", data.shop);
          }
        })
        .catch(err => console.error("Fout bij ophalen van data:", err));
    }
  }
});
