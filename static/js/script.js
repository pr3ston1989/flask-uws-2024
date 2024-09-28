document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    locale: "pl",
    eventTimeFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
      omitZeroMinute: false,
    },
    eventDidMount: function (info) {
      info.el.setAttribute("title", info.event.title);
    },
    events: [],
    eventClick: function (info) {
      const eventId = info.event.id;
      fetch(`/event/${eventId}`)
        .then((response) => response.text())
        .then(data => changeDialogContent(data));
    },
  });
  calendar.render();

  calendar.addEventSource(eventsData);
});

function changeDialogContent(data) {

  const dialogDiv = document.querySelector(".event-info");
  dialogDiv.innerHTML = data
  const dialog = document.querySelector("dialog")
  dialog.showModal();
}

document.getElementById('close-dialog').addEventListener("click", (e) => {
  e.preventDefault();
  document.querySelector("dialog").close();
});
