from team_parse import getTeams,getDrivers
import yaml

team_data = {key: {} for key in getTeams()}
for team in team_data.keys():
    drivers = getDrivers(team)
    for driver in drivers:
        team_data[team][driver] = {}

with open('./input_files/data_structure.yaml', 'w+') as outfile:
    yaml.dump(team_data, outfile, default_flow_style=False)