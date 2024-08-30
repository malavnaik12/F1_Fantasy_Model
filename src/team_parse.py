def _mainListParse():
    with open("./input_files/list_teams.txt","r+") as team_info:
        data = [line.split('\n')[0].split(',') for line in team_info.readlines()]
    info_dict = {}
    for item in data:
        try:
            info_dict[item[0]].append({'driver_name':item[1],'driver_num':item[2]})
        except KeyError:
            info_dict[item[0]] = [{'driver_name':item[1],'driver_num':item[2]}]
    return info_dict

def getTeams():
    return list(_mainListParse().keys())

def getDrivers(team: str):
    return [driver_info['driver_name'] for driver_info in _mainListParse()[team]]