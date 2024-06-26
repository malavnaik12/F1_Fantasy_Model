import yaml
import json

def main():
    """
    The main function of create_database.py is simply used to create database.json with the desired structure.
    This file is not directly executable.
    
    Args:
        None
    
    Returns:
        None
    """
    with open("./input_files/data_structure.yaml", "r") as file:
        inputs = yaml.safe_load(file)
        data_attrs = inputs["attributes"]
        team_info = inputs["team_data"]
        teams = {key: {} for key in list(team_info.keys())}
        for team in list(teams.keys()):
            for attribute in list(data_attrs.keys()):
                teams[team][attribute] = []
            for driver in list(team_info[team].keys()):
                # data_attrs['availability'] = []
                teams[team][driver] = data_attrs
    
    with open("./database_files/database.json","w") as db_file:
        json.dump(teams, db_file, indent=2)

if __name__ == '__main__':
    print("This file is not directly callable. It is called to create database.json within database.py.")