new Calendar({
    id: '#color-calendar',
    eventsData: myEvents,
    primaryColor: '#446878',
    headerColor: '#13445A',
    headerBackgroundColor: 'black',
    weekdaysColor: 'based on theme',

    dateChanged: (currentDate, events) => {
        const eventDisplay = document.getElementById("events-display");
        let html = "";
        events.forEach((event) => {
            let time = new Date(event.start).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

            html += `
        <a class="button is-info is-outlined is-fullwidth is-small" href="${event.url}">
        <span class="icon"><i class="fas fa-user"></i></span>
        <span class="span">${event.name}</span>
          <span class="icon"><i class="fas fa-clock"></i></span> <span>${time}</span>
        </a>
      `;
        });
        eventDisplay.innerHTML = html;
    }
})

