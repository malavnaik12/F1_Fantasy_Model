def _parse_list(file_name: str):
    with open(f"./input_files/{file_name}","r+") as item_list:
        return [item.split('\n')[0] for item in item_list.readlines()]
    
def gp_parse(gp_info_file="list_gp_info.txt"):
    gp_info = [item.split(",") for item in _parse_list(gp_info_file)]
    gp_info_locs = [item[0] for item in gp_info]
    return gp_info_locs

def gp_type_parse(gp_info_file="list_gp_info.txt"):
    gp_info = [item.split(",") for item in _parse_list(gp_info_file)]
    gp_type = [item[1] for item in gp_info]
    return gp_type

def sessions_parse(raceLoc):
    gp_info_locs = gp_parse()
    gp_type = gp_type_parse()
    get_race_indx = gp_info_locs.index(raceLoc)
    sessions = _parse_list("list_session_types.txt")
    weekend_type = gp_type[get_race_indx]
    if weekend_type == 'Normal':
        sessions.pop(sessions.index('Sprint Qualifying'))
        sessions.pop(sessions.index('Sprint Race'))
    elif weekend_type == 'Sprint':
        sessions.pop(sessions.index('Free Practice 2'))
        sessions.pop(sessions.index('Free Practice 3'))
    return sessions

if __name__ == "__main__":
    # gp_parse()
    print("Not executable by itself.")