import unittest
from mongo_database.collections.constructors_collection import get_col_Constructors
from mongo_database.crud import constructors_crud

class testRoutes(unittest.TestCase):
    def testResults(self):
        check = constructors_crud.read_item(name="redbull",race="bahrain",main_collection=get_col_Constructors())
        self.assertTrue(check==None)

if __name__ == "__main__":
    unittest.main()