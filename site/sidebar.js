// Keep navigation and the current article's outline in one accessible tab panel.
(() => {
  const tablist = document.querySelector('.sidebar-tabs');
  if (!tablist) return;
  const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));

  function activate(selected, focus = false) {
    for (const tab of tabs) {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    }
    if (focus) selected.focus();
  }

  for (const [index, tab] of tabs.entries()) {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      activate(tabs[next], true);
    });
  }
  activate(tabs[0]);
  tablist.hidden = false;

  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('site-sidebar');
  if (!toggle || !sidebar) return;
  const home = document.querySelector('.site-header a');
  const storageKey = 'notebook:sidebar-hidden:' + new URL(home.href).pathname;

  function setHidden(hidden) {
    sidebar.hidden = hidden;
    document.body.classList.toggle('sidebar-hidden', hidden);
    toggle.setAttribute('aria-expanded', String(!hidden));
    toggle.textContent = hidden ? '显示导航' : '隐藏导航';
  }

  let savedHidden = false;
  try {
    savedHidden = window.localStorage.getItem(storageKey) === 'true';
  } catch (_) { /* Navigation remains usable when storage is unavailable. */ }
  setHidden(savedHidden);
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    setHidden(!sidebar.hidden);
    try {
      window.localStorage.setItem(storageKey, String(sidebar.hidden));
    } catch (_) { /* Saving the preference is optional. */ }
  });
})();
