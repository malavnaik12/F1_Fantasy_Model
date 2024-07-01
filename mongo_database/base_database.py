import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

def get_col_Constructors():
    return mydb.constructors

def get_col_Constructors_cache():
    return mydb.constructors_cache

def get_col_Drivers():
    return mydb.drivers

def get_col_Drivers_cache():
    return mydb.drivers_cache
