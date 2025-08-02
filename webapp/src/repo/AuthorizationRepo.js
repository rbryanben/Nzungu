import { ENDPOINTS } from "@/main"
import axios from "axios"

// Routes
const ROUTE_AUTHENTICATE = '/api/v1/authenticate'

export function getAuthorizationToken() {
  const token = localStorage.getItem('authorization');

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