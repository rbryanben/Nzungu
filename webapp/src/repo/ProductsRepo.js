import axios from "axios"
import {ENDPOINTS} from "../main.js"
import {DUMMY_PRODUCTS,DUMMY_FILTERS} from "./DummyData.js"
import getAuthorizationToken from "./AuthorizationRepo.js"

const ROUTE_CREATE_PRODUCT = '/api/v1/create-product'

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

export function generateReference(callback){
    setTimeout(()=>{
        callback(true,{
            reference : "7549daf3"
        })
    })
}

export function r_createProduct(product,callback){
    axios.post(ENDPOINTS.BASE_URL+ROUTE_CREATE_PRODUCT,product,{
        headers: {
            'Authorization' : getAuthorizationToken()
        }
    }).then(res => res.data)
    .then(res => {
        callback(true,res)
    })
    .catch(err => {
        callback(false,err)
    })
}
