import axios from "axios"
import {ENDPOINTS} from "../main.js"
import {DUMMY_PRODUCTS,DUMMY_FILTERS} from "./DummyData.js"
import {getAuthorizationToken} from "./AuthorizationRepo.js"

const ROUTE_CREATE_PRODUCT = '/api/v1/create-product'
const ROUTE_GET_STOCK_FILTERS = '/api/v1/get-products-stock-filters'
const ROUTE_GET_PRODUCT = '/api/v1/get-product'
const ROUTE_UPDATE_PRODUCT = '/api/v1/update-product'
const ROUTE_ADD_STOCK = '/api/v1/add-stock'

export function getProductsInventory(callback){
    setTimeout(()=>{
        callback(true,DUMMY_PRODUCTS)
    },1000)
}

/*
    Retrieve a product from the backend
*/
export function r_getProduct(callback,productReference){
    axios.get(ENDPOINTS.BASE_URL + ROUTE_GET_PRODUCT,{
        headers: {
            Authorization : getAuthorizationToken()
        },
        params: {
            reference : productReference
        }
    }).then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}

/*
    Fetch stock filters from the server
*/
export function getFilters(callback){
    axios.get(ENDPOINTS.BASE_URL + ROUTE_GET_STOCK_FILTERS,{
        headers: {
            Authorization: getAuthorizationToken()
        }
    })
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
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

export function r_updateProduct(product,reference,callback){
    axios.put(
        ENDPOINTS.BASE_URL + ROUTE_UPDATE_PRODUCT,
        product,
        {
            headers: {
                Authorization: getAuthorizationToken()
            },
            params: {
                product_reference: reference
            }
        }
    ).then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}


export function r_addStock(stockPayload,callback){
    axios.post(ENDPOINTS.BASE_URL + ROUTE_ADD_STOCK,
        stockPayload,
        {
            headers: {
                'Authorization' : getAuthorizationToken()
            }
        }  
    ).then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}