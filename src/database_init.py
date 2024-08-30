import yaml
import json
import team_parse
import weekend_parse

class WeekendInfo(weekend_parse.WeekendParser):
    def __init__(self):
        super().__init__()
        # self.gp_parse()

def main():
    """
    The main function of create_database.py is simply used to create database.json with the desired structure.
    This file is not directly executable.
    
    Args:
        None
    
    Returns:
        None
    """
    init_WI = WeekendInfo()
    with open("./input_files/positions_schema.yaml", "r") as pos_schema_file:
        pos_schema = yaml.safe_load(pos_schema_file)
    print(pos_schema)
    print(init_WI.gp_type)
    print(init_WI.gp_parse())
    print(init_WI.sessions_parse('Bahrain'))
    print(team_parse.getTeams())
    print(team_parse.getDrivers('Redbull'))
    # with open("./input_files/list_teams.txt","r+") as team_info_file:
    #     team_items = [entry.split('\n')[0] for entry in team_info_file.readlines()]
    # print(inputs)
    #     data_attrs = inputs["attributes"]
    #     team_info = inputs["team_data"]
    #     teams = {key: {} for key in list(team_info.keys())}
    #     for team in list(teams.keys()):
    #         for attribute in list(data_attrs.keys()):
    #             teams[team][attribute] = []
    #         for driver in list(team_info[team].keys()):
    #             # data_attrs['availability'] = []
    #             teams[team][driver] = data_attrs
    
    # with open("./database_files/database.json","w") as db_file:
    #     json.dump(teams, db_file, indent=2)

if __name__ == '__main__':
    main()
    # print("This file is not directly callable. It is called to create database.json within database.py.")