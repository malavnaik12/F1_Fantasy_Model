import yaml

class generate_prices_yaml:
    def __init__(self):
        pass
    
    def initialize_yaml_file(self):
        self.out_dict = {}
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
        return self.out_dict

if __name__ == '__main__':
    print(f"""
            This file is not meant for standalone execution.\n
            The contents in the files are used to construct useful data objects for the GUI.""")
