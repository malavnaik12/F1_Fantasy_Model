import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

def get_col_Constructors():
    return mydb.constructors

def get_col_Drivers():
    return mydb.drivers
