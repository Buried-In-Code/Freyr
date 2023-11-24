const TABS = document.querySelectorAll('#tabs li');
const CONTENT = document.querySelectorAll('#tab-content div');
const ACTIVE_CLASS = 'is-active';

function initTabs() {
  TABS.forEach((tab) => {
    tab.addEventListener('click', () => {
      const selected = tab.getAttribute('data-tab');
      updateActiveElement(TABS, tab);
      updateActiveElement(CONTENT, selected, 'data-content');
    });
  });
}

function updateActiveElement(elements, target, attribute = null) {
  elements.forEach((item) => {
    if (item && item.classList.contains(ACTIVE_CLASS)) {
      item.classList.remove(ACTIVE_CLASS);
    }

    const data = attribute ? item.getAttribute(attribute) : null;

    if (data === target) {
      item.classList.add(ACTIVE_CLASS);
    }
  });
}

ready(initTabs);
