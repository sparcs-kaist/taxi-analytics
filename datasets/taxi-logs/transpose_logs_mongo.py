from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
import os
import re

def getDB():
    load_dotenv()
    MONGODB_URI = os.getenv('MONGODB_URI')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME')
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB_NAME]
    return db

def getLogFileNames():
    fileList = os.listdir("logs")
    fileList = list(filter(lambda x: x.endswith("-combined.log"), fileList))
    return fileList

def getLogsFromFileName(fileName):
    f = open("logs/" + fileName, "r")
    logs = f.readlines()
    return logs

def logParser(logLine):
    logPattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[([^\]]+)\]: ([^(\s]+)\(([^)]+)\) "([^"]+)" (\d+) on ([\d\.]+)ms'
    timePattern = '%Y-%m-%d %H:%M:%S'
    match = re.search(logPattern, logLine)
    if match:
        timestamp, logLevel, username, ipAddress, request, statusCode, responseTime = match.groups()
        timestamp = datetime.strptime(timestamp, timePattern)
        return {
            "timestamp": timestamp,
            "logLevel": logLevel,
            "username": username,
            "ipAddress": ipAddress,
            "request": request,
            "statusCode": statusCode,
            "responseTime": responseTime,
        }
    return None

if __name__ == "__main__":
    db = getDB()
    for fileName in tqdm(getLogFileNames()):
        for log in getLogsFromFileName(fileName):
            parsedLog = logParser(log)
            if parsedLog:
                db.logs.update_one(parsedLog, {"$set": parsedLog}, upsert=True)
