chrome.alarms.create("checkCashback", { periodInMinutes: 1 });

chrome.alarms.onAlarm.addListener(() => {
  fetch("https://mijn-stripe-app.onrender.com")
    .then(res => res.json())
    .then(data => {
      if (data.deals && data.deals.length > 0) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png", // Zorg dat je een klein icon.png in de map hebt
          title: "Geld Terug! 🎉",
          message: `Je hebt zojuist €${data.deals[0].cashback} cashback verdiend bij ${data.deals[0].shop}!`
        });
      }
    });
});
