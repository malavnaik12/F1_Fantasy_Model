import yaml

def main():
    out_dict = {}
    out_dict["session_info"] = {}
    out_dict["session_info"]["session_type"] = str()
    out_dict["session_info"]["session_num"] = int()
    out_dict["session_info"]["fp_override"] = bool(1)
    out_dict["session_info"]["quali_override"] = bool(1)
    out_dict["session_info"]["race_override"] = bool(1)
    out_dict["current_week"] = {}
    with open('./input_files/data_structure.yaml') as data_struct_file:
        data_struct = yaml.safe_load(data_struct_file)
        data_struct_file.close()
    team_names = list(data_struct["team_data"].keys())
    team_out = [team.capitalize() for team in team_names]
    for team in team_names:
        out_dict["current_week"][team] = {}
        drivers = list(data_struct["team_data"][team].keys())
        driver_list = []
        for driver in drivers:
            driver_list.append(driver.capitalize())
            out_dict["current_week"][team][driver] = int()
    return out_dict, team_out

if __name__ == '__main__':    
    print(f"""
            This file is not meant for standalone execution.\n
            The contents in the files are used to construct position data objects for the GUI.""")