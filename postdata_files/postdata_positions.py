import yaml

class generate_positions_yaml:
    def __init__(self):
        self.out_dict = {}
    
    def initialize_yaml_file(self):
        self.out_dict = {}
        self.out_dict["session_info"] = {}
        self.out_dict["session_info"]["session_type"] = str()
        self.out_dict["session_info"]["session_num"] = int()
        self.out_dict["session_info"]["fp_override"] = bool(1)
        self.out_dict["session_info"]["quali_override"] = bool(1)
        self.out_dict["session_info"]["race_override"] = bool(1)
        self.out_dict["current_week"] = {}
        with open('./input_files/data_structure.yaml') as data_struct_file:
            self.data_struct = yaml.safe_load(data_struct_file)
            data_struct_file.close()
        self.team_names = list(self.data_struct["team_data"].keys())
        self.team_out = [team.capitalize() for team in self.team_names]
        for team in self.team_names:
            self.out_dict["current_week"][team] = {}
            drivers = list(self.data_struct["team_data"][team].keys())
            for driver in drivers:
                self.out_dict["current_week"][team][driver] = int()

    def post_data(self,session,session_id):
        self.out_dict["session_info"]["session_type"] = session
        self.out_dict["session_info"]["session_num"] = session_id
        print(f"Requesting Data for {session}, {session_id}")
        for team in self.team_names:
            self.out_dict["current_week"][team] = {}
            drivers = list(self.data_struct["team_data"][team].keys())
            for driver in drivers:
                pos = input(f"Enter Position for following Driver, {driver} (Team: {team}): ")
                self.out_dict["current_week"][team][driver] = int(pos)

    def main(self):
        self.initialize_yaml_file()
        self.session_types = ['Free Practice','Qualifying','Race']
        self.fp_sessions_nums = ['1','2','3']
        self.overrides = ['fp_override','quali_override','race_override']
        # self.post_data(session=self.session_types[0],session_id=self.fp_sessions_nums[0])

        # with open('test.yaml',"w") as file:
        #     yaml.dump(self.out_dict, file, indent=2)
        return self.session_types, self.team_out
if __name__ == '__main__':
    gpy = generate_positions_yaml()
    gpy.main()
