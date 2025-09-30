import { ENDPOINTS } from "@/main";
import axios from "axios";
import { getAuthorizationToken } from "./AuthorizationRepo";

// Routes 
const ROUTE_GET_FEATURE_FLAGS = '/api/v1/get-feature-flags'

// Attributes 
let flags; 
let flagsPromise; 


// Request to get feature flags 
const pr_getFeatureFlags = async () => {
    // Get the flags
    const res = await axios.get(`${ENDPOINTS.BASE_URL}${ROUTE_GET_FEATURE_FLAGS}`, {
        headers: {
            Authorization: getAuthorizationToken()
        }
    });

    return res.data;
};

// Method to check if a feature is enabled 
export async function checkFlag(flag){
    try{
        await ensureFeatureFlagsLoaded()
        return flag in flags.flags
    }
    catch(err){
        return false
    }
}


// Ensure feature flags loaded 
export async function ensureFeatureFlagsLoaded(){
    try {
        // If flags is already defined then resolve
        if (flags){
            return
        }

        // If there is no promise create on 
        if (!flagsPromise){
            flagsPromise = pr_getFeatureFlags()
        }

        // Fetch flags and set
        flags = await flagsPromise
    }
    catch (err){
        // Failed to fetch flags 
        console.log(err)
        throw err
    }
}

