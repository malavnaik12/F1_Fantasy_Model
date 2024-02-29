from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import postdata_positions as pd_pos
from PIL import Image, ImageTk
import yaml

class postdata_gui:
    def __init__(self):
        self.yaml_gen = pd_pos.generate_positions_yaml()
        self.full_team_data, self.out_dict = self.yaml_gen.initialize_yaml_file()
        self.sessions, self.constructor_names = self.yaml_gen.main()
        self.fp_sessions_nums = ['1','2','3']
        self.overrides = ['fp_override','quali_override','race_override']
        self.session_types = {'Free Practice':'fp','Qualifying':'quali','Race':'race'}
        self.image = "./picture_files/F1_logo.png"
        self.width = 275
        self.height = 450

    def get_session(self,event):
        try:
            self.fp_session_label.grid_remove()
            self.fp_session_menu.grid_remove()
            self.fp_session_override_label.grid_remove()
            self.fp_session_override.grid_remove()
            self.other_session_label.grid_remove()
            self.other_session_override.grid_remove()
        except:
            pass
        self.session_type = event
        if self.session_type == self.sessions[0]:
            self.fp_session_label = Label(self.positions_mframe, text=f'Select FP Session: ',font=("Helvetica 8"))
            self.fp_session_label.grid(row=4,column=0,sticky='w')
            self.session_num_var = StringVar(self.positions_mframe)
            self.session_num_var.set("Select Option")
            self.fp_session_menu = OptionMenu(self.positions_mframe, self.session_num_var, *self.fp_sessions_nums, command=self.get_fp_session)
            self.fp_session_menu.grid(row=4,column=2,sticky='w')
        else:
            self.other_session_label = Label(self.positions_mframe, text=f'Override Pos. Data for {self.session_type}?',font=("Helvetica 8"))
            self.other_session_label.grid(row=5,column=0,sticky='w')
            self.other_override = IntVar()
            self.other_override.set(1)
            self.other_session_override = Checkbutton(self.positions_mframe, text="Yes", onvalue=1, offvalue=0, variable=self.other_override, command=self.pos_override)
            self.other_session_override.grid(row=5,column=2,sticky='w')
        self.out_dict["session_info"]["session_type"] = self.session_types[self.session_type]
    
    def get_fp_session(self, fp_session):
        self.out_dict["session_info"]["session_num"] = fp_session
        self.fp_session_override_label = Label(self.positions_mframe, text=f'Override Pose. Data for FP{fp_session}?',font=("Helvetica 8"))
        self.fp_session_override_label.grid(row=5,column=0,sticky='w')
        self.fp_override = IntVar()
        self.fp_override.set(1)
        self.fp_session_override = Checkbutton(self.positions_mframe, text="Yes", onvalue=1, offvalue=0, variable=self.fp_override, command=self.pos_override)
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

    def get_drivers(self,team):
        try:
            self.driver_label1.grid_remove()
            self.driver_val1.grid_remove()
            self.driver_label2.grid_remove()
            self.driver_val2.grid_remove()
            self.enter_driver_pos.grid_remove()
        except:
            pass
        self.curr_team = team.lower()
        drivers = [driver.capitalize() for driver in self.out_dict['current_week'][self.curr_team]]
        self.driver1 = drivers[0].lower()
        self.driver2 = drivers[1].lower()
        self.driver_label1 = Label(self.positions_mframe, text=f"Enter Position for {drivers[0]}",font=("Helvetica 8"))
        self.driver_label1.grid(row=7,column=0,sticky='w')
        self.driver_val1 = Entry(self.positions_mframe, width=5)
        self.driver_val1.grid(row=7,column=2,sticky='w')
        self.driver_label2 = Label(self.positions_mframe, text=f"Enter Position for {drivers[1]}",font=("Helvetica 8"))
        self.driver_label2.grid(row=8,column=0,sticky='w')
        self.driver_val2 = Entry(self.positions_mframe, width=5)
        self.driver_val2.grid(row=8,column=2,sticky='w')
        self.enter_driver_pos = Button(self.positions_mframe,text="Enter",command=self.set_driver_info)
        self.enter_driver_pos.grid(row=8,column=2,sticky='e')
    
    def set_driver_info(self):
        pos1 = self.driver_val1.get()
        pos2 = self.driver_val2.get()
        self.count+=1
        try:
            pos_num1 = int(pos1)
            pos_num2 = int(pos2)
            assert(20 >= pos_num1 > 0 )
            assert(20 >= pos_num2 > 0 )
        except: 
            raise ValueError("Enter a number between 1 and 20.")
        self.out_dict['current_week'][self.curr_team][self.driver1] = pos_num1
        self.out_dict['current_week'][self.curr_team][self.driver2] = pos_num2
        if self.count==1:
            self.create_pos_yaml_file = Button(self.positions_mframe,text="Create Inputs",command=self.create_positions_yaml)
            self.create_pos_yaml_file.grid(row=9,column=2,sticky='e')
    
    def create_positions_yaml(self):
        with open('test.yaml',"w") as file:
            yaml.dump(self.out_dict, file, indent=2)

    def price_override(self):
        constructor_override = self.constructor_price_override.get()
        driver_override = self.driver_price_override.get()
    
    def get_price_info(self,team):
        self.price_team = team.lower()
        print(self.price_team)

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
        img = ImageTk.PhotoImage(Image.open(self.image).resize((self.width,self.height-300),Image.ADAPTIVE))
        self.count = 0
        self.notes = ttk.Notebook(self.root)
        self.notes.grid(row=0,column=0,sticky='nsew')
        self.positions_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.positions_mframe, text='Positions')
        self.gui_title1 = Label(self.positions_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title1.grid(row=10,column=0,columnspan=4,sticky='nsew')
        lbl_1 = Label(self.positions_mframe,image=img)
        lbl_1.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.positions_label1 = Label(self.positions_mframe, text='Current Week Positions\nDrivers and Constructors',anchor='center',font=("Helvetica 12"))
        self.positions_label1.grid(row=1,column=0,columnspan=4,sticky='nsew')
        self.line1 = ttk.Separator(self.positions_mframe).grid(row=2,column=0,columnspan=4,sticky='nsew')
        self.line2 = ttk.Separator(self.positions_mframe).grid(row=2,column=1,rowspan=5,sticky='nsew')
        self.positions_mframe.grid_rowconfigure(0, weight=1)
        self.positions_mframe.grid_rowconfigure(1, weight=1)
        self.positions_mframe.grid_rowconfigure(2, weight=1)
        self.positions_mframe.grid_rowconfigure(3, weight=1)
        self.positions_mframe.grid_rowconfigure(4, weight=1)
        self.positions_mframe.grid_rowconfigure(5, weight=1)
        self.positions_mframe.grid_rowconfigure(6, weight=1)
        self.positions_mframe.grid_rowconfigure(7, weight=1)
        self.positions_mframe.grid_rowconfigure(8, weight=1)
        self.positions_mframe.grid_rowconfigure(9, weight=1)
        self.positions_mframe.grid_rowconfigure(10, weight=1)
        self.positions_mframe.grid_columnconfigure(0, weight=1)
        self.positions_mframe.grid_columnconfigure(1, weight=1)
        self.positions_mframe.grid_columnconfigure(2, weight=1)
        self.sessions_label = Label(self.positions_mframe, text='Session Type: ',font=("Helvetica 8"))
        self.sessions_label.grid(row=3,column=0,sticky='w')
        self.session_var = StringVar(self.positions_mframe)
        self.session_var.set("Select Option")
        self.sessions_menu = OptionMenu(self.positions_mframe, self.session_var, *self.sessions, command=self.get_session)
        self.sessions_menu.grid(row=3,column=2,sticky='w')
        self.constructors_label = Label(self.positions_mframe, text='Select Constructor: ',font=("Helvetica 8"))
        self.constructors_label.grid(row=6,column=0,sticky='w')
        self.constructor_var = StringVar(self.positions_mframe)
        self.constructor_var.set("Select Option")
        self.constructors_menu = OptionMenu(self.positions_mframe, self.constructor_var, *self.constructor_names, command=self.get_drivers)
        self.constructors_menu.grid(row=6,column=2,sticky='w')

        
        self.prices_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.prices_mframe, text='Prices')
        lbl_2 = Label(self.prices_mframe,image=img)
        lbl_2.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.prices_label1 = Label(self.prices_mframe, text='Current Week Prices\nDrivers and Constructors',anchor='center',font=("Helvetica 12"))
        self.prices_label1.grid(row=1,column=0,columnspan=4,sticky='nsew')
        self.line3 = ttk.Separator(self.prices_mframe).grid(row=2,column=0,columnspan=4,sticky='nsew')
        self.line4 = ttk.Separator(self.prices_mframe).grid(row=2,column=1,rowspan=5,sticky='nsew')
        self.prices_mframe.grid_rowconfigure(0, weight=1)
        self.prices_mframe.grid_rowconfigure(1, weight=1)
        self.prices_mframe.grid_rowconfigure(2, weight=1)
        self.prices_mframe.grid_rowconfigure(3, weight=1)
        self.prices_mframe.grid_rowconfigure(4, weight=1)
        self.prices_mframe.grid_rowconfigure(5, weight=1)
        self.prices_mframe.grid_rowconfigure(6, weight=1)
        self.prices_mframe.grid_rowconfigure(7, weight=1)
        self.prices_mframe.grid_rowconfigure(8, weight=1)
        self.prices_mframe.grid_rowconfigure(9, weight=1)
        self.prices_mframe.grid_rowconfigure(10, weight=1)
        self.prices_mframe.grid_columnconfigure(0, weight=1)
        self.prices_mframe.grid_columnconfigure(1, weight=1)
        self.prices_mframe.grid_columnconfigure(2, weight=1)
        self.budget = Label(self.prices_mframe, text=f"Team Budget (millions)",font=("Helvetica 8"))
        self.budget.grid(row=3,column=0,sticky='w')
        self.budget_val = Entry(self.prices_mframe, width=10)
        self.budget_val.grid(row=3,column=2,sticky='w')
        self.constructor_price_override_label = Label(self.prices_mframe, text=f'Override Constructor Price Data?',font=("Helvetica 8"))
        self.constructor_price_override_label.grid(row=4,column=0,sticky='w')    
        self.constructor_price_override = IntVar()
        self.constructor_price_override.set(1)
        self.constructor_price_override_input = Checkbutton(self.prices_mframe, text="Yes", onvalue=1, offvalue=0, variable=self.constructor_price_override)
        self.constructor_price_override_input.grid(row=4,column=2,sticky='w')
        self.driver_price_override_label = Label(self.prices_mframe, text=f'Override Driver Price Data?',font=("Helvetica 8"))
        self.driver_price_override_label.grid(row=5,column=0,sticky='w')    
        self.driver_price_override = IntVar()
        self.driver_price_override.set(1)
        self.driver_price_override_input = Checkbutton(self.prices_mframe, text="Yes", onvalue=1, offvalue=0, variable=self.driver_price_override, command=self.price_override)
        self.driver_price_override_input.grid(row=5,column=2,sticky='w')
        self.constructors_price_label = Label(self.prices_mframe, text='Select Constructor: ',font=("Helvetica 8"))
        self.constructors_price_label.grid(row=6,column=0,sticky='w')
        self.constructor_price_name = StringVar(self.prices_mframe)
        self.constructor_price_name.set("Select Option")
        self.constructors_price_menu = OptionMenu(self.prices_mframe, self.constructor_price_name, *self.constructor_names, command=self.get_price_info)
        self.constructors_price_menu.grid(row=6,column=2,sticky='w')


        self.gui_title2 = Label(self.prices_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title2.grid(row=10,column=0,columnspan=4,sticky='nsew')

        self.ga_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.ga_mframe, text='GA Inputs')
        lbl_3 = Label(self.ga_mframe,image=img)
        lbl_3.grid(row=0,column=0,columnspan=4,sticky='nsew')
        self.ga_mframe1 = Label(self.ga_mframe, text='Current Week GA Inputs\nParameters for Optimizations',anchor='center',font=("Helvetica 12"))
        self.ga_mframe1.grid(row=1,column=0,columnspan=4,sticky='nsew')
        self.line5 = ttk.Separator(self.ga_mframe).grid(row=2,column=0,columnspan=4,sticky='nsew')
        self.line6 = ttk.Separator(self.ga_mframe).grid(row=2,column=1,rowspan=5,sticky='nsew')
        self.gui_title3 = Label(self.ga_mframe, text=f"GA-Powered F1 Fantasy",anchor='center',font=("Helvetica 12"))
        self.gui_title3.grid(row=10,column=0,columnspan=4,sticky='nsew')

        self.root.mainloop()
if __name__ == "__main__":
    class_init = postdata_gui()
    class_init.main()