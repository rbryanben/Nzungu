import { notify_failed } from "./notifications";

export function generateUUID() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

export function handleAxiosError(error, options = {}) {
  const {
    notify = true,
    notifyFunction = notify_failed, // your notification function
    onUnauthorized = null,         // optional callback for 401
    onForbidden = null,            // optional callback for 403
    onServerError = null,          // optional callback for 500
    fallback = null                // optional fallback callback
  } = options;

  let message = 'An unexpected error occurred.';

  if (error.response) {
    const { status, data } = error.response;

    switch (status) {
      case 401:
        message = 'Unauthorized - Please log in again.';
        if (typeof onUnauthorized === 'function') onUnauthorized(error);
        return;

      case 403:
        message = 'Forbidden - You do not have permission.';
        if (typeof onForbidden === 'function') onForbidden(error);
        return;

      case 500:
        message = 'Server error - Please try again later.';
        if (typeof onServerError === 'function') onServerError(error);
        return;

      default:
        message = data?.message || `Error: ${status}`;
        if (typeof fallback === 'function') fallback(error);
        return;
    }

    if (notify && typeof notifyFunction === 'function') {
      notifyFunction(message);
    }

    return null;
  }

  if (error.request) {
    message = 'Network error - Please check your internet connection.';
    if (notify && typeof notifyFunction === 'function') {
      notifyFunction(message);
    }
    return null;
  }

  // Fallback for non-Axios errors
  if (notify && typeof notifyFunction === 'function') {
    notifyFunction(message);
  }

  return null;
}


export function formatTwoDecimals(value) {
    // Ensure the value is a number
    const number = Number(value);
    if (isNaN(number)) {
        throw new Error("Invalid number");
    }
    // Return the number with 2 decimal places
    return number.toFixed(2);
}

export function isoToHumanReadable(isoString) {
    const date = new Date(isoString);

    // Options for formatting
    const options = {
        weekday: 'long',      // "Monday"
        year: 'numeric',      // "2025"
        month: 'long',        // "August"
        day: 'numeric',       // "20"
        hour: '2-digit',      // "04 PM"
        minute: '2-digit',    // "45"
        second: '2-digit',    // "30"
        hour12: true           // 12-hour format
    };

    return date.toLocaleString('en-US', options);
}