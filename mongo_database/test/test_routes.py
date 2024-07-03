import unittest
# from routes.base_routes import 
from base_database import get_col_Constructors, get_col_Constructors_cache
from crud import base_crud

class testRoutes(unittest.TestCase):
    def testResults(self):
# check = base_routes.read_item(name="redbull",race="bahrain",collection=get_col_Constructors())
# check_2 = base_routes.read_item(name="ferrari",race="bahrain",collection=get_col_Constructors())

        check = base_crud.read_item(name="redbull",race="bahrain",main_collection=get_col_Constructors())
        self.assertTrue(check==None)
        # check_2 = base_crud.read_item(name="ferrari",race="bahrain",main_collection=get_col_Constructors())
        # print("from main collection:",check)
        # print("from main collection:",check_2)

if __name__ == "__main__":
    unittest.main()