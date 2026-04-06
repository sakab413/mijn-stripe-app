// Luister of een tabblad wordt bijgewerkt (bijv. als iemand naar Nike.com gaat)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    
    // We checken of de gebruiker op een ondersteunde shop zit
    if (tab.url.includes("nike.com") || tab.url.includes("adidas.nl")) {
      
      console.log("Webshop herkend! Data ophalen uit database...");

      // VERVANG ONDERSTAANDE URL DOOR JOUW EIGEN RENDER URL
      fetch('https://JOUW-APP-NAAM.onrender.com/api/check-cashback')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'found') {
            // Maak een echte Windows/Mac notificatie
            chrome.notifications.create({
              type: 'basic',
              iconUrl: 'icon.png',
              title: 'Cashback Alert! 💰',
              message: `Bij ${data.shop} krijg je nu €${data.amount} terug via EasyCashBack!`,
              priority: 2
            });
          }
        })
        .catch(err => console.error("Kon geen data ophalen van Render:", err));
    }
  }
});
