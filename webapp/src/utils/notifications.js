export function notify_failed(message, opts={}) {
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
  icon.className = 'notify-icon';
  icon.style.color = '#ff4d4f'; // red for failed
  icon.innerHTML = '✖'; // cross mark

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


(function ensureCartCompletedStyles(){
  if (document.getElementById('notify-cart-styles')) return;
  const css = `
  .cart-completed-container {
    position: fixed; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    display: flex; flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 99999;
  }
  .cart-completed-card {
    background: #292929ff;
    color: #fff;
    padding: 20px 30px;
    border-radius: 12px;
    width: 150px;
    height: 150px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    opacity: 0;
    transform: scale(0.8);
    transition: opacity 0.3s ease, transform 0.3s ease;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  }
  .cart-completed-card.show {
    opacity: 1;
    transform: scale(1);
  }
  .cart-completed-icon {
    font-size: 4rem;
    color: #4CAF50;
    animation: bounce 0.4s ease;
  }
  @keyframes bounce {
    0% { transform: scale(0); }
    50% { transform: scale(1.3); }
    100% { transform: scale(1); }
  }
  .cart-completed-text {
    font-size: 0.9rem;
    font-weight: bold;
    text-align: center;
    font-family: Arial;
  }
  `;
  const style = document.createElement('style');
  style.id = 'notify-cart-styles';
  style.textContent = css;
  document.head.appendChild(style);
})();

export function notify_cart_completed() {
  // Container
  let container = document.querySelector('.cart-completed-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'cart-completed-container';
    document.body.appendChild(container);
  }

  // Card
  const card = document.createElement('div');
  card.className = 'cart-completed-card';

  // Icon
  const icon = document.createElement('div');
  icon.className = 'cart-completed-icon';
  icon.innerHTML = '✔'; // big green check mark

  // Text
  const text = document.createElement('div');
  text.className = 'cart-completed-text';
  text.textContent = 'Cart Completed';

  // Assemble
  card.appendChild(icon);
  card.appendChild(text);
  container.appendChild(card);

  // Animate in
  requestAnimationFrame(() => card.classList.add('show'));

  // Auto-remove after 2.5s
  const remove = () => {
    card.classList.remove('show');
    card.addEventListener('transitionend', () => card.remove(), { once: true });
  };
  setTimeout(remove, 1000);

  // Remove on click
  card.addEventListener('click', remove);
}
