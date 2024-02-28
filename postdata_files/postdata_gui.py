from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import postdata_positions as pd_pos
from PIL import Image, ImageTk
import yaml

class postdata_gui:
    def __init__(self):
        self.yaml_gen = pd_pos.generate_positions_yaml()
        self.full_team_data,self.out_dict = self.yaml_gen.initialize_yaml_file()
        self.sessions, self.constructor_names = self.yaml_gen.main()
        self.fp_sessions_nums = ['1','2','3']
        self.overrides = ['fp_override','quali_override','race_override']
        self.image = "./picture_files/F1_logo.png"
        self.width = 300
        self.height = 300

    def get_session(self,event):
        if event == 'fp':
            self.fp_session_num 

    def get_drivers(self,team):
        team = self.constructor_var.get()
        self.curr_team = team.lower()
        drivers = [driver.capitalize() for driver in self.out_dict['current_week'][self.curr_team]]
        self.drivers_label = Label(self.positions_mframe, text='Select Driver: ',font=("Helvetica 8"))
        self.drivers_label.grid(row=5,column=0,sticky='w')
        self.driver_var = StringVar(self.positions_mframe)
        self.driver_var.set("Select Option")
        self.drivers_menu = OptionMenu(self.positions_mframe, self.driver_var, *drivers, command=self.get_driver_info)
        self.drivers_menu.grid(row=5,column=2,sticky='w')
    
    def get_driver_info(self,driver):
        driver = self.driver_var.get()
        self.curr_driver = driver.lower()
        self.drivers_label = Label(self.positions_mframe, text=f'Enter Position for {driver}: ',font=("Helvetica 8"))
        self.drivers_label.grid(row=6,column=0,sticky='w')
        self.driver_pos_info = Entry(self.positions_mframe, width=5)
        self.driver_pos_info.grid(row=6,column=2,sticky='w')
        self.enter_driver_pos = Button(self.positions_mframe,text="Enter",command=self.set_driver_info)
        self.enter_driver_pos.grid(row=6,column=2,sticky='e')
    
    def set_driver_info(self):
        pos = self.driver_pos_info.get()
        self.count+=1
        try:
            pos_num = int(pos)
        except: 
            raise ValueError("Enter a number between 1 and 20.")
        self.out_dict['current_week'][self.curr_team][self.curr_driver] = pos_num
        if self.count==3:
            self.create_pos_yaml_file = Button(self.positions_mframe,text="Create Inputs",command=self.create_positions_yaml)
            self.create_pos_yaml_file.grid(row=7,column=2,sticky='e')
    
    def create_positions_yaml(self):
        with open('test.yaml',"w") as file:
            yaml.dump(self.out_dict, file, indent=2)

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
        img = ImageTk.PhotoImage(Image.open(self.image).resize((self.width,self.height-200),Image.ADAPTIVE))
        self.count = 0
        self.notes = ttk.Notebook(self.root)
        self.notes.grid(row=0,column=0,sticky='nsew')
        self.positions_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.positions_mframe, text='Positions')
        self.positions_label1 = Label(self.positions_mframe, text='Current Week Positions\nDrivers and Constructors',anchor='center',font=("Helvetica 12"))
        lbl = Label(self.positions_mframe,image=img)
        lbl.grid(row=0,column=0,columnspan=4,sticky='nsew')
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
        self.positions_mframe.grid_columnconfigure(0, weight=1)
        self.positions_mframe.grid_columnconfigure(1, weight=1)
        self.positions_mframe.grid_columnconfigure(2, weight=1)
        self.positions_mframe.grid_columnconfigure(3, weight=1)
        self.sessions_label = Label(self.positions_mframe, text='Session Type: ',font=("Helvetica 8"))
        self.sessions_label.grid(row=3,column=0,sticky='w')
        self.session_var = StringVar(self.positions_mframe)
        self.session_var.set("Select Option")
        self.sessions_menu = OptionMenu(self.positions_mframe, self.session_var, *self.sessions, command=self.get_session)
        self.sessions_menu.grid(row=3,column=2,sticky='w')
        self.constructors_label = Label(self.positions_mframe, text='Select Constructor: ',font=("Helvetica 8"))
        self.constructors_label.grid(row=4,column=0,sticky='w')
        self.constructor_var = StringVar(self.positions_mframe)
        self.constructor_var.set("Select Option")
        self.constructors_menu = OptionMenu(self.positions_mframe, self.constructor_var, *self.constructor_names, command=self.get_drivers)
        self.constructors_menu.grid(row=4,column=2,sticky='w')

        # self.positions_sframe1 = ttk.Frame(self.positions_mframe,borderwidth=2,relief='sunken')
        # self.positions_sframe1.grid(row=2,column=0,sticky='nsew')

        # self.prices_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        # self.notes.add(self.prices_mframe, text='Prices')

        # self.inputs_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        # self.notes.add(self.inputs_mframe, text='GA Inputs')

        self.root.mainloop()
if __name__ == "__main__":
    class_init = postdata_gui()
    class_init.main()