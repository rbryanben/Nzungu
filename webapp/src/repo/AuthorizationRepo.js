import { ENDPOINTS } from "@/main"
import axios from "axios"

// Routes
const ROUTE_AUTHENTICATE = '/api/v1/authenticate'
const ROUTE_CHECK_FEATURE_FLAG = '/api/v1/check-feature-flag'

export function getAuthorizationToken() {
  const token = sessionStorage.getItem('authorization');

  if (token && typeof token === 'string' && token.trim() !== '') {
    return token;
  }

  return 'mock-token';
}

export function r_authenticate(credentials,callback){
    axios.post(
        ENDPOINTS.BASE_URL + ROUTE_AUTHENTICATE,
        credentials
    )
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}

export function r_checkFeatureFlag(feature,callback){
    axios.get(
        ENDPOINTS + ROUTE_CHECK_FEATURE_FLAG,{
            headers: {
              Authorization: getAuthorizationToken()
            },
            params: {
              'feature' : feature
            }
        }
    )
    .then(res => res.data)
    .then(data => callback(true,data))
    .catch(err => callback(false,err))
}