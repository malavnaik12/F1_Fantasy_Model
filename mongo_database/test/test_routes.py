import unittest
from mongo_database.base_database import get_col_Constructors
from mongo_database.crud import base_crud

class testRoutes(unittest.TestCase):
    def testResults(self):
        check = base_crud.read_item(name="redbull",race="bahrain",main_collection=get_col_Constructors())
        self.assertTrue(check==None)

if __name__ == "__main__":
    unittest.main()