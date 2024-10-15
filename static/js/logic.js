
const display_name = document.body.dataset.displayName;

is_female = display_name.includes("המפקדת");
logout_msg = is_female ? "התנתקי" : "התנתק";

function takeSnapShot() {
    window.location.href = "/take_shot"
}

function goToHanich(display_name) {

    went_out_msg = ""
    if (is_female) {
        went_out_hebrew = display_name + " יצאה לפעמון ב"
    }
    else {
        went_out_hebrew = display_name + " יצא לפעמון ב"
    }
    fetch('record_who_went', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ display_name: went_out_hebrew })
    })
        .then(response => response.json())
        .then(data => {
            fethchEventsLog();
        })
        .catch(error => console.error('Error:', error));
}

function fethchEventsLog() {
    fetch('get_events_log').
        then(response => response.json())
        .then(data => {
            const events_log_div = document.getElementById('events-log');
            events_log_div.innerHTML = '';
            data.events.forEach(event => {
                const event_item = document.createElement('p');
                event_item.textContent = event;
                events_log_div.appendChild(event_item);

            });
        }).catch(error => console.error("errorr", error));
}

setInterval(fethchEventsLog, 5000);
window.onload = fethchEventsLog;