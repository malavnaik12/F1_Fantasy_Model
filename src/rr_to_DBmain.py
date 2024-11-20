import json
from weekend_parse import gp_parse, get_gp_info, gp_type_parse
from team_parse import full_team_info,getDrivers

# self.num_gp = gp_parse(get_gp_info())
# self.gp_type = gp_type_parse(get_gp_info())
# self.sprint_gp_count = self.gp_type.count('Sprint')
# self.normal_gp_count = self.gp_type.count('Normal')

class rr_to_DBmain:
    def __init__(self):
        with open('./database_files/race_results.json',"r+") as rr_f:
            self.rr = json.load(rr_f)
        with open('./database_files/database_main.json',"r+") as db_main_f:
            self.db_main = json.load(db_main_f)
        self.gp_locs = gp_parse(get_gp_info())

    def populate_positions(self,race_info,attr,attr_items,constructor_flag):
        for team in self.dbmain_year:
            if constructor_flag:
                self.dbmain_year[team][attr][race_info] = attr_items[team]
            else:
                drivers = getDrivers(team)
                for driver in drivers:
                    self.dbmain_year[team][driver][attr][race_info] = attr_items.index(driver)+1
    
    def populate_prices(self,race_info,attr,attr_items,constructor_flag):
        for team in self.dbmain_year:
            if constructor_flag:
                self.dbmain_year[team][attr][race_info] = attr_items[team]
            else:
                drivers = getDrivers(team)
                for driver in drivers:
                    try:
                        self.dbmain_year[team][driver][attr][race_info] = attr_items[driver]
                    except KeyError:
                        pass

    def main(self,item):
        year = item['year']
        self.dbmain_year = self.db_main[str(year)]
        for race_loc in self.gp_locs:
            get_race_num = self.gp_locs.index(race_loc)
            race_data = self.rr[str(year)][race_loc]
            for race_attr in list(race_data.keys()):
                if race_attr == "race_weekend_type":
                    continue
                elif race_attr == "Constructor":
                    for constructor_attr in list(race_data[race_attr].keys()):
                        if constructor_attr == "prices":
                            self.populate_prices(race_loc,constructor_attr,race_data[race_attr][constructor_attr],True)
                        else:
                            self.populate_positions(get_race_num,constructor_attr,race_data[race_attr][constructor_attr],True)
                elif race_attr == "prices":
                    self.populate_prices(race_loc,race_attr,race_data[race_attr],False)
                else:
                    try:
                        assert len(race_data[race_attr])>0
                        self.populate_positions(get_race_num,race_attr,race_data[race_attr],False)
                    except:
                        continue
        self.db_main[str(year)] = self.dbmain_year
        with open('./database_files/database_main.json',"w+") as db_file:
            json.dump(self.db_main, db_file, indent=2)

if __name__ == "__main__":
    init = rr_to_DBmain()
    init.main({'year':2024})