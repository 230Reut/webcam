
const display_name = document.body.dataset.displayName;

is_female = display_name.includes("המפקדת");
logout_msg = isFemale? "התנתקי":"התנתק";

function takeSnapShot() {
    window.location.href = "/take_shot"
}

function goToHanich(display_name) {

    if (is_female){   
        console.log(display_name + " יצאה לפעמון");
    }
    else {
        console.log(display_name + "יצא לפעמון");
    }

    const timestamp = new Date().toLocaleTimeString();
    const log_entry = document.createElement('li');
    log_entry.textContent = timestamp + " " + display_name + " יצאה לפעמון";
    const log_list = document.getElementById('log-list');
    log_list.appendChild(log_entry);
}