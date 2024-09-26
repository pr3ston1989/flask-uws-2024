document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    events: [],
    eventClick: alert("!!!"),
  });
  calendar.render();

  calendar.addEventSource(eventsData);
});
