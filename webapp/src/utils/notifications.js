export function notify_failed(message) {
  alert(message)
}

(function ensureNotifyStyles(){
  if (document.getElementById('notify-toast-styles')) return;
  const css = `
  .notify-container {
    position: fixed; top: 16px; left: 50%;
    transform: translateX(-50%);
    display: flex; flex-direction: column; gap: 8px; z-index: 99999;
    align-items: center;
  }
  .notify-toast {
    display: flex; align-items: center; gap: 8px;
    background: #292929ff; color: #fff; padding: 10px 14px;
    border-radius: 5px; font: 0.85rem/1 system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    box-shadow: 0 6px 18px rgba(63, 63, 63, 0.35); max-width: 90vw;
    opacity: 0; transform: translateY(-10px);
    transition: opacity .25s ease, transform .25s ease;
  }
  .notify-toast.show { opacity: 1; transform: translateY(0); }
  .notify-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
  }
  .notify-icon.success {
    color: #4CAF50; /* green */
  }
  `;
  const style = document.createElement('style');
  style.id = 'notify-toast-styles';
  style.textContent = css;
  document.head.appendChild(style);
})();

export function notify_success(message, opts={}) {
  const { timeout = 3000 } = opts;

  // Create container once
  let container = document.querySelector('.notify-container');
  if (!container){
    container = document.createElement('div');
    container.className = 'notify-container';
    container.setAttribute('aria-live', 'polite');
    container.setAttribute('aria-atomic', 'true');
    document.body.appendChild(container);
  }

  // Create toast
  const toast = document.createElement('div');
  toast.className = 'notify-toast';

  // Icon
  const icon = document.createElement('span');
  icon.className = 'notify-icon success';
  icon.innerHTML = '✔'; // simple check mark

  // Text
  const text = document.createElement('span');
  text.textContent = String(message ?? '');

  // Assemble
  toast.appendChild(icon);
  toast.appendChild(text);
  container.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => toast.classList.add('show'));

  // Auto-remove after timeout
  const remove = () => {
    toast.classList.remove('show');
    toast.addEventListener('transitionend', () => toast.remove(), { once: true });
  };
  const timer = setTimeout(remove, timeout);

  // Remove on click
  toast.addEventListener('click', () => {
    clearTimeout(timer);
    remove();
  });
}
