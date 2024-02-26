import yaml
import json
import os
import shutil
import database_files.create_database as create_db_file

class UpdateData:
    def __init__(self):
        self.warning_price_c = False
        self.warning_price_d = False
        self.warning_fp = False
        self.warning_quali = False
        self.warning_race = False
        self.dir_files = os.listdir(os.getcwd()+"\\database_files\\")
        if "database.json" not in self.dir_files:
            create_db_file.main()
        with open("./database_files/database.json") as db_file:
            try:
                self.teams = json.load(db_file)
                db_file.close()
            except Exception:
                print(f"\nPotential Empty \33[3mdatabase.json\033[0m file detected.\n  Delete the \33[3mdatabase.json\033[0m file from the folder and re-execute the \33[3mdatabase.py\033[0m")
        
    def get_data(self):
        with open("./input_files/positions.yaml", "r") as data_file:
            self.curr_week_info = yaml.safe_load(data_file)
            self.data_session = self.curr_week_info["session_info"]["session_type"]
            self.curr_week_positions = self.curr_week_info["current_week"]
            data_file.close()
        with open("./input_files/inputs.yaml","r") as inputs_file:
            self.curr_week_num = yaml.safe_load(inputs_file)["race_week_num"]
            inputs_file.close()
        with open("./input_files/prices.yaml","r") as price_file:
            self.prices_info = yaml.safe_load(price_file)
            self.budget = self.prices_info["weekly_budget"]
            self.prices = self.prices_info["current_week"]
            price_file.close()
    
    def post_data(self):
        try:
            if self.data_session == 'race':
                session_id = 'race_hist'
                print(f"Note: \33[34msession_num\033[0m parameter under \33[34msession_info\033[0m in \33[3mpositions.yaml\033[0m is ignored.")
            elif self.data_session == 'quali':
                session_id = 'quali_hist'
                print(f"Note: \33[34msession_num\033[0m parameter under \33[34msession_info\033[0m in \33[3mpositions.yaml\033[0m is ignored.")
            elif self.data_session == 'fp':
                session_id = 'fp'
                try:
                    session_num = int(self.curr_week_info["session_info"]["session_num"])
                    assert(4 > session_num > 0)
                except:
                    raise TypeError(f"TypeError in \33[3mdatabase.py\033[0m.\n  The free practice specified \33[34msession_num\033[0m in \33[3mpositions.yaml\033[0m is not valid, must be \33[32m1\033[0m, \33[32m2\033[0m, or \33[32m3\033[0m corresponding to the free practice session number.")
            else:
                raise ValueError(f"ValueError in \33[3mdatabase.py\033[0m.\n  Incorrect session_type specified in \33[3mpositions.yaml\033[0m.\n  Correct Options:\n  \33[33mfp\033[0m (and corresponding fp session number via \33[34msession_num\033[0m)\n  \33[33mquali\033[0m\n  \33[33mrace\033[0m")
            for team_name in self.curr_week_positions.keys():
                driver_info = self.curr_week_positions[team_name]
                if (len(self.teams[team_name]["price"]) < self.curr_week_num):
                    self.teams[team_name]["price"].append(self.prices[team_name]["constructor"])
                else:
                    try:
                        assert(type(self.prices_info["constructor_override"]) == bool)
                    except:
                        raise TypeError(f"The value for \33[34mconstructor_override\033[0m in \33[3mprices.yaml\033[0m must be either \33[34mtrue\033[0m or \33[34mfalse\033[0m.\n  Instead, the value of \33[34m{self.prices_info["constructor_override"]}\033[0m was found")
                    if (self.prices_info["constructor_override"]):
                        self.teams[team_name]["price"][self.curr_week_num-1] = self.prices[team_name]["constructor"]
                    elif (not self.warning_price_c):
                        print(f"\033[1;31mWarning:\033[0m Constructor price already populated for this week.\n  Set \33[34mconstructor_override\033[0m to \33[34mtrue\033[0m in \33[3mprices.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                        self.warning_price_c = True
                driver_pos = 0
                for driver_name in driver_info.keys():
                    if (session_id == 'fp' and (len(self.teams[team_name][driver_name][session_id]) < session_num)):
                        self.teams[team_name][driver_name][session_id].append(driver_info[driver_name])
                        driver_pos += driver_info[driver_name]
                    elif (session_id == 'fp' and (len(self.teams[team_name][driver_name][session_id]) == 3)):
                        try:
                            assert(type(self.curr_week_info["session_info"]["fp_override"]) == bool)
                        except:
                            raise TypeError(f"The value for \33[34mfp_override\033[0m in \33[3mpositions.yaml\033[0m must be either \33[34mtrue\033[0m or \33[34mfalse\033[0m.\n  Instead, the value of \33[34m{self.curr_week_info["session_info"]["fp_override"]}\033[0m was found.")
                        if (self.curr_week_info["session_info"]["fp_override"]):
                            self.teams[team_name][driver_name][session_id][session_num-1] = driver_info[driver_name]
                            driver_pos += driver_info[driver_name]
                        elif (not self.warning_fp):
                            print(f"\033[1;31mWarning:\033[0m Driver {self.data_session}{session_num} position already populated for this session.\n  Set \33[34mfp_override\033[0m to \33[34mtrue\033[0m in \33[3mpositions.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                            self.warning_fp = True
                    else:
                        if (len(self.teams[team_name][driver_name][session_id]) < self.curr_week_num):
                            self.teams[team_name][driver_name][session_id].append(driver_info[driver_name])
                            driver_pos += driver_info[driver_name]
                        elif ((session_id == 'quali_hist' or session_id == 'race_hist' ) and (len(self.teams[team_name][driver_name][session_id]) == self.curr_week_num)):
                            try:
                                assert(type(self.curr_week_info["session_info"][f"{self.data_session}_override"]) == bool)
                            except:
                                raise TypeError(f"The value for \33[34m{self.data_session}_override\033[0m in \33[3mpositions.yaml\033[0m must be either \33[34mtrue\033[0m or \33[34mfalse\033[0m.\n  Instead, the value of \33[34m{self.curr_week_info["session_info"][f"{self.data_session}_override"]}\033[0m was found.")
                            if (self.curr_week_info["session_info"][f"{self.data_session}_override"]):
                                self.teams[team_name][driver_name][session_id][self.curr_week_num-1] = driver_info[driver_name]
                                driver_pos += driver_info[driver_name]
                            elif (not self.warning_quali and session_id == 'quali_hist'):
                                    print(f"\033[1;31mWarning:\033[0m Driver {self.data_session} position already populated for this session.\n  Set \33[34m{self.data_session}_override\033[0m to \33[34mtrue\033[0m in \33[3mpositions.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                                    self.warning_quali = True
                            elif (not self.warning_race and session_id == 'race_hist'):
                                    print(f"\033[1;31mWarning:\033[0m Driver {self.data_session} position already populated for this session.\n  Set \33[34m{self.data_session}_override\033[0m to \33[34mtrue\033[0m in \33[3mpositions.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                                    self.warning_race = True

                    if (len(self.teams[team_name][driver_name]["price"]) < self.curr_week_num):
                        self.teams[team_name][driver_name]["price"].append(self.prices[team_name][driver_name])
                    else:
                        try:
                            assert(type(self.prices_info["driver_override"]) == bool)
                        except:
                            raise TypeError(f"The value for \33[34mdriver_override\033[0m in \33[3mprices.yaml\033[0m must be either \33[34mtrue\033[0m or \33[34mfalse\033[0m.\n  Instead, the value of \33[34m{self.prices_info["driver_override"]}\033[0m was found.")
                        if (self.prices_info["driver_override"]):
                            self.teams[team_name][driver_name]["price"][self.curr_week_num-1] = self.prices[team_name][driver_name]
                        elif (not self.warning_price_d):
                            print(f"\033[1;31mWarning:\033[0m Driver price already populated for this week.\n  Set \33[34mdriver_override\033[0m to \33[34mtrue\033[0m in \33[3mprices.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                            self.warning_price_d = True
                avg_driver_pos = driver_pos/len(list(driver_info.keys()))
                if (session_id == 'fp' and (len(self.teams[team_name][session_id]) < session_num)):
                    self.teams[team_name][session_id].append(avg_driver_pos)
                elif (session_id == 'fp' and (len(self.teams[team_name][session_id]) == 3)):
                    if (self.curr_week_info["session_info"]["fp_override"]):
                        self.teams[team_name][session_id][session_num-1] = avg_driver_pos
                    # elif (not self.warning_fp):
                    #     print(f"\033[1;31mWarning:\033[0m Constructor {self.data_session}{session_num} position already populated for this session.\n  Set 'fp_override\033[0m to \33[34mtrue\033[0m in \33[3mpositions.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                    #     self.warning_fp = True
                else:
                    if (len(self.teams[team_name][session_id]) < self.curr_week_num):
                        self.teams[team_name][session_id].append(avg_driver_pos)
                    elif ((session_id == 'quali_hist' or session_id == 'race_hist' ) and (len(self.teams[team_name][session_id]) == self.curr_week_num)):
                        if (self.curr_week_info["session_info"][f"{self.data_session}_override"]):
                            self.teams[team_name][session_id][self.curr_week_num-1] = avg_driver_pos
                        # elif (not self.warning_quali and session_id == 'quali_hist'):
                        #         print(f"\033[1;31mWarning:\033[0m Constructor {self.data_session} position already populated for this session.\n  Set \33[34m{self.data_session}_override\033[0m to \33[34mtrue\033[0m in \33[3mpositions.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                        #         self.warning_quali = True
                        # elif (not self.warning_race and session_id == 'race_hist'):
                        #         print(f"\033[1;31mWarning:\033[0m Constructor {self.data_session} position already populated for this session.\n  Set \33[34m{self.data_session}_override\033[0m to \33[34mtrue\033[0m in \33[3mpositions.yaml\033[0m to overide value and re-run \33[3mdatabase.py\033[0m.")
                        #         self.warning_race = True
            
            working_dir = os.getcwd()
            database_file = "\\database_files\\database.json"
            shutil.move(working_dir+database_file,working_dir+'\\database_files\\database_old.json')
            with open("./database_files/database_update.json","w") as db_file:
                json.dump(self.teams, db_file, indent=2)
            shutil.move(working_dir+"\\database_files\\database_update.json",working_dir+database_file)
            
        except:
            raise Exception(f"There was an issue in \33[3mdatabase.py\033[0m.\n  Ensure your inputs in \33[3minputs.yaml\033[0m, \33[3mprices.yaml\033[0m, and \33[3mpositions.yaml\033[0m are correct")
            # pass
    
    def update_data(self):
        # Move the override code to this function
        pass

    def delete_data(self):
        # Include any code to delete data from database.py here
        pass

    def main(self):
        try:
            self.get_data()
            self.post_data()
        except AttributeError:
            print(f"Message from \33[3mdatabase.py\033[0m.\n The database file, \33[3mdatabase.json\033[0m, is created. Re-run the \33[3mdatabase.py\033[0m to start populating \33[3mdatabase.json\033[0m file.")

if __name__ == '__main__':
    db_gen = UpdateData()
    db_gen.main()