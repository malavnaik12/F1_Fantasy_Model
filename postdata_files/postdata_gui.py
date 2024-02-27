from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import postdata_positions as pd_pos
from PIL import Image, ImageTk

class postdata_gui:
    def __init__(self):
        self.yaml_gen = pd_pos.generate_positions_yaml()
        self.sessions, self.constructor_names = self.yaml_gen.main()
        self.fp_sessions_nums = ['1','2','3']
        self.overrides = ['fp_override','quali_override','race_override']
        self.image = "./picture_files/F1_logo.png"
        self.width = 375
        self.height = 400

    def main(self):
        self.root = Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("GA-Powered F1 Fantasy")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(row=0,column=0,sticky='nsew')
        # self.style = ttk.Style(self.root)
        # self.style.theme_use('winnative')
        # self.root.configure(bg='black')
        self.root.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        img = ImageTk.PhotoImage(Image.open(self.image).resize((self.width,self.height-200),Image.ADAPTIVE))

        self.notes = ttk.Notebook(self.root)
        self.notes.grid(row=0,column=0,sticky='nsew')
        self.positions_mframe = ttk.Frame(self.notes,borderwidth=2,relief='sunken')
        self.notes.add(self.positions_mframe, text='Positions')
        self.positions_label1 = Label(self.positions_mframe, text='Current Week Positions: Drivers and Constructors',anchor='center',font=("Helvetica 12"))
        lbl = Label(self.positions_mframe,image=img)
        lbl.grid(row=0,column=0,columnspan=3,sticky='nsew')
        self.positions_label1.grid(row=1,column=0,columnspan=3,sticky='nsew')
        self.line1 = ttk.Separator(self.positions_mframe).grid(row=2,column=0,columnspan=3,sticky='nsew')
        self.line2 = ttk.Separator(self.positions_mframe).grid(row=2,column=1,rowspan=2,sticky='nsew')
        self.positions_mframe.grid_rowconfigure(0, weight=1)
        self.positions_mframe.grid_rowconfigure(1, weight=1)
        self.positions_mframe.grid_rowconfigure(2, weight=1)
        self.positions_mframe.grid_rowconfigure(3, weight=1)
        self.positions_mframe.grid_rowconfigure(4, weight=1)
        self.positions_mframe.grid_columnconfigure(0, weight=1)
        self.positions_mframe.grid_columnconfigure(1, weight=1)
        self.positions_mframe.grid_columnconfigure(2, weight=1)
        self.sessions_label = Label(self.positions_mframe, text='Session Type: ',font=("Helvetica 8"))
        self.sessions_label.grid(row=3,column=0,sticky='w')
        session_var = StringVar(self.positions_mframe)
        session_var.set("Select Option")
        self.sessions_menu = OptionMenu(self.positions_mframe, session_var, *self.sessions)
        self.sessions_menu.grid(row=3,column=2,sticky='w')
        self.constructors_label = Label(self.positions_mframe, text='Select Constructor: ',font=("Helvetica 8"))
        self.constructors_label.grid(row=4,column=0,sticky='w')
        constructor_var = StringVar(self.positions_mframe)
        constructor_var.set("Select Option")
        self.constructors_menu = OptionMenu(self.positions_mframe, constructor_var, *self.constructor_names)
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