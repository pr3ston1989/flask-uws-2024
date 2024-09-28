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
      info.el.setAttribute("title", `${info.event.title}\n\n${info.event.extendedProps.short_description}`)
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
  function changeCalendarView() {
    if (window.innerWidth < 1024) {
      calendar.changeView('timeGridDay')
    } else {
      calendar.changeView('dayGridMonth')
    }
  }
  
  window.addEventListener('resize', changeCalendarView)
});



const dialog = document.querySelector("dialog")
const dialogCloseBtn = document.getElementById('close-dialog')

function changeDialogContent(data) {
  const dialogDiv = document.querySelector(".event-info");
  dialogDiv.innerHTML = data
  dialog.showModal();
}

dialogCloseBtn.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.close();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape')
    dialog.close()
})
