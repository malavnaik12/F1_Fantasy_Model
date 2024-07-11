import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["F1_Fantasy_Model"]

def get_col_Drivers():
    return mydb.drivers

def get_col_Drivers_cache():
    return mydb.drivers_cache
