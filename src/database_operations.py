import json
from database_init import InitializeFiles
class InsertData:
    def __init__(self):
        try:
            self.db_filename = "./database_files/race_results.json"
            with open(self.db_filename,"r") as db_file:
                self.data = json.load(db_file)
        except FileNotFoundError:
            InitializeFiles()


    def init_race_weekend(self,race_loc):
        for key in list(self.data[race_loc].keys()):
            if type(self.data[race_loc][key]) == list:
                if len(self.data[race_loc][key]) == 0:
                    self.data[race_loc][key] = ['']*20

    def post_race(self,item_dict):
        d1 = "driver1"
        d2 = "driver2"
        # print(item_dict)
        self._post_driver(item_dict=item_dict,driver=d1)
        self._post_driver(item_dict=item_dict,driver=d2)
        print(self.data[item_dict['raceLoc']])
        with open(self.db_filename,"w") as db_file:
            json.dump(self.data, db_file, indent=2)
    
    def _post_driver(self,item_dict,driver):
        try:
            get_existing_indx = self.data[item_dict['raceLoc']][item_dict["session"]].index(item_dict[f"{driver}"])
            self.data[item_dict['raceLoc']][item_dict["session"]].pop(get_existing_indx)
        except ValueError:
            self.data[item_dict['raceLoc']][item_dict["session"]][item_dict[f"{driver}_pos"]-1] = item_dict[f"{driver}"]
        else:
            self.data[item_dict['raceLoc']][item_dict["session"]][item_dict[f"{driver}_pos"]-1] = item_dict[f"{driver}"]
            
if __name__ == "__main__":
    initClass = InsertData()
    initClass.init_race_weekend('Bahrain')