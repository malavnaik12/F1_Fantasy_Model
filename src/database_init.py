import yaml
import json
# import team_parse
from weekend_parse import gp_parse, gp_type_parse, get_gp_info
import os

class InitializeFiles:
    def __init__(self, year: int) -> None:
        os.makedirs("./database_files",exist_ok=True)
        # InitializeRaceResults()
        InitializeMain()

class InitializeRaceResults:
    def __init__(self) -> None:
        self.db_filename = "./database_files/race_results.json"
        self.main_data_dict = {}
        try:
            # os.path.isfile("./database_files/database.json")
            with open(self.db_filename,"r") as db_file:
                self.data = json.load(db_file)
            for race in list(self.data['2024'].keys()):
                self.data['2024'][race]['Constructor'] = {}
            with open(self.db_filename,"w") as outfile:
                json.dump(self.data,outfile,indent=2)
        except FileNotFoundError:
            data = {}
            for gp in gp_parse(get_gp_info()):
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
        gp_type = gp_type_parse(get_gp_info())
        with open("./input_files/prices_schema.yaml", "r") as price_schema_file:
            price_schema = yaml.safe_load(price_schema_file)
        for (indx, gp) in enumerate(list(info_dict.keys())):
            with open("./input_files/positions_schema.yaml", "r") as pos_schema_file:
                pos_schema = yaml.safe_load(pos_schema_file)
                pos_schema.update(price_schema)
            info_dict[gp] = self._create_weekend_schema(pos_schema,gp_type[indx])
        self.main_data_dict["2024"] = info_dict
        with open(self.db_filename,"w") as outfile:
            json.dump(self.main_data_dict,outfile,indent=2)

class InitializeMain:
    def __init__(self) -> None:
        self.db_filename = "./database_files/database_main.json"
        self.main_data_dict = {}
        self.num_gp = gp_parse(get_gp_info())
        # self.gp_type = gp_type_parse(get_gp_info())
        # self.sprint_gp_count = self.gp_type.count('Sprint')
        # self.normal_gp_count = self.gp_type.count('Normal')
        try:
            # os.path.isfile("./database_files/database.json")
            with open(self.db_filename,"r") as db_file:
                self.data = json.load(db_file)
        except FileNotFoundError:
            self.init_db()

    def develop_attr(self,attrs,curr_attr):
        attr = attrs[curr_attr]
        if attr == []:
            # if curr_attr in ['Free Practice 2','Free Practice 3']:
            #     init_attr = [None]*self.normal_gp_count
            # elif curr_attr in ['Sprint Qualifying','Sprint Race']:
            #     init_attr = [None]*self.sprint_gp_count
            # else:
            init_attr = [None]*len(self.num_gp)
        else:
            init_attr = attr
        return init_attr
    
    def init_db(self):
        with open("./input_files/data_structure.yaml", "r") as file:
            team_info = yaml.safe_load(file)
        with open("./input_files/positions_schema.yaml", "r") as pos_schema_file:
            pos_schema = yaml.safe_load(pos_schema_file)
            pos_schema.pop('race_weekend_type')
        with open("./input_files/prices_schema.yaml", "r") as price_schema_file:
            price_schema = yaml.safe_load(price_schema_file)
            pos_schema.update(price_schema)
        data_attrs = pos_schema
        teams = {key: {} for key in list(team_info.keys())}
        for team in list(teams.keys()):
            for attribute in list(data_attrs.keys()):
                if attribute == 'Constructor':
                        continue
                else:
                    teams[team][attribute] = self.develop_attr(data_attrs,attribute)
            for driver in list(team_info[team].keys()):
                teams[team][driver] = team_info[team][driver]
                for attribute in list(data_attrs.keys()):
                    if attribute == 'Constructor':
                        continue
                    else:
                        teams[team][driver][attribute] = self.develop_attr(data_attrs,attribute)
        self.main_data_dict[f"2024"] = teams
        with open(self.db_filename,"w") as db_file:
            json.dump(self.main_data_dict, db_file, indent=2)

if __name__ == '__main__':
    InitializeFiles(2024) 
    # print("This file is not directly callable. It is called to create database.json within database.py.")