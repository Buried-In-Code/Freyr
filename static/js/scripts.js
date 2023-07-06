const unique = (arr) => [...new Set(arr)];
const headers = {
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
};

function ready(fn) {
  if (document.readyState !== 'loading') {
    fn();
    return;
  }
  document.addEventListener('DOMContentLoaded', fn);
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function addLoading(caller){
  let element = document.getElementById(caller);
  element.classList.add("is-loading");
}

function removeLoading(caller){
  let element = document.getElementById(caller);
  element.classList.remove("is-loading");
}

function setTheme(){
  let darkCss = document.getElementById("dark-theme");
  let lightCss = document.getElementById("light-theme");
  let theme = getCookie("theme");
  if (theme == "light"){
    darkCss.disabled = true;
    lightCss.disabled = false;
  } else {
    darkCss.disabled = false;
    lightCss.disabled = true;
  }
}

function changeTheme(){
  let currentTheme = getCookie("theme");
  let newTheme = "dark";
  if (currentTheme == "dark")
    newTheme = "light";

  document.cookie = `theme=${newTheme};path=/;max-age=${60*60*24*30};SameSite=Strict`;
  setTheme();
}

function statEntry(id, value) {
  return `<h4 class="subtitle has-text-centered has-text-info" id="${id}">${value}</h4>`
}

function createColumn(device) {
  let timeEntry = `<p class="has-text-centered" id="${device}-time">{time}</p>`;
  let tempEntry = statEntry(`${device}-temp`, "{temp}")
  let humidEntry = statEntry(`${device}-humid`, "{humid}")
  let newColumn = `<div class="box has-text-centered" id="${device}"><h3 class="subtitle">${device}</h3><div class="columns is-mobile"><div class="column is-half">${tempEntry}</div><div class="column is-half">${humidEntry}</div></div>${timeEntry}</div>`;
  let columnsRoot = document.getElementById("content");
  columnsRoot.insertAdjacentHTML("beforeend",newColumn);
}

function updateStats() {
  fetch("/api/devices", {
    method: "GET",
    headers: headers
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      data.forEach((entry) => {
        let column = document.getElementById(entry.device)
        if (column == null)
          createColumn(entry.device)
        if (entry.entries.length > 0)
          updateColumn(entry.device, entry.entries[0])
      })
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}

function updateColumn(device, entry){
  let timeLabel = document.getElementById(`${device}-time`);
  timeLabel.textContent = moment(entry.timestamp, "YYYY-MM-DD[T]hh:mm:ss").fromNow();
  let tempLabel = document.getElementById(`${device}-temp`);
  tempLabel.textContent = `${entry.temperature}°C`;
  let humidLabel = document.getElementById(`${device}-humid`);
  humidLabel.textContent = `${entry.humidity}%`;
}
