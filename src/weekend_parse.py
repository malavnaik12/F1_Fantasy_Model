
class WeekendParser():
    def __init__(self):
        self.gp_parse()
    def _parse_list(self,file_name: str):
        with open(f"./input_files/{file_name}","r+") as item_list:
            return [item.split('\n')[0] for item in item_list.readlines()]
        
    def gp_parse(self):
        gp_info = [item.split(",") for item in self._parse_list("list_gp_info.txt")]
        self.gp_info_locs = [item[0] for item in gp_info]
        self.gp_type = [item[1] for item in gp_info]
        # print(gp_info_locs,gp_type)
        return self.gp_info_locs

    def sessions_parse(self,raceLoc):
        get_race_indx = self.gp_info_locs.index(raceLoc)
        sessions = self._parse_list("list_session_types.txt")
        weekend_type = self.gp_type[get_race_indx]
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