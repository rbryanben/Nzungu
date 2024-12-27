export default {
    // Username validator 
    username : (s)=>{
        return s.length > 3 
    },
    // Password validator 
    password: (s)=>{
        return s.length > 5
    } 
}