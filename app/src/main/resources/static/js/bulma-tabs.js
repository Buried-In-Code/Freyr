ready(() => {
  const tabs = document.querySelectorAll(".tabs ul li");
  const tabContents = document.querySelectorAll(".tab-content");

  const activateTab = (hash) => {
    tabs.forEach(tab => tab.classList.remove("is-active"));
    tabContents.forEach(content => content.classList.add("is-hidden"));

    const activeTab = document.querySelector(`a[href="${hash}"]`);
    if (activeTab) {
      activeTab.parentNode.classList.add("is-active");
      document.querySelector(hash).classList.remove("is-hidden");
    }
  };

  const initialHash = window.location.hash || tabs[0].querySelector("a").getAttribute("href");
  activateTab(initialHash);

  tabs.forEach(tab => {
    tab.addEventListener("click", (e) => {
      e.preventDefault();

      const target = tab.querySelector("a").getAttribute("href");
      window.location.hash = target;

      activateTab(target);
    });
  });

  window.addEventListener("hashchange", () => {
    activateTab(window.location.hash);
  });
});
