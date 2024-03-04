import yaml

class generate_prices_yaml:
    def __init__(self):
        pass
    
    def initialize_yaml_file(self):
        self.out_dict = {}
        # self.out_dict["session_info"] = {}
        # self.out_dict["session_info"]["session_type"] = str()
        # self.out_dict["session_info"]["session_num"] = int()
        # self.out_dict["session_info"]["fp_override"] = bool(1)
        # self.out_dict["session_info"]["quali_override"] = bool(1)
        # self.out_dict["session_info"]["race_override"] = bool(1)
        self.out_dict["current_week"] = {}
        with open('./input_files/data_structure.yaml') as data_struct_file:
            self.data_struct = yaml.safe_load(data_struct_file)
            data_struct_file.close()
        self.team_names = list(self.data_struct["team_data"].keys())
        for team in self.team_names:
            self.out_dict["current_week"][team] = {}
            self.out_dict["current_week"][team]['constructor'] = float()
            drivers = list(self.data_struct["team_data"][team].keys())
            for driver in drivers:
                self.out_dict["current_week"][team][driver] = int()

            
        # self.team_out = [team.capitalize() for team in self.team_names]
        # for team in self.team_names:
        #     driver_list = []
        #         driver_list.append(driver.capitalize())
        #     self.team_info[team] = driver_list
        return self.out_dict

    # def post_data(self,session,session_id):
        # self.out_dict["session_info"]["session_type"] = session
        # self.out_dict["session_info"]["session_num"] = session_id
        # print(f"Requesting Data for {session}, {session_id}")
        # for team in self.team_names:
        #     self.out_dict["current_week"][team] = {}
        #     drivers = list(self.data_struct["team_data"][team].keys())
        #     for driver in drivers:
        #         pos = input(f"Enter Position for following Driver, {driver} (Team: {team}): ")
        #         self.out_dict["current_week"][team][driver] = int(pos)

if __name__ == '__main__':
    print(
        f"""
        This file is not meant for standalone execution.\n
        The contents in the files are used to construct useful data objects for the GUI."""
          )