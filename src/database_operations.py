import json
from database_init import InitializeFiles
import fastf1_connect
import weekend_parse
import asyncio

class InsertData:
    def __init__(self):
        try:
            self.db_filename = "./database_files/race_results.json"
            with open(self.db_filename,"r") as db_file:
                self.data = json.load(db_file)
        except FileNotFoundError:
            InitializeFiles(2024) # Need to make it so that this input is being supplied by front end

    def save_to_db(self):
        with open(self.db_filename,"w") as outfile:
            json.dump(self.data,outfile,indent=2)

    def init_race_weekend(self,race_loc):
        for key in list(self.data[race_loc].keys()):
            if type(self.data[race_loc][key]) == list:
                if len(self.data[race_loc][key]) == 0:
                    self.data[race_loc][key] = ['']*20

    def get_session(self,item_dict):
        gp_info_locs = weekend_parse.gp_parse()
        if len(self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]]) == 0:
            year = item_dict[f'year']
            race_indx = gp_info_locs.index(item_dict['raceLoc'])+1
            session = ''.join([item[0] for item in item_dict['session'].split(' ')])
            if session == 'SR':
                session = 'S'
            session_info = asyncio.run(fastf1_connect.call_from_dp_ops(year,race_indx,session))
            self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]] = session_info
            self.save_to_db()
        return self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]]

    def post_race(self,item_dict):
        d1 = "driver1"
        d2 = "driver2"
        self._post_driver(item_dict=item_dict,driver=d1)
        self._post_driver(item_dict=item_dict,driver=d2)
        print(self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']])
        with open(self.db_filename,"w") as db_file:
            json.dump(self.data, db_file, indent=2)
    
    def _post_driver(self,item_dict,driver):
        try:
            get_existing_indx = self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]].index(item_dict[f"{driver}"])
            self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]][get_existing_indx] = ''
        except ValueError:
            self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]][item_dict[f"{driver}_pos"]-1] = item_dict[f"{driver}"]
        else:
            self.data[f"{item_dict[f'year']}"][item_dict['raceLoc']][item_dict["session"]][item_dict[f"{driver}_pos"]-1] = item_dict[f"{driver}"]
            
if __name__ == "__main__":
    initClass = InsertData()
    initClass.init_race_weekend('Bahrain')