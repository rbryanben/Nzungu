export default {
    // Username validator 
    username: (s) => {
        return typeof s === "string" && s.length > 3;
    },
    // Password validator 
    password: (s) => {
        return typeof s === "string" && s.length > 5;
    },
    // Price validator (positive number)
    price: (s) => {
        const num = parseFloat(s);
        return !isNaN(num) && num > 0;
    },
    // Number validator (allows integers & floats)
    number: (s) => {
        if (s === null || s === undefined) return false;
        return !isNaN(s) && isFinite(s);
    },
    // Date validator (checks if valid date string)
    date: (dateString) => {
        // Check format (yyyy-mm-dd)
        const regex = /^\d{4}-\d{2}-\d{2}$/;
        if (!regex.test(dateString)) return false;

        // Parse values
        const [year, month, day] = dateString.split("-").map(Number);

        // Month must be 1–12
        if (month < 1 || month > 12) return false;

        // Create Date object
        const date = new Date(dateString);

        // Validate exact year, month, day match (to avoid auto-fix like 2025-02-30 → Mar 2)
        return (
            date.getFullYear() === year &&
            date.getMonth() + 1 === month &&
            date.getDate() === day
        );
    },
    // None validator
    none: () => true,
}
