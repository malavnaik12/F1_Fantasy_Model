import yaml
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import postdata_positions as pd_pos
import postdata_prices as pd_prices
from PIL import Image, ImageTk

class postdata_gui:
    def __init__(self):
        self.out_dict, self.constructor_names = pd_pos.main()
        self.out_dict_prices = pd_prices.main()
        self.out_dict_ga_inputs = {}
        self.sessions = ['Free Practice','Qualifying','Race']
        self.fp_sessions_nums = ['1','2','3']
        self.overrides = ['fp_override','quali_override','race_override']
        self.session_types = {'Free Practice':'fp','Qualifying':'quali','Race':'race'}
        self.image = "./picture_files/F1_logo.png"
        self.width = 700
        self.height = 625

    def get_session(self,event):
        try:
            self.fp_session_label.grid_remove()
            self.fp_session_menu.grid_remove()
            self.fp_session_override_label.grid_forget()
            self.fp_session_override.grid_remove()
            self.other_session_label.grid_remove()
            self.other_session_override.grid_remove()
            self.listbox1.delete(0,END)
            self.listbox2.delete(0,END)
            self.listbox3.delete(0,END)
        except:
            pass
        self.session_type = event
        if self.session_type == self.sessions[0]:
            self.fp_session_label = Label(self.positions_sframe1, text=f'Select FP Session: ',font=("Helvetica 9"))
            self.fp_session_label.grid(row=4,column=0,sticky='w')
            self.session_num_var = StringVar(self.positions_sframe1)
            self.session_num_var.set("Select")
            self.fp_session_menu = OptionMenu(self.positions_sframe1, self.session_num_var, *self.fp_sessions_nums, command=self.get_fp_session)
            self.fp_session_menu.grid(row=4,column=2,sticky='w')
        else:
            self.other_session_label = Label(self.positions_sframe1, text=f'Override Pos. Data for {self.session_type}?',font=("Helvetica 9"))
            self.other_session_label.grid(row=5,column=0,sticky='w')
            self.other_override = IntVar()
            self.other_override.set(1)
            self.other_session_override = Checkbutton(self.positions_sframe1, text="Yes", onvalue=1, offvalue=0, variable=self.other_override, command=self.pos_override)
            self.other_session_override.grid(row=5,column=2,sticky='w')
        self.out_dict["session_info"]["session_type"] = self.session_types[self.session_type]

    def get_fp_session(self, fp_session):
        try:
            self.listbox1.delete(0,END)
            self.listbox2.delete(0,END)
            self.listbox3.delete(0,END)
        except:
            pass
        self.out_dict["session_info"]["session_num"] = fp_session
        self.fp_session_override_label = Label(self.positions_sframe1, text=f'Override Pose. Data for FP{fp_session}?',font=("Helvetica 9"))
        self.fp_session_override_label.grid(row=5,column=0,sticky='w')
        self.fp_override = IntVar()
        self.fp_override.set(1)
        self.fp_session_override = Checkbutton(self.positions_sframe1, text="Yes", onvalue=1, offvalue=0, variable=self.fp_override, command=self.pos_override)
        self.fp_session_override.grid(row=5,column=2,sticky='w')

    def pos_override(self):
        if self.session_type == self.sessions[0]:
            fp_override = self.fp_override.get()
            if fp_override:
                override = True
            else:
                override = False
            self.out_dict["session_info"]["fp_override"] = override
        else:
            other_session_override = self.other_override.get()
            if self.session_type == self.sessions[1]:
                session = 'quali_override'
            elif self.session_type == self.sessions[2]:
                session = 'race_override'
            if other_session_override:
                override = True
            else:
                override = False
            self.out_dict["session_info"][session] = override

    def get_drivers_positions(self,team):
        try:
            self.driver_label1.grid_remove()
            self.driver_val1.grid_remove()
            self.driver_label2.grid_remove()
            self.driver_val2.grid_remove()
            self.enter_driver_pos.grid_remove()
            self.positions_ssframe1.grid_remove()
        except:
            pass
        self.curr_team = team
        self.drivers = [driver.capitalize() for driver in self.out_dict['current_week'][self.curr_team.lower()]]
        self.driver_label1 = Label(self.positions_sframe1, text=f"Enter Position for {self.drivers[0]}",font=("Helvetica 9"))
        self.driver_label1.grid(row=7,column=0,sticky='w')
        self.driver_val1 = Entry(self.positions_sframe1, width=5)
        self.driver_val1.grid(row=7,column=2,sticky='w')
        self.driver_label2 = Label(self.positions_sframe1, text=f"Enter Position for {self.drivers[1]}",font=("Helvetica 9"))
        self.driver_label2.grid(row=8,column=0,sticky='w')
        self.driver_val2 = Entry(self.positions_sframe1, width=5)
        self.driver_val2.grid(row=8,column=2,sticky='w')
        self.enter_driver_pos = Button(self.positions_sframe1,text="Enter",command=self.set_driver_pos_info)
        self.enter_driver_pos.grid(row=8,column=2,sticky='e')
        self.reserve_driver_entry_label_pos = Label(self.positions_sframe1, text=f'Are there any driver replacements?',font=("Helvetica 9"))
        self.reserve_driver_entry_label_pos.grid(row=9,column=0,sticky='w')
        self.reserve_driver_entry_pos = IntVar()
        self.reserve_driver_entry_pos.set(0)
        self.enter_reserve_pos = Checkbutton(self.positions_sframe1, text="Yes", onvalue=1, offvalue=0, variable=self.reserve_driver_entry_pos, command=self.enter_reserve_driver_pos)
        self.enter_reserve_pos.grid(row=9,column=2,sticky='w')

    def enter_reserve_driver_pos(self):
        self.positions_ssframe1 = ttk.Frame(self.positions_sframe1,borderwidth=2,relief='sunken')
        self.positions_ssframe1.grid(row=10,column=0,columnspan=3,sticky='nsew')
        self.positions_ssframe1.grid_rowconfigure(0, weight=1)
        self.positions_ssframe1.grid_rowconfigure(1, weight=1)
        self.positions_ssframe1.grid_rowconfigure(2, weight=1)
        self.positions_ssframe1.grid_columnconfigure(0, weight=1)
        self.positions_ssframe1.grid_columnconfigure(1, weight=1)
        self.positions_ssframe1.grid_columnconfigure(2, weight=1)
        self.reserve_driver_title_pos = Label(self.positions_ssframe1, text=f"Replacement Driver Entries and Info",anchor='center',font=("Helvetica 9"))
        self.reserve_driver_title_pos.grid(row=0,column=0,columnspan=3,sticky='nsew')
        self.reserve_driver_name_label_pos = Label(self.positions_ssframe1, text=f'Enter Name of Replacement Driver',font=("Helvetica 9"))
        self.reserve_driver_name_label_pos.grid(row=1,column=0,sticky='w')
        self.reserve_driver_name_pos = Entry(self.positions_ssframe1, width=10)
        self.reserve_driver_name_pos.grid(row=1,column=2,sticky='w')
        self.reserve_driver_pos_label = Label(self.positions_ssframe1, text=f'Enter Pos of Replacement Driver',font=("Helvetica 9"))
        self.reserve_driver_pos_label.grid(row=2,column=0,sticky='w')
        self.reserve_driver_pos = Entry(self.positions_ssframe1, width=10)
        self.reserve_driver_pos.grid(row=2,column=2,sticky='w')

    def set_driver_pos_info(self):
        pos1 = self.driver_val1.get()
        pos2 = self.driver_val2.get()
        driver1 = self.drivers[0]
        driver2 = self.drivers[1]
        if pos1 == '':
            try:
                self.out_dict['current_week'][self.curr_team.lower()].pop(driver1.lower())
            except:
                pass
            pos1 = self.reserve_driver_pos.get()
            driver1 = self.reserve_driver_name_pos.get().capitalize()
            self.out_dict['current_week'][self.curr_team.lower()][driver1.lower()] = int()
        elif pos2 == '':
            try:
                self.out_dict['current_week'][self.curr_team.lower()].pop(driver2.lower())
            except:
                pass
            pos2 = self.reserve_driver_pos.get()
            driver2 = self.reserve_driver_name_pos.get().capitalize()
            self.out_dict['current_week'][self.curr_team.lower()][driver2.lower()] = int()
        if (pos1 == '' or pos2 == ''):
            raise ValueError("Position Incorrectly Entered\nEnsure if Reserve Driver is needed and leave position blank for driver being replaced.")
        try:
            constructor_indx = self.listbox1.get(0, END).index(self.curr_team)
            driver1_indx = self.listbox2.get(0, END).index(driver1)
            driver2_indx = self.listbox2.get(0, END).index(driver2)
            self.listbox1.delete(constructor_indx)
            self.listbox2.delete(driver1_indx)
            self.listbox2.delete(driver2_indx)
            self.listbox3.delete(driver1_indx)
            self.listbox3.delete(driver2_indx)
            # self.listbox1.delete(END)
            self.listbox2.delete(END)
            self.listbox3.delete(END)
        except:
            pass
        try:
            pos_num1 = int(pos1)
            pos_num2 = int(pos2)
            assert(20 >= pos_num1 > 0 )
            assert(20 >= pos_num2 > 0 )
        except: 
            raise ValueError("Enter a number between 1 and 20.")
        self.listbox1.insert(END,self.curr_team)
        self.listbox2.insert(END,driver1)
        self.listbox3.insert(END,pos1)
        self.listbox2.insert(END,driver2)
        self.listbox3.insert(END,pos2)

        self.out_dict['current_week'][self.curr_team.lower()][driver1.lower()] = pos_num1
        self.out_dict['current_week'][self.curr_team.lower()][driver2.lower()] = pos_num2
        self.create_pos_yaml_file = Button(self.positions_sframe1,text="Save Inputs",command=self.create_positions_yaml)
        self.create_pos_yaml_file.grid(row=11,column=2,sticky='e')

    def create_positions_yaml(self):
        with open('test.yaml',"w") as file:
            yaml.dump(self.out_dict, file, indent=2)

    def get_price_info(self,team):
        try:
            self.price_label1.grid_remove()
            self.price_label1_val.grid_remove()
            self.price_label2.grid_remove()
            self.price_label2_val.grid_remove()
            self.price_label3.grid_remove()
            self.price_label3_val.grid_remove()
        except:
            pass
        self.price_team = team
        self.price_keys = [item.capitalize() for item in self.out_dict_prices['current_week'][self.price_team.lower()]]
        self.price_label1 = Label(self.prices_sframe1, text=f"Enter Price for {self.price_team}",font=("Helvetica 9"))
        self.price_label1.grid(row=7,column=0,sticky='w')
        self.price_label1_val = Entry(self.prices_sframe1, width=5)
        self.price_label1_val.grid(row=7,column=2,sticky='w')
        self.price_label2 = Label(self.prices_sframe1, text=f"Enter Price for {self.price_keys[1]}",font=("Helvetica 9"))
        self.price_label2.grid(row=8,column=0,sticky='w')
        self.price_label2_val = Entry(self.prices_sframe1, width=5)
        self.price_label2_val.grid(row=8,column=2,sticky='w')
        self.price_label3 = Label(self.prices_sframe1, text=f"Enter Price for {self.price_keys[2]}",font=("Helvetica 9"))
        self.price_label3.grid(row=9,column=0,sticky='w')
        self.price_label3_val = Entry(self.prices_sframe1, width=5)
        self.price_label3_val.grid(row=9,column=2,sticky='w')
        self.enter_driver_price = Button(self.prices_sframe1,text="Enter",command=self.set_price_info)
        self.enter_driver_price.grid(row=9,column=2,sticky='e')
        
        self.reserve_driver_entry_label_price = Label(self.prices_sframe1, text=f'Are there any driver replacements?',font=("Helvetica 9"))
        self.reserve_driver_entry_label_price.grid(row=10,column=0,sticky='w')
        self.reserve_driver_entry_price = IntVar()
        self.reserve_driver_entry_price.set(0)
        self.enter_reserve_price = Checkbutton(self.prices_sframe1, text="Yes", onvalue=1, offvalue=0, variable=self.reserve_driver_entry_price, command=self.enter_reserve_driver_price)
        self.enter_reserve_price.grid(row=10,column=2,sticky='w')

    def enter_reserve_driver_price(self):
        self.prices_ssframe1 = ttk.Frame(self.prices_sframe1,borderwidth=2,relief='sunken')
        self.prices_ssframe1.grid(row=11,column=0,columnspan=3,sticky='nsew')
        self.prices_ssframe1.grid_rowconfigure(0, weight=1)
        self.prices_ssframe1.grid_rowconfigure(1, weight=1)
        self.prices_ssframe1.grid_rowconfigure(2, weight=1)
        self.prices_ssframe1.grid_columnconfigure(0, weight=1)
        self.prices_ssframe1.grid_columnconfigure(1, weight=1)
        self.prices_ssframe1.grid_columnconfigure(2, weight=1)
        self.reserve_driver_title_price = Label(self.prices_ssframe1, text=f"Replacement Driver Entries and Info",anchor='center',font=("Helvetica 9"))
        self.reserve_driver_title_price.grid(row=0,column=0,columnspan=3,sticky='nsew')
        self.reserve_driver_name_label_price = Label(self.prices_ssframe1, text=f'Enter Name of Replacement Driver',font=("Helvetica 9"))
        self.reserve_driver_name_label_price.grid(row=1,column=0,sticky='w')
        self.reserve_driver_name_price = Entry(self.prices_ssframe1, width=10)
        self.reserve_driver_name_price.grid(row=1,column=2,sticky='w')
        self.reserve_driver_price_label = Label(self.prices_ssframe1, text=f'Enter Price of Replacement Driver',font=("Helvetica 9"))
        self.reserve_driver_price_label.grid(row=2,column=0,sticky='w')
        self.reserve_driver_price = Entry(self.prices_ssframe1, width=10)
        self.reserve_driver_price.grid(row=2,column=2,sticky='w')

    def set_price_info(self):
        try:
            price1 = float(self.price_label1_val.get())
            assert(200.0 > price1 >= 0.0)
        except:
            raise ValueError(f"Unexpected Constructor Price detected for {self.price_team}. Double check the input value.")
        try:
            price2 = float(self.price_label2_val.get())
            price3 = float(self.price_label3_val.get())
            assert(200.0 > price2 >= 0.0)
            assert(200.0 > price3 >= 0.0)
        except:
            raise ValueError(f"Unexpected Driver Prices detected. Double check the input value.")

        try:
            constructor_indx = self.prices_listbox1.get(0, END).index(self.price_team)
            driver1_indx = self.prices_listbox3.get(0, END).index(self.price_keys[1])
            driver2_indx = self.prices_listbox3.get(0, END).index(self.price_keys[2])
            self.prices_listbox1.delete(constructor_indx)
            self.prices_listbox2.delete(constructor_indx)
            self.prices_listbox3.delete(driver1_indx)
            self.prices_listbox4.delete(driver1_indx)
            self.prices_listbox3.delete(driver2_indx)
            self.prices_listbox4.delete(driver2_indx)
            # self.prices_listbox1.delete(END)
            self.prices_listbox2.delete(END)
            self.prices_listbox3.delete(END)
            self.prices_listbox4.delete(END)
        except:
            pass
        self.prices_listbox1.insert(END,self.price_team)
        self.prices_listbox2.insert(END,price1)
        self.prices_listbox3.insert(END,self.price_keys[1])
        self.prices_listbox4.insert(END,price2)
        self.prices_listbox3.insert(END,self.price_keys[2])
        self.prices_listbox4.insert(END,price3)

        self.out_dict_prices['current_week'][self.price_team.lower()][self.price_keys[0].lower()] = price1
        self.out_dict_prices['current_week'][self.price_team.lower()][self.price_keys[1].lower()] = price2
        self.out_dict_prices['current_week'][self.price_team.lower()][self.price_keys[2].lower()] = price3
        self.create_price_yaml_file = Button(self.prices_sframe1,text="Save Inputs",command=self.create_prices_yaml)
        self.create_price_yaml_file.grid(row=12,column=2,sticky='w')

    def create_prices_yaml(self):
        constructor_override = bool(self.constructor_price_override.get())
        driver_override = bool(self.driver_price_override.get())
        try:
            budget = float(self.budget_val.get())
            assert(200.0 > budget >= 0.0)
        except:
            raise ValueError("Unexpected Budget value detected. Double check the input value.")
        self.out_dict_prices["constructor_override"] = constructor_override
        self.out_dict_prices["driver_override"] = driver_override
        self.out_dict_prices["weekly_budget"] = budget
        with open('test_1.yaml',"w") as file:
            yaml.dump(self.out_dict_prices, file, indent=2)

    def main(self):
        self.root = Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("GA-Powered F1 Fantasy")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(row=0,column=0,sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        img = ImageTk.PhotoImage(Image.open(self.image).resize((self.width-200,self.height-325),Image.ADAPTIVE))
        self.notes = ttk.Notebook(self.root)
        self.notes.grid(row=0,column=0,sticky='nsew')
        self.style = ttk.Style()
        self.style.theme_use('winnative')

        self.positions_mframe = ttk.Frame(self.notes)
        self.notes.add(self.positions_mframe, text='Positions')
        self.positions_mframe.grid_rowconfigure(list(range(12)), weight=1)
        self.positions_mframe.grid_columnconfigure(list(range(2)), weight=1)
        lbl_1 = Label(self.positions_mframe,image=img)
        lbl_1.grid(row=0,column=0,columnspan=2,sticky='nsew')
        self.positions_sframe1 = ttk.Frame(self.positions_mframe,borderwidth=2,relief='sunken')
        self.positions_sframe1.grid(row=1,column=0,sticky='nsew')
        self.gui_title1 = Label(self.positions_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title1.grid(row=12,column=0,columnspan=2,sticky='nsew')
        self.footer1 = Label(self.positions_mframe, text=f"Made by Malav Naik 2024",anchor='center',font=("Helvetica 6"))
        self.footer1.grid(row=13,column=0,columnspan=2,sticky='nsew')
        self.positions_label1 = Label(self.positions_sframe1, text='Current Week Positions\nDrivers and Constructors',anchor='center',font=("Helvetica 12"))
        self.positions_label1.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.positions_sframe1.grid_rowconfigure(list(range(14)), weight=1)
        self.positions_sframe1.grid_columnconfigure(list(range(3)), weight=1)
        self.sessions_label = Label(self.positions_sframe1, text='Session Type: ',font=("Helvetica 9"))
        self.sessions_label.grid(row=3,column=0,sticky='w')
        self.session_var = StringVar(self.positions_sframe1)
        self.session_var.set("Select")
        self.sessions_menu = OptionMenu(self.positions_sframe1, self.session_var, *self.sessions, command=self.get_session)
        self.sessions_menu.grid(row=3,column=2,sticky='w')
        self.constructors_label = Label(self.positions_sframe1, text='Select Constructor: ',font=("Helvetica 9"))
        self.constructors_label.grid(row=6,column=0,sticky='w')
        self.constructor_var = StringVar(self.positions_sframe1)
        self.constructor_var.set("Select")
        self.constructors_menu = OptionMenu(self.positions_sframe1, self.constructor_var, *self.constructor_names, command=self.get_drivers_positions)
        self.constructors_menu.grid(row=6,column=2,sticky='w')
        self.positions_sframe2 = ttk.Frame(self.positions_mframe,borderwidth=2,relief='sunken')
        self.positions_sframe2.grid(row=1,column=1,sticky='nsew')
        self.positions_sframe2.grid_rowconfigure(list(range(4)), weight=1)
        self.positions_sframe2.grid_columnconfigure(list(range(3)), weight=1)
        self.listbox_suptitle = Label(self.positions_sframe2, text=f"Completed Inputs",anchor='center',font=("Helvetica 12"))
        self.listbox_suptitle.grid(row=0,column=0,columnspan=3,sticky='nsew')
        self.listbox1_title = Label(self.positions_sframe2, text=f"Constructors",anchor='center',font=("Helvetica 9"))
        self.listbox1_title.grid(row=1,column=0,sticky='nsew')
        self.listbox1 = Listbox(self.positions_sframe2,width=10,justify='center')
        self.listbox1.grid(row=2,column=0,sticky='nsew')
        self.listbox2_title = Label(self.positions_sframe2, text=f"Drivers",anchor='center',font=("Helvetica 9"))
        self.listbox2_title.grid(row=1,column=1,sticky='nsew')
        self.listbox2 = Listbox(self.positions_sframe2,width=8,justify='center')
        self.listbox2.grid(row=2,column=1,sticky='nsew')
        self.listbox3_title = Label(self.positions_sframe2, text=f"Pos",anchor='center',font=("Helvetica 9"))
        self.listbox3_title.grid(row=1,column=2,sticky='nsew')
        self.listbox3 = Listbox(self.positions_sframe2,width=2,justify='center')
        self.listbox3.grid(row=2,column=2,sticky='nsew')
        
        self.prices_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.prices_mframe, text='Prices')
        self.prices_mframe.grid_rowconfigure(list(range(12)), weight=1)
        self.prices_mframe.grid_columnconfigure(list(range(2)), weight=1)
        lbl_2 = Label(self.prices_mframe,image=img)
        lbl_2.grid(row=0,column=0,columnspan=2,sticky='nsew')
        self.prices_sframe1 = ttk.Frame(self.prices_mframe,borderwidth=2,relief='sunken')
        self.prices_sframe1.grid(row=1,column=0,sticky='nsew')
        self.prices_label1 = Label(self.prices_sframe1, text='Current Week Prices\nDrivers and Constructors',anchor='center',font=("Helvetica 12"))
        self.prices_label1.grid(row=1,column=0,columnspan=4,sticky='nsew')
        self.gui_title2 = Label(self.prices_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title2.grid(row=13,column=0,columnspan=2,sticky='nsew')
        self.footer2 = Label(self.prices_mframe, text=f"Made by Malav Naik 2024",anchor='center',font=("Helvetica 6"))
        self.footer2.grid(row=14,column=0,columnspan=2,sticky='nsew')
        self.line3 = ttk.Separator(self.prices_sframe1).grid(row=2,column=0,columnspan=3,sticky='nsew')
        self.line4 = ttk.Separator(self.prices_sframe1).grid(row=2,column=1,rowspan=13,sticky='nsew')
        self.prices_sframe1.grid_rowconfigure(list(range(15)), weight=1)
        self.prices_sframe1.grid_columnconfigure(list(range(3)), weight=1)
        self.budget = Label(self.prices_sframe1, text=f"Team Budget (millions)",font=("Helvetica 9"))
        self.budget.grid(row=3,column=0,sticky='w')
        self.budget_val = Entry(self.prices_sframe1, width=10)
        self.budget_val.grid(row=3,column=2,sticky='w')
        self.constructor_price_override_label = Label(self.prices_sframe1, text=f'Override Constructor Price Data?',font=("Helvetica 9"))
        self.constructor_price_override_label.grid(row=4,column=0,sticky='w')    
        self.constructor_price_override = IntVar()
        self.constructor_price_override.set(1)
        self.constructor_price_override_input = Checkbutton(self.prices_sframe1, text="Yes", onvalue=1, offvalue=0, variable=self.constructor_price_override)
        self.constructor_price_override_input.grid(row=4,column=2,sticky='w')
        self.driver_price_override_label = Label(self.prices_sframe1, text=f'Override Driver Price Data?',font=("Helvetica 9"))
        self.driver_price_override_label.grid(row=5,column=0,sticky='w')    
        self.driver_price_override = IntVar()
        self.driver_price_override.set(1)
        self.driver_price_override_input = Checkbutton(self.prices_sframe1, text="Yes", onvalue=1, offvalue=0, variable=self.driver_price_override)
        self.driver_price_override_input.grid(row=5,column=2,sticky='w')
        self.constructors_price_label = Label(self.prices_sframe1, text='Select Constructor: ',font=("Helvetica 9"))
        self.constructors_price_label.grid(row=6,column=0,sticky='w')
        self.constructor_price_name = StringVar(self.prices_sframe1)
        self.constructor_price_name.set("Select")
        self.constructors_price_menu = OptionMenu(self.prices_sframe1, self.constructor_price_name, *self.constructor_names, command=self.get_price_info)
        self.constructors_price_menu.grid(row=6,column=2,sticky='w')
        self.prices_sframe2 = ttk.Frame(self.prices_mframe,borderwidth=2,relief='sunken')
        self.prices_sframe2.grid(row=1,column=1,sticky='nsew')
        self.prices_sframe2.grid_rowconfigure(list(range(4)), weight=1)
        self.prices_sframe2.grid_columnconfigure(list(range(4)), weight=1)
        self.prices_listbox_suptitle = Label(self.prices_sframe2, text=f"Completed Inputs",anchor='center',font=("Helvetica 12"))
        self.prices_listbox_suptitle.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.prices_listbox1_title = Label(self.prices_sframe2, text=f"Constructors",anchor='center',font=("Helvetica 9"))
        self.prices_listbox1_title.grid(row=1,column=0,sticky='nsew')
        self.prices_listbox1 = Listbox(self.prices_sframe2,width=8,justify='center')
        self.prices_listbox1.grid(row=2,column=0,sticky='nsew')
        self.prices_listbox2_title = Label(self.prices_sframe2, text=f"Price",anchor='center',font=("Helvetica 9"))
        self.prices_listbox2_title.grid(row=1,column=1,sticky='nsew')
        self.prices_listbox2 = Listbox(self.prices_sframe2,width=1,justify='center')
        self.prices_listbox2.grid(row=2,column=1,sticky='nsew')
        self.prices_listbox3_title = Label(self.prices_sframe2, text=f"Drivers",anchor='center',font=("Helvetica 9"))
        self.prices_listbox3_title.grid(row=1,column=2,sticky='nsew')
        self.prices_listbox3 = Listbox(self.prices_sframe2,width=8,justify='center')
        self.prices_listbox3.grid(row=2,column=2,sticky='nsew')
        self.prices_listbox4_title = Label(self.prices_sframe2, text=f"Price",anchor='center',font=("Helvetica 9"))
        self.prices_listbox4_title.grid(row=1,column=3,sticky='nsew')
        self.prices_listbox4 = Listbox(self.prices_sframe2,width=1,justify='center')
        self.prices_listbox4.grid(row=2,column=3,sticky='nsew')
        
        self.ga_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.ga_mframe, text='GA Inputs')
        lbl_3 = Label(self.ga_mframe,image=img)
        lbl_3.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.ga_mframelabel_1 = Label(self.ga_mframe, text='Current Week GA Inputs\nParameters for Optimizations',anchor='center',font=("Helvetica 12"))
        self.ga_mframelabel_1.grid(row=1,column=0,columnspan=4,sticky='nsew')
        self.gui_title3 = Label(self.ga_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title3.grid(row=12,column=0,columnspan=4,sticky='nsew')
        self.footer3 = Label(self.ga_mframe, text=f"Made by Malav Naik 2024",anchor='center',font=("Helvetica 6"))
        self.footer3.grid(row=13,column=0,columnspan=4,sticky='nsew')
        self.line5 = ttk.Separator(self.ga_mframe).grid(row=2,column=0,columnspan=4,sticky='nsew')
        self.line6 = ttk.Separator(self.ga_mframe).grid(row=2,column=1,rowspan=5,sticky='nsew')
        self.ga_mframe.grid_rowconfigure(list(range(14)), weight=1)
        self.ga_mframe.grid_columnconfigure(list(range(3)), weight=1)
        self.max_gens = Label(self.ga_mframe, text=f"Enter Maximum number of Generations: ",font=("Helvetica 9"))
        self.max_gens.grid(row=3,column=0,sticky='w')
        self.max_gens_val = Entry(self.ga_mframe, width=5)
        self.max_gens_val.grid(row=3,column=2,sticky='w')
        self.pop_set = Label(self.ga_mframe, text=f"Enter Size of the Population Set: ",font=("Helvetica 9"))
        self.pop_set.grid(row=4,column=0,sticky='w')
        self.pop_set_val = Entry(self.ga_mframe, width=5)
        self.pop_set_val.grid(row=4,column=2,sticky='w')
        self.crossover = Label(self.ga_mframe, text=f"Enter Crossover Probability: ",font=("Helvetica 9"))
        self.crossover.grid(row=5,column=0,sticky='w')
        self.crossover_val = Entry(self.ga_mframe, width=5)
        self.crossover_val.grid(row=5,column=2,sticky='w')
        self.mutation = Label(self.ga_mframe, text=f"Enter Mutation Rate: ",font=("Helvetica 9"))
        self.mutation.grid(row=6,column=0,sticky='w')
        self.mutation_val = Entry(self.ga_mframe, width=5)
        self.mutation_val.grid(row=6,column=2,sticky='w')
        self.elitism = Label(self.ga_mframe, text=f"Enter Elitism Rate: ",font=("Helvetica 9"))
        self.elitism.grid(row=7,column=0,sticky='w')
        self.elitism_val = Entry(self.ga_mframe, width=5)
        self.elitism_val.grid(row=7,column=2,sticky='w')
        self.tournament_prop = Label(self.ga_mframe, text=f"Enter Tournament Size Proportion: ",font=("Helvetica 9"))
        self.tournament_prop.grid(row=8,column=0,sticky='w')
        self.tournament_prop_val = Entry(self.ga_mframe, width=5)
        self.tournament_prop_val.grid(row=8,column=2,sticky='w')
        self.race_week = Label(self.ga_mframe, text=f"Enter The Number of Current Race Week: ",font=("Helvetica 9"))
        self.race_week.grid(row=9,column=0,sticky='w')
        self.race_week_val = Entry(self.ga_mframe, width=5)
        self.race_week_val.grid(row=9,column=2,sticky='w')
        self.max_drivers = Label(self.ga_mframe, text=f"Enter The Maximum Number of Drivers Allowed: ",font=("Helvetica 9"))
        self.max_drivers.grid(row=10,column=0,sticky='w')
        self.max_drivers_val = Entry(self.ga_mframe, width=5)
        self.max_drivers_val.grid(row=10,column=2,sticky='w')
        self.max_constructors = Label(self.ga_mframe, text=f"Enter The Maximum Number of Constructors Allowed: ",font=("Helvetica 9"))
        self.max_constructors.grid(row=11,column=0,sticky='w')
        self.max_constructors_val = Entry(self.ga_mframe, width=5)
        self.max_constructors_val.grid(row=11,column=2,sticky='w')
        self.max_gens_val.insert(0,"150")
        self.pop_set_val.insert(0,"50")
        self.crossover_val.insert(0,"0.8")
        self.mutation_val.insert(0,"1")
        self.elitism_val.insert(0,"1")
        self.tournament_prop_val.insert(0,"0.9")
        self.max_drivers_val.insert(0,"5")
        self.max_constructors_val.insert(0,"2")

        self.exec_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.exec_mframe, text='Create Team')
        lbl_4 = Label(self.exec_mframe,image=img)
        lbl_4.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.exec_mframelabel_1 = Label(self.exec_mframe, text='Current Week\nUpdate Database and Generate Team',anchor='center',font=("Helvetica 12"))
        self.exec_mframelabel_1.grid(row=1,column=0,columnspan=4,sticky='nsew')
        self.gui_title4 = Label(self.exec_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title4.grid(row=7,column=0,columnspan=4,sticky='nsew')
        self.footer4 = Label(self.exec_mframe, text=f"Made by Malav Naik 2024",anchor='center',font=("Helvetica 6"))
        self.footer4.grid(row=8,column=0,columnspan=4,sticky='nsew')
        self.line7 = ttk.Separator(self.exec_mframe).grid(row=2,column=0,columnspan=4,sticky='nsew')
        self.line8 = ttk.Separator(self.exec_mframe).grid(row=2,column=1,rowspan=5,sticky='nsew')
        self.exec_mframe.grid_rowconfigure(list(range(12)), weight=1)
        self.exec_mframe.grid_columnconfigure(list(range(3)), weight=1)
        
        self.root.mainloop()
if __name__ == "__main__":
    class_init = postdata_gui()
    class_init.main()