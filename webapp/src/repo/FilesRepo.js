import { ENDPOINTS } from "@/main";
import axios from "axios";
import {getAuthorizationToken} from "./AuthorizationRepo";

// Routes 
const ROUTE_FILE_UPLOAD = '/api/v1/upload'

export function uploadFile(file,callback){

    // Create the form data
    let formData = new FormData()
    formData.append('file',file)

    // Upload with axios 
    axios.post(ENDPOINTS.BASE_URL+ROUTE_FILE_UPLOAD,formData,{
        headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization' : getAuthorizationToken()
        }
    }).then(
        res => res.data
    ).then(res=>{
        callback(true,res)
    }).catch(err=>{
        callback(false,err)
    })
}