import { promises as fs } from 'fs';

// Utility function to log messages with a timestam
async function logMessage(message,showConsole=true) {
    // Log to file 
    const now = new Date();
    const timestamp = now.toISOString()
    const logEntry = `${timestamp} ${message}\n`;
    await fs.appendFile('./logs/application.log', logEntry);

    // Show to console
    if (showConsole){
        console.log(`${timestamp} ${message}`)
    }   
}

export default logMessage


