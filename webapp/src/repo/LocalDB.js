import { notify_failed } from "@/utils/notifications";

let db; 

// On database error 
const onOpenDbError = (event) =>{
    notify_failed(`Failed to open local database - ${event.target.error}`)
}

// On open database success 
const onOpenDbSuccess = (event) => {
    db = event.target.result
}

// Create sales table 
const createSalesTable = (db) => {    
    let store;

    // Create the table
    if (!db.objectStoreNames.contains('offline_sales')){
        store =  db.createObjectStore("offline_sales",{ keyPath: "id", autoIncrement: true})
    }

    // Create the commited index 
    if (!store.indexNames.contains('commitedIndex')){
        store.createIndex('commitedIndex','commited',{unique: false})
    }
}

// Create sales table 
const createConfigTable = (db) => {    
    let store;

    // Create the table
    if (!db.objectStoreNames.contains('config')){
        store =  db.createObjectStore("config",{ keyPath: "id", autoIncrement: true})
    }

    // Create the commited index 
    if (!store.indexNames.contains('keyIndex')){
        store.createIndex('keyIndex','key',{unique: true})
    }
}

// Create products table
const createProductsTable = (db) => {
    let store;

    // Create the table
    if (!db.objectStoreNames.contains('products')){
        store =  db.createObjectStore("products",{ keyPath: "id", autoIncrement: true})
    }

    // Create the reference index 
    if (!store.indexNames.contains('refIndex')){
        store.createIndex('refIndex','ref',{unique: true})
    }
}

// Create products table
const createCategoriesTable = (db) => {
    let store;

    // Create the table
    if (!db.objectStoreNames.contains('categories')){
        store =  db.createObjectStore("categories",{ keyPath: "id", autoIncrement: true})
    }
}


// On upgrade required 
const onUpgradeRequired = (e)=> {
    // Database
    db = e.target.result

    // Created tables 
    createSalesTable(db)
    createProductsTable(db)
    createConfigTable(db)
    createCategoriesTable(db)
}

// Add method
export function addRecord(table,value,callback=()=>{}){

    // Check if the db is defined 
    if (db == NaN || db == undefined){
        callback(false,'Local database is not open')
    }

    // Transaction 
    const tx = db.transaction(table,'readwrite')
    const store = tx.objectStore(table)
    let request = store.add(value)

    // On error
    request.onerror = (error)=> {
        callback(false,error)
    }

    // On success 
    request.onsuccess = (event)=>{
        callback(true,event.target.result)
    }

}

export function p_addRecord(table,value){
    return new Promise((resolve,reject)=>{
        // Check if the db is defined 
        if (!db){
            reject('DB is not open')
        }

        // Transaction 
        const tx = db.transaction(table,'readwrite')
        const store = tx.objectStore(table)
        let request = store.add(value)

        // On error
        request.onerror = (e) => reject(e)

        // On success 
        request.onsuccess = (e) => resolve(e)
    })
}

// Function to query a table 
export function queryTable(table,indexName,range,handler){
    // Check if the db is defined 
    if (!db){
        return handler(false,'Local database is not open')
    }

    const tx = db.transaction(table,"readwrite")
    const store = tx.objectStore(table)
    const index = store.index(indexName)

    index.openCursor(range).onsuccess = (event)=>{
        const cursor = event.target.result
        if (cursor){
            handler(true,cursor.value)
            cursor.continue()
        }
        else{
            handler(false,null)
        }
    }
}

// Function to query a table 
export function p_queryTable(table,indexName,range){
    return new Promise((resolve,reject)=>{
        // Check if the db is defined 
        if (!db){
            return reject('Database is closed')
        }

        const tx = db.transaction(table,"readonly")
        const store = tx.objectStore(table)
        const index = store.index(indexName)

        let records = [] 

        let request = index.openCursor(range)
        
        request.onsuccess = (event)=>{
            const cursor = event.target.result
            if (cursor){
                records.push(cursor.value)
                cursor.continue()
            }
            else{
                return resolve(records)
            }
        }

        request.onerror = e => reject(e)
        
    })
}



// Get all from table 
export function getAllFromTable(table,callback){
    const tx = db.transaction(table,"readwrite")
    const store = tx.objectStore(table)
    const request = store.getAll()

    request.onerror = (error)=>{
        callback(false,error)
    }

    request.onsuccess = (event)=> {
        callback(true,event.target.result)
    }
}

export function p_getAllFromTable(table){
    return new Promise((resolve,reject)=>{
        const tx = db.transaction(table,"readwrite")
        const store = tx.objectStore(table)
        const request = store.getAll()

        request.onerror = (error)=> reject(error)

        request.onsuccess = (event)=> resolve(event.target.result)
    })
}


// Function to delete item from db 
export function deleteFromTable(table,key,callback){
    const tx = db.transaction(table,'readwrite')
    const store = tx.objectStore(table)

    const request = store.delete(key)

    request.onerror = (error)=> {
        callback(false,error)
    }
    request.onsuccess = ()=>{
        callback(true,null)
    }
}

// bulk add
export function bulkAddRecord(table,values,callback){
    // Check if the db is defined 
    if (!db){
        return callback(false,'Local database is not open')
    }

    // Transaction 
    const tx = db.transaction(table,'readwrite')
    const store = tx.objectStore(table)
    let callbackCalled = false

    tx.oncomplete = ()=> {
        if (!callbackCalled){
            callbackCalled = true
            callback(true,null)
        }
    }

    tx.onabort = ()=>{
        if (!callbackCalled){
            callbackCalled = true
            callback(false,'Transaction failed to complete')
        }
    }

    tx.onerror = (e) => {
        if (!callbackCalled){
            callbackCalled = true
            callback(false, e.target.error);
        }
    };


    // Iterate the batch
    try{
        values.forEach(record => {
            // Request
            const request = store.add(record)
            request.onerror = (error)=> {
                tx.abort()
            }
        });
    }
    catch(error){
        tx.abort()
    }
}

export function p_updateTable(table,indexName,key,value){
    return new Promise((resolve,reject) => {
        const tx = db.transaction(table,"readwrite")
        const store = tx.objectStore(table)
        const index = store.index(indexName)

        // Fetch the object first 
        let request = index.get(key)

        // If could not fetch then reject 
        request.onerror = (error)=>{
            reject(error)
        }

        // On fetch success then update the record
        request.onsuccess = (event)=>{
            // Record 
            let record = event.target.result
            
             // event is null then return success 
            if (!record){
                return resolve(null)
            }

            // Update the record 
            record = {
                id : record.id,
                ...value
            }

            // Update request
            let updateRequest = store.put(record)

            updateRequest.onsuccess = (e) => {resolve(e.target.result)}
            updateRequest.onerror = (e) => {reject(e)}
        }
    })
}

// Method that opens a db
export function openDB(name="nzungu",version=1,onsuccess=onOpenDbSuccess,onerror=onOpenDbError){
    // Open db request
    const request = indexedDB.open(name,1)

    // Error 
    request.onerror = onerror
    // Success
    request.onsuccess = onsuccess
    // Upgrade required
    request.onupgradeneeded = onUpgradeRequired
}

export function ensureOpenDB(name="nzungu",version=1){
    return new Promise((resolve,reject)=>{
        // If db is already open
        if (db){
            resolve(db)
            return
        }

        // Open db request
        const request = indexedDB.open(name,1)

        // Error 
        request.onerror = error => reject(error)
        
        // Success
        request.onsuccess = event => {
            db = event.target.result
            resolve(event.target.result)
        }

        // Upgrade required
        request.onupgradeneeded = onUpgradeRequired
    })
}