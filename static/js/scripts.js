const HEADERS = {
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
};

function ready(callback) {
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", callback);
  else
    callback();
}

function getCookie(cname) {
  const name = cname + "=";
  const cookies = decodeURIComponent(document.cookie).split(";");

  for (const cookie of cookies) {
    let _cookie = cookie.trim();
    if (_cookie.indexOf(name) == 0)
      return _cookie.substring(name.length);
  }
  return "";
}

function addLoading(caller) {
  const element = document.getElementById(caller);
  element.classList.add("is-loading");
}

function removeLoading(caller) {
  const element = document.getElementById(caller);
  element.classList.remove("is-loading");
}

function resetForm(page) {
  window.location = page;
}

function setTheme() {
  const darkCss = document.getElementById("dark-theme");
  const lightCss = document.getElementById("light-theme");
  const theme = getCookie("freyr_theme");

  if (darkCss !== null && lightCss !== null) {
    darkCss.disabled = theme == "dark";
    lightCss.disabled = theme == "light";
  }
}

function toggleTheme() {
  const currentTheme = getCookie("freyr_theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  document.cookie = `freyr_theme=${newTheme}; path=/; max-age=${60 * 60 * 24 * 30}; SameSite=Strict`;
  setTheme();
}

ready(setTheme);

async function submitRequest(endpoint, method, body = {}) {
  try {
    const options = {
      method: method,
      headers: HEADERS,
    };
    if (method !== "GET")
      options.body = JSON.stringify(body);

    const response = await fetch(endpoint, options);

    if (!response.ok)
      throw response;
    return response.status !== 204 ? response.json() : "";
  } catch(error) {
    return null;
  }
}
