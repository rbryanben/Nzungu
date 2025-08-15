import axios from "axios"
import {ENDPOINTS} from "../main.js"
import {DUMMY_PRODUCTS,DUMMY_CATEGORIES} from "./DummyData.js"
import { generateUUID } from "@/utils/common.js"
import {getAuthorizationToken} from "./AuthorizationRepo.js"

const ROUTE_COMPLETE_CART = "/api/v1/complete-cart"
const ROUTE_GET_CATEGORIES = '/api/v1/get-categories'
const ROUTE_GET_PRODUCTS = '/api/v1/get-products'
const ROUTE_GET_UDPATED_PRODUCTS = '/api/v1/get-product-updates'
const ROUTE_GET_EMPLOYEE = '/api/v1/get-employee-details'
const LOCAL_STORE_KEY = "LOCAL_SALES_CACHE"

/*
    Fetches products from backend 
*/
export function getAllProducts(callback){
    axios.get(
        ENDPOINTS.BASE_URL + ROUTE_GET_PRODUCTS,
        {
            headers : {
                Authorization : getAuthorizationToken()
            }
        }
    )
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}

/*
    Fetches employee details
*/
export function getEmployeeDetails(callback){
    axios.get(
        ENDPOINTS.BASE_URL + ROUTE_GET_EMPLOYEE,
        {
            headers: {
                Authorization : getAuthorizationToken()
            }
        }
    )
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}

/*
    Get product updates 
*/
export function getUpdatedProducts(callback,lastUpdatedIsoDatetime){
    axios.get(
        `${ENDPOINTS.BASE_URL}${ROUTE_GET_UDPATED_PRODUCTS}?last-fetched-date-iso=${lastUpdatedIsoDatetime}`,
        {
            headers: {
                Authorization : getAuthorizationToken()
            }
        }
    )
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}

/*
    Fetches categories from backend
*/
export function getAllCategories(callback){
    axios.get(
        ENDPOINTS.BASE_URL + ROUTE_GET_CATEGORIES,
        {
            headers : {
                'Authorization' : getAuthorizationToken()
            }
        }
    )
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}

function writeToLocalStore(sale){
    // prev state 
    const prev_state = localStorage.getItem(LOCAL_STORE_KEY)

    // If null then create a new stat 
    if (prev_state === null){
        localStorage.setItem(LOCAL_STORE_KEY,JSON.stringify([sale]))
        return
    }

    // Append to prev stat 
    let prev_state_list = JSON.parse(prev_state)
    prev_state_list.push(sale)
    localStorage.setItem(LOCAL_STORE_KEY,JSON.stringify(prev_state_list))
}

/*
    Complete cart:
        - will try to commit to database : if failure will store to localstorage  
        - returns {
            "sale_reference" : string,
            "total_products" : integer
        }
*/
export function completeCart(callback,cart_productModelList,currency,idempotence_key,payment_option='CASH',username='no-username',shop='no-shop'){
    // Payload 
    let payload = {
        cart_items : cart_productModelList.map(item => item.toJson()),
        teller : username,
        shop : shop,
        currency: currency,
        idempotence_key: idempotence_key,
        payment_option: payment_option,
        commited : new Date().toISOString()
    }

    // Set the payload
    axios.post(ENDPOINTS.BASE_URL + ROUTE_COMPLETE_CART,payload,{
        headers: {
            'Authorization' : getAuthorizationToken()
        }
    })
    .then(res => res.data)
    .then(res => callback(true,res))
    .catch(err => {
        // store localy 
        writeToLocalStore(payload)
        callback(true,{
            'ref' : 'offline-sales-' + idempotence_key
        })
    })
}
