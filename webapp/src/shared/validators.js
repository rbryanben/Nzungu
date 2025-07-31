export default {
    // Username validator 
    username : (s)=>{
        return s.length > 3 
    },
    // Password validator 
    password: (s)=>{
        return s.length > 5
    },
    // price
    price: (s) => {
        const num = parseFloat(s);
        return !isNaN(num) && num > 0;
    },
    // None validator
    none: (s)=>{
        return true
    }
}