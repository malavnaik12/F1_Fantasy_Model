import yaml
import json
import team_parse
import weekend_parse

class InitializeFiles:
    def __init__(self) -> None:
        InitializeRaceResults()
        InitializeMain()

class WeekendInfo(weekend_parse.WeekendParser):
    def __init__(self):
        super().__init__()

class InitializeRaceResults:
    def __init__(self) -> None:
        self.init_WI = WeekendInfo()
        self.db_filename = "./database_files/race_results.json"
        try:
            # os.path.isfile("./database_files/database.json")
            with open(self.db_filename,"r") as db_file:
                self.data = json.load(db_file)
        except FileNotFoundError:
            data = {}
            for gp in self.init_WI.gp_parse():
                data[gp] = {}
            self.init_db(data)

    def _create_weekend_schema(self,_schema, weekend_type):
        if weekend_type == 'Normal':
            for key in list(_schema.keys()):
                if 'Sprint' in key.split(' '):
                    _schema.pop(key)
        elif weekend_type == 'Sprint':
            _schema.pop('Free Practice 2')
            _schema.pop('Free Practice 3')
        for key in list(_schema.keys()):
            if key == 'race_weekend_type':
                _schema[key] = weekend_type
        return _schema

    def init_db(self,info_dict):
        with open("./input_files/prices_schema.yaml", "r") as price_schema_file:
            price_schema = yaml.safe_load(price_schema_file)
        for (indx, gp) in enumerate(list(info_dict.keys())):
            with open("./input_files/positions_schema.yaml", "r") as pos_schema_file:
                pos_schema = yaml.safe_load(pos_schema_file)
                pos_schema.update(price_schema)
            info_dict[gp] = self._create_weekend_schema(pos_schema,self.init_WI.gp_type[indx])
        with open(self.db_filename,"w") as outfile:
            json.dump(info_dict,outfile,indent=2)

class InitializeMain:
    def __init__(self) -> None:
        self.init_WI = WeekendInfo()
        self.db_filename = "./database_files/database_main.json"
        try:
            # os.path.isfile("./database_files/database.json")
            with open(self.db_filename,"r") as db_file:
                self.data = json.load(db_file)
        except FileNotFoundError:
            self.init_db()
    def init_db(self):
        with open("./input_files/data_structure.yaml", "r") as file:
            inputs = yaml.safe_load(file)
        with open("./input_files/positions_schema.yaml", "r") as pos_schema_file:
            pos_schema = yaml.safe_load(pos_schema_file)
            pos_schema.pop('race_weekend_type')
        with open("./input_files/prices_schema.yaml", "r") as price_schema_file:
            price_schema = yaml.safe_load(price_schema_file)
            pos_schema.update(price_schema)
        data_attrs = pos_schema
        team_info = inputs["team_data"]
        teams = {key: {} for key in list(team_info.keys())}
        for team in list(teams.keys()):
            for attribute in list(data_attrs.keys()):
                if attribute == 'prices':
                    teams[team][attribute] = []
                else:
                    teams[team][attribute] = data_attrs[attribute]
            for driver in list(team_info[team].keys()):
                teams[team][driver] = data_attrs
        with open(self.db_filename,"w") as db_file:
            json.dump(teams, db_file, indent=2)

if __name__ == '__main__':
    InitializeFiles()
    # print("This file is not directly callable. It is called to create database.json within database.py.")