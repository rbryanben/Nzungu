import axios from "axios"
import {ENDPOINTS} from "../main.js"
import {DUMMY_PRODUCTS,DUMMY_FILTERS} from "./DummyData.js"

export function getProductsInventory(callback){
    setTimeout(()=>{
        callback(true,DUMMY_PRODUCTS)
    },1000)
}

export function getFilters(callback){
    setTimeout(()=>{
        callback(true,DUMMY_FILTERS)
    },500)
}