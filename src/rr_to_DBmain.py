import sys
import json
from team_parse import getDrivers
from weekend_parse import gp_parse, get_gp_info, gp_type_parse


class rr_to_DBmain:
    def __init__(self):
        self.gp_locs = gp_parse(get_gp_info())
        # with open("./database_files/race_results.json", "r+") as rr_f:
        #     self.rr = json.load(rr_f)
        # with open("./database_files/database_main.json", "r+") as db_main_f:
        #     self.db_main = json.load(db_main_f)

    def _load_json(self, fpath=""):
        with open(fpath, "r+") as db_main_f:
            return json.load(db_main_f)

    def populate_positions(self, race_info, attr, attr_items, constructor_flag):
        for team in self.dbmain_year:
            if constructor_flag:
                # try:
                #     print(len(self.dbmain_year[team][attr]) + 1, race_info)
                #     input()
                #     assert len(self.dbmain_year[team][attr]) + 1 == race_info
                #     # self.dbmain_year[team][attr][race_info] = attr_items[team]
                # except AssertionError:
                #     self.dbmain_year[team][attr].append(None)
                self.dbmain_year[team][attr][race_info] = attr_items[team]
                # input()
            else:
                drivers = getDrivers(team)
                # print(race_info, team, drivers)
                # input()
                for driver in drivers:
                    # if driver == "Piastri":
                    #     print("Before: ", self.dbmain_year[team][driver][attr])
                    self.dbmain_year[team][driver][attr][race_info] = (
                        attr_items.index(driver) + 1
                    )
                    # if driver == "Piastri":
                    #     print("After: ", self.dbmain_year[team][driver][attr])

    def populate_prices(self, race_info, attr, attr_items, constructor_flag):
        for team in self.dbmain_year:
            if constructor_flag:
                self.dbmain_year[team][attr][race_info] = attr_items[team]
            else:
                drivers = getDrivers(team)
                for driver in drivers:
                    try:
                        self.dbmain_year[team][driver][attr][race_info] = attr_items[
                            driver
                        ]
                    except KeyError:
                        pass

    def main(self, item):
        year = item["year"]
        rr = self._load_json(fpath="./database_files/race_results.json")
        try:
            db_main = self._load_json(fpath="./database_files/database_main.json")
        except FileNotFoundError:
            db_main = {}
        # print("in rr_to_DBmain:", list(db_main.keys()))
        # input()
        self.dbmain_year = db_main[str(year)]
        # self.dbmain_year = {}
        for race_loc in self.gp_locs:
            get_race_num = self.gp_locs.index(race_loc)
            race_data = rr[str(year)][race_loc]
            for race_attr in list(race_data.keys()):
                if race_attr == "race_weekend_type":
                    continue
                elif race_attr == "Constructor":
                    for constructor_attr in list(race_data[race_attr].keys()):
                        if constructor_attr == "prices":
                            self.populate_prices(
                                race_loc,
                                constructor_attr,
                                race_data[race_attr][constructor_attr],
                                True,
                            )
                        else:
                            self.populate_positions(
                                get_race_num,
                                constructor_attr,
                                race_data[race_attr][constructor_attr],
                                True,
                            )
                elif race_attr == "prices":
                    self.populate_prices(
                        race_loc, race_attr, race_data[race_attr], False
                    )
                else:
                    try:  # Need  better way to handle this try-except, it's causing issues with populating database_main.json
                        # print(get_race_num, race_data[race_attr])
                        assert len(race_data[race_attr]) > 0
                        self.populate_positions(
                            get_race_num, race_attr, race_data[race_attr], False
                        )
                    except:
                        continue
            # print(self.dbmain_year)
            # input("Above line is producing empty dictionaries")
        db_main[str(year)] = self.dbmain_year
        with open("./database_files/database_main.json", "w+") as db_file:
            json.dump(db_main, db_file, indent=2)


if __name__ == "__main__":
    init = rr_to_DBmain()
    init.main({"year": 2024})
