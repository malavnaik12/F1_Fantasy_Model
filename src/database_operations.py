import json
import fastf1_connect
from team_parse import getTeams
from database_init import InitializeFiles
from weekend_parse import get_gp_info, gp_parse


class InsertData:
    def __init__(self, year=None):
        self.manual_sessions = ["Free Practice 1", "Free Practice 2", "Free Practice 3"]
        if year != None:
            try:
                self.db_filename = "./database_files/race_results.json"
                with open(self.db_filename, "r") as db_file:
                    self.data = json.load(db_file)
                # print(str(year), list(self.data.keys()))
                assert str(year) in list(self.data.keys())
            except (FileNotFoundError, AssertionError) as e:
                InitializeFiles(int(year))

    def _get_teams_info(self):
        with open("./input_files/list_teams.txt", "r+") as teams_file:
            teams_list = teams_file.readlines()
        self.teams = {}
        prev_team = ""
        for item in teams_list:
            if prev_team != item.split(",")[0]:
                self.teams[item.split(",")[0]] = {}
                self.teams[item.split(",")[0]]["avg_pos"] = int()
                prev_team = item.split(",")[0]
            self.teams[item.split(",")[0]][item.split(",")[1]] = int()

    def save_to_db(self):
        with open(self.db_filename, "w") as outfile:
            json.dump(self.data, outfile, indent=2)

    def init_race_weekend(self, race_loc):
        for key in list(self.data[race_loc].keys()):
            if type(self.data[race_loc][key]) == list:
                if len(self.data[race_loc][key]) == 0:
                    self.data[race_loc][key] = [""] * 20

    def get_session(self, item_dict):
        # Need logic in below if for substitute driver
        if item_dict["session"] in self.manual_sessions and item_dict["data_override"]:
            session_info = self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                item_dict["session"]
            ]
            if len(session_info) == 0:
                session_info = [""] * 20
            session_info[int(item_dict["driver1_pos"]) - 1] = item_dict["driver1"]
            session_info[int(item_dict["driver2_pos"]) - 1] = item_dict["driver2"]
        else:
            gp_info_locs = gp_parse(get_gp_info())
            year = item_dict["year"]
            race_indx = gp_info_locs.index(item_dict["raceLoc"]) + 1
            session = "".join([item[0] for item in item_dict["session"].split(" ")])
            if session == "SR":
                session = "S"
            session_info = fastf1_connect.call_from_dp_ops(year, race_indx, session)
        try:
            assert item_dict["year"] in list(self.data.keys())
        except AssertionError:
            self.data[f"{item_dict['year']}"] = {}
        self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
            item_dict["session"]
        ] = session_info
        self.save_to_db()
        return self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
            item_dict["session"]
        ]

    def sort_dict(self, unsorted_dict: dict):
        return {
            k: v for k, v in sorted(unsorted_dict.items(), key=lambda item: item[1])
        }

    def get_session_constructors(self, item_dict, drivers_results):
        self._get_teams_info()
        constructor_pos = {}
        for team in list(self.teams.keys()):
            for key in list(self.teams[team].keys()):
                if key in drivers_results:
                    self.teams[team][key] = drivers_results.index(key) + 1
                    self.teams[team]["avg_pos"] += 0.5 * self.teams[team][key]
            constructor_pos[team] = self.teams[team]["avg_pos"]
        self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["Constructor"][
            item_dict["session"]
        ] = self.sort_dict(constructor_pos)
        self.save_to_db()
        return self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["Constructor"][
            item_dict["session"]
        ]

    def post_race_positions(self, item_dict):
        d1 = "driver1"
        d2 = "driver2"
        self._post_driver(item_dict=item_dict, driver=d1)
        self._post_driver(item_dict=item_dict, driver=d2)
        with open(self.db_filename, "w") as db_file:
            json.dump(self.data, db_file, indent=2)

    def _post_driver(self, item_dict, driver):
        try:
            get_existing_indx = self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                item_dict["session"]
            ].index(item_dict[f"{driver}"])
            self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                item_dict["session"]
            ][get_existing_indx] = ""
        except ValueError:
            self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                item_dict["session"]
            ][item_dict[f"{driver}_pos"] - 1] = item_dict[f"{driver}"]
        else:
            self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                item_dict["session"]
            ][item_dict[f"{driver}_pos"] - 1] = item_dict[f"{driver}"]

    def post_driver_prices(self, item_dict):
        if len(self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["prices"]) == 0:
            prices_dict = {}
            for driver, price in zip(item_dict["drivers"], item_dict["driver_prices"]):
                prices_dict[f"{driver}"] = price
            self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                "prices"
            ] = prices_dict
            self.save_to_db()
        return self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["prices"]

    def get_driver_prices(self, item_dict):
        return self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["prices"]

    def post_constructor_prices(self, item_dict):
        _temp = {}
        for team, price in zip(
            item_dict["constructors"], item_dict["constructor_prices"]
        ):
            _temp[team] = price
        self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["Constructor"][
            "prices"
        ] = self.sort_dict(_temp)
        self.save_to_db()
        return self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["Constructor"][
            "prices"
        ]

    def get_constructor_prices(self, item_dict):
        teams = getTeams()
        try:
            assert (
                len(
                    self.data[f"{item_dict['year']}"][item_dict["raceLoc"]][
                        "Constructor"
                    ]["prices"]
                )
                > 0
            )
        except KeyError:
            self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["Constructor"][
                "prices"
            ] = {key: 0 for key in teams}
        self.save_to_db()
        return self.data[f"{item_dict['year']}"][item_dict["raceLoc"]]["Constructor"][
            "prices"
        ]


if __name__ == "__main__":
    initClass = InsertData()
    # initClass.init_race_weekend('Bahrain')
