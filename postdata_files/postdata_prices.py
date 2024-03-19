import yaml

def main():
    out_dict = {}
    out_dict["current_week"] = {}
    with open('./input_files/data_structure.yaml') as data_struct_file:
        data_struct = yaml.safe_load(data_struct_file)
        data_struct_file.close()
    team_names = list(data_struct["team_data"].keys())
    for team in team_names:
        out_dict["current_week"][team] = {}
        out_dict["current_week"][team]['constructor'] = float()
        drivers = list(data_struct["team_data"][team].keys())
        for driver in drivers:
            out_dict["current_week"][team][driver] = int()
    return out_dict

if __name__ == '__main__':
    print(f"""
            This file is not meant for standalone execution.\n
            The contents in the files are used to construct prices data objects for the GUI.""")
