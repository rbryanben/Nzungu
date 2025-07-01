import {ENDPOINTS} from "../main.js"
import {DUMMY_PRODUCTS,DUMMY_CATEGORIES} from "./DummyData.js"
 
/*
    Fetches products from backend 
*/
export function getAllProducts(callback){
    setTimeout(()=>{
        callback(true,DUMMY_PRODUCTS)
    },1000)
}


/*
    Fetches categories from backend
*/
export function getAllCategories(callback){
    setTimeout(()=>{
        callback(true,DUMMY_CATEGORIES)
    },800)
}