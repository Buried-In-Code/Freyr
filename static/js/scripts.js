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

ready(setTheme);
