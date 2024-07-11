import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["F1_Fantasy_Model"]

def get_col_Constructors():
    return mydb.constructors

def get_col_Constructors_cache():
    return mydb.constructors_cache