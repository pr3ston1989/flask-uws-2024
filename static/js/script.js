document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    locale: "pl",
    eventDidMount: function (info) {
      info.el.setAttribute("title", info.event.title);
    },
    events: [],
    eventClick: function (info) {
      const eventId = info.event.id;
      console.log(eventId);
      fetch(`/event/${eventId}`)
        .then((response) => response.json())
        .then((data) => {
          changeDialogContent(data);
        });
    },
  });
  calendar.render();

  calendar.addEventSource(eventsData);
});

function changeDialogContent(data) {
  const dialog = document.querySelector("dialog");
  const title = document.getElementById("event-title");
  const description = document.getElementById("event-description");

  title.textContent = data.name;
  description.textContent = data.long_description;

  dialog.showModal();
}

document.querySelector("dialog button").addEventListener("click", (e) => {
  e.preventDefault();
  document.querySelector("dialog").close();
});
