import yaml
import json
import os
import shutil

class UpdateData:
    def __init__(self):
        self.dir_files = os.listdir(os.getcwd())
        if "database.json" in self.dir_files:
            with open("database.json") as db_file:
                try:
                    self.teams = json.load(db_file)
                except Exception:
                    print(f"\nPotential Empty database.json file detected.\n  Delete the database.json file from the folder and re-execute the database.py")
        else:    
            with open("data_structure.yaml", "r") as file:
                inputs = yaml.safe_load(file)
                data_attrs = inputs["attributes"]
                team_info = inputs["team_data"]
                team_names = list(team_info.keys())
                teams = {key: {} for key in team_names}
                for team in list(teams.keys()):
                    for attribute in list(data_attrs.keys()):
                        teams[team][attribute] = []
                    drivers = team_info[team]
                    for driver in list(drivers.keys()):
                        drivers[driver] = data_attrs
                        teams[team][driver] = data_attrs
            
            with open("database.json","w") as db_file:
                json.dump(teams, db_file, indent=2)

    def get_current_week_data(self):
        with open("positions.yaml", "r") as data_file:
            curr_week_info = yaml.safe_load(data_file)
            data_session = curr_week_info["session_info"]["session_type"]
            curr_week_positions = curr_week_info["current_week"]
        with open("inputs.yaml","r") as inputs_file:
            curr_week_num = yaml.safe_load(inputs_file)["race_week_num"]
        
        try:
            working_dir = os.getcwd()
            database_file = "\\database.json"
            if data_session == 'race':
                session_id = 'race_hist'
            elif data_session == 'quali':
                session_id = 'quali_hist'
            elif data_session == 'fp':
                session_id = 'fp'
                try:
                    session_num = int(curr_week_info["session_info"]["session_num"])
                except:
                    raise TypeError
            else:
                raise ValueError
            for team_name in curr_week_positions.keys():
                driver_info = curr_week_positions[team_name]
                for driver_name in driver_info.keys():
                    if (session_id == 'fp' and (len(self.teams[team_name][driver_name][session_id]) <= session_num)):
                        self.teams[team_name][driver_name][session_id].append(driver_info[driver_name])
                    else:
                        if (len(self.teams[team_name][driver_name][session_id]) < curr_week_num):
                            self.teams[team_name][driver_name][session_id].append(driver_info[driver_name])
                # print(self.teams[team_name])
                # input()
            shutil.move(working_dir+database_file,working_dir+'\\database_old.json')
            with open("database_update.json","w") as db_file:
                json.dump(self.teams, db_file, indent=2)
            shutil.move(working_dir+"\\database_update.json",working_dir+database_file)
            
        except ValueError:
            print(f"ValueError in database.py.\n  Incorrect session_type specified in positions.yaml.\n  Correct Options:\n'fp' (and corresponding fp session number via session_num)\n'quali'\n'race'")
            # pass
        except TypeError:
            print(f"ValueError in database.py.\n  The free practice specified session_num in positions.yaml is not valid, must be 1, 2, or 3 corresponding to the free practice session number.")
            # pass
    def main(self):
        try:
            self.get_current_week_data()
        except AttributeError:
            print(f"Message from database.py.\n The database file, database.json, is created. Re-run the database.py to start populating database.json file.")

if __name__ == '__main__':
    db_gen = UpdateData()
    db_gen.main()