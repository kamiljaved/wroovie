
let notificationsElement = document.getElementById("notifications");
let notificationWrapper = document.getElementById("notification-wrapper");
const notificationTransitionTimeout = 300;    // milliseconds

// console.log(notificationWrapper);

document.onload = function() {
    notificationWrapper.focus();
}


function showNotifications() {
    notificationsElement.style.display = "block";
}

function clearHideNotfications() {
    notificationWrapper.style.opacity = "0";
    setTimeout(function() {
        notificationsElement.style.display = "none";
        notificationWrapper.innerHTML = "";
        notificationWrapper.style.opacity = "100";
    }, notificationTransitionTimeout)
}

function hideNotifications() {
    notificationsElement.style.display = "none";
}

notificationsElement.addEventListener("keydown", function(event) {
    // console.log(event.keyCode);
    if (event.keyCode === 27) {
        hideNotifications();
    }
});

function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
  }

function addNotification(notification, type) {
    if (notification === "You are now Logged Out" || notification === "Successfully Logged In")
        return
    let date = new Date()
    let notification_html = `<div class="notification notification-${type}"><span class="timestamp">[${pad(date.getDay(), 2)}-${pad(date.getMonth()+1, 2)}-${date.getFullYear()} ${pad(date.getHours(), 2)}:${pad(date.getMinutes(), 2)}:${pad(date.getSeconds(), 2)}]</span> ${notification}</div>`;
    notificationWrapper.innerHTML = notification_html + "\n" + notificationWrapper.innerHTML;
    showNotifications();
}

document.getElementById("clear-notif-btn").addEventListener("click", function(e) {
    e.stopPropagation();
    clearHideNotfications();
})