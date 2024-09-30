document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  // Inicjalizacja kalendarza
  var calendar = new FullCalendar.Calendar(calendarEl, {
    // setCalendarView określa startowy widok zależnie od rozmiaru ekranu.
    initialView: setCalendarView(),
    locale: "pl",
    eventTimeFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
      omitZeroMinute: false,
    },
    eventDidMount: function (info) {
      // Wyświetlanie tooltipa z pełnym tytułem wydarzenia oraz krótkim opisem.
      info.el.setAttribute("title", `${info.event.title}\n\n${info.event.extendedProps.short_description}`)
    },
    events: [],
    // Wyświetlanie modalu ze szczegółowymi danymi wydarzenia po kliknięciu.
    eventClick: function (info) {
      const eventId = info.event.id;
      fetch(`/event/${eventId}`)
        .then((response) => response.text())
        .then(data => changeDialogContent(data))
        .catch(error => console.log('Error fetching data:', error));
    },
  });
  calendar.render();
  calendar.addEventSource(eventsData);

  function setCalendarView() {
    if (window.innerWidth < 1024) {
      return 'listWeek'
    } else {
      return 'dayGridMonth'
    }
  }

  //Aktualizacja widoku kalendarza przy zmianie rozmiaru okna.
  function changeCalendarView() {
    calendar.changeView(setCalendarView())
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
