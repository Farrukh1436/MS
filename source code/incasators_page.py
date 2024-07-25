import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
import sqlite3
from tkinter import messagebox
from tkinter import simpledialog
import images as ic

class CustomDialog(simpledialog._QueryString):
    def body(self, master):
        tk.Label(master, text=self.prompt, justify=tk.LEFT).grid(row=0, padx=5, sticky='w')
        self.entry = tk.Entry(master, width=50)  # Set the desired width here
        self.entry.grid(row=1, padx=5, sticky='we')
        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, ctk.END)
        return self.entry

def ask_string(title, prompt, **kwargs):
    d = CustomDialog(title, prompt, **kwargs)
    return d.result



class InterActiveButton(ctk.CTkButton):
    def __init__(self, master, max_expansion: int = 12, bg='dark blue', fg='#dad122', **kwargs):
        self.max_expansion = max_expansion
        self.bg = bg
        self.fg = fg

        button_args = dict(fg_color=bg, text_color=fg, corner_radius=10, font=("Arial", 18, "bold"), 
                           height=50, hover_color=fg)
        button_args.update(kwargs)
        super().__init__(master, **button_args)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

        self.base_width = kwargs.get("width", 200)
        self.width = self.base_width
        self.mode = None

    def increase_width(self):
        if self.width <= self.base_width + self.max_expansion:
            if self.mode == "increasing":
                self.width += 1
                self.configure(width=self.width)
                self.after(5, self.increase_width)

    def decrease_width(self):
        if self.width > self.base_width:
            if self.mode == "decreasing":
                self.width -= 1
                self.configure(width=self.width)
                self.after(5, self.decrease_width)

    def on_hover(self, event=None):
        self.mode = "increasing"
        self.configure(fg_color=self.fg, text_color=self.bg)
        self.after(5, self.increase_width)

    def on_leave(self, event=None):
        self.mode = "decreasing"
        self.configure(fg_color=self.bg, text_color=self.fg)
        self.after(5, self.decrease_width)


class IncasatorsPage(ctk.CTkFrame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller
        self.db_connection = self.controller.db_connection
        self.configure(fg_color='#020f12')
        self.create_widgets()

    def create_widgets(self):
        
       
        self.home_button = ctk.CTkButton(self, image=ic.iconik("home",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#ECF0F1',
                                         text_color='#3498DB',hover_color='#ECF0F1',font=("Arial",16,'bold'),
                                            text="Home", command=self.go_home)
        self.home_button.place(relx=0.5, rely=0.05, anchor="center")  # Position the button below the image

        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()
        
        self.regions = ["Andijon viloyati","Buxoro viloyati","Fargʻona viloyati",
                        "Jizzax viloyati","Qashqadaryo viloyati","Xorazm viloyati",
                        "Namangan viloyati","Navoiy viloyati","Samarqand viloyati",
                        "Surxondaryo viloyati","Sirdaryo viloyati","Toshkent viloyati",
                        "Qoraqalpogʻiston Respublikasi","Toshkent shahri"]
         # Calculate the number of rows and columns
        num_buttons = len(self.regions)
        num_cols = 4
        num_rows = (num_buttons + num_cols - 1) // num_cols  # Integer division with ceiling

        # Create buttons for each region
        for i, region in enumerate(self.regions):
            col_index = i % num_cols  # Column index based on button position
            row_index = i // num_cols  # Row index based on button position

            button_width = 300  # Adjust width as needed
            button_height = 50  # Adjust height as needed

            # Calculate button position with spacing
            x_pos = screen_width * 0.1 + col_index * (button_width + 40)  # Add spacing between buttons
            y_pos = screen_height * 0.08 + row_index * (button_height + 90)

            button = InterActiveButton(self, text=region, width=button_width, height=button_height, command=lambda r=region: self.open_incasators_window(r))

            button.place(x=x_pos, y=y_pos) 
        

        dev_label1 =  ctk.CTkLabel(self, text="Developer:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        dev_label1.place(relx=0.02,rely=0.8)
        dev_label =  ctk.CTkLabel(self, text="F.Sattorov", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        dev_label.place(relx=0.115,rely=0.8)
        eng_label1 =  ctk.CTkLabel(self, text="Engineer:\nAsistant:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        eng_label1.place(relx=0.8,rely=0.8)
        eng_label =  ctk.CTkLabel(self, text="E.Sattorov\nShozod", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        eng_label.place(relx=0.9,rely=0.8)
            
    def open_incasators_window(self, region):
        IncasatorsWindow(self.controller, region)

    def go_home(self):
        self.controller.show_frame("HomePage")


class IncasatorsWindow(ctk.CTkToplevel):
    def __init__(self, controller, region):
        super().__init__()

        self.controller = controller
        self.region = region
        self.title("Incasators Management")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.configure(fg_color='#020f12')
        self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
      
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "../database/database.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()



      


        # Button to add a new incasator
        self.add_button = ctk.CTkButton(self, image=ic.iconik("add",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#00FF00',
                                         text_color='#800080',hover_color='#00FF00',font=("Arial",16,'bold'),
                                          text="Add New Incasator", command=self.add_new_incasator)
        self.add_button.pack(pady=10)
        self.back_button = ctk.CTkButton(self,image=ic.iconik("back",32), bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#00FFFF',
                                         text_color='#DE3163',hover_color='#00FFFF',font=("Arial",16,'bold'),
                                         text="Back", command=self.on_close)
        self.back_button.place(relx=0.9, rely=0.01)
        # Create the CTkTabview
        self.tab_view = ctk.CTkTabview(self, fg_color='#020f12')
        self.tab_view.pack(expand=1, fill="both")

        self.refresh_tabs()
        # Bring window to the top and focus it
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(0, lambda: self.attributes('-topmost', False))

        # Bind the close event to handle window close properly
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.conn.close()
        self.destroy()

    def refresh_tabs(self):
        # Clear all existing tabs
        for tab_name in self.tab_view._tab_dict:
            self.tab_view.delete(tab_name)
    
        # Reload incasators from the database
        self.load_incasators()

    def load_incasators(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Incasators WHERE Region=?", (self.region,))
        incasators = cursor.fetchall()
    
        for incasator in incasators:
            self.create_incasator_tab(incasator)


    def create_incasator_tab(self, incasator):
        base_name = f"{incasator[2]}"
        tab_name = base_name
    
        counter = 1
        while tab_name in self.tab_view._tab_dict:
            tab_name = f"{base_name}_{counter}"
            counter += 1
    
        frame = self.tab_view.add(tab_name)
        self.tab_view._tab_dict[tab_name] = frame
        self.tab_view._name_list.append(tab_name)
    
        scrollable_frame = ctk.CTkScrollableFrame(frame, fg_color='#020f12')
        scrollable_frame.pack(fill="both", expand=True)
    
        self.fields = ["Incasator", "Kiosks_n", "MEI_n", "ICT_n", "NV_n", "CASHCODE_n", "CUSTOM1_n", "CUSTOM2_n", "MASON_n",
                       "Touchscreen_n", "Display_n", "DDR3_n", "Modem_n", "Simcard_n", "BA_board_n", "motherboard_n",
                       "comport_board_n", "power_supply_n", "paper_n"]
    
        label_r = ctk.CTkLabel(scrollable_frame, text="Region:" + str(self.region),
                               text_color='white', fg_color='#020f12', font=("Arial", 20, 'bold'))
        label_r.pack(fill="x", pady=5)
        
       
    
        self.name_var = ctk.StringVar(value=incasator[2])
        self.kiosks_var = ctk.StringVar(value=incasator[3])
        self.mei_var = ctk.StringVar(value=incasator[4])
        self.ict_var = ctk.StringVar(value=incasator[5])
        self.nv_var = ctk.StringVar(value=incasator[6])
        self.cc_var = ctk.StringVar(value=incasator[7])
        self.c1_var = ctk.StringVar(value=incasator[8])
        self.c2_var = ctk.StringVar(value=incasator[9])
        self.mason_var = ctk.StringVar(value=incasator[10])
        self.ts_var = ctk.StringVar(value=incasator[11])
        self.display_var = ctk.StringVar(value=incasator[12])
        self.ddr3_var = ctk.StringVar(value=incasator[13])
        self.modem_var = ctk.StringVar(value=incasator[14])
        self.simcard_var = ctk.StringVar(value=incasator[15])
        self.ba_board_var = ctk.StringVar(value=incasator[16])
        self.motherboard_var = ctk.StringVar(value=incasator[17])
        self.c_board_var = ctk.StringVar(value=incasator[18])
        self.ps_var = ctk.StringVar(value=incasator[19])
        self.paper_var = ctk.StringVar(value=incasator[20])

        # Create a dictionary to store the entry widgets for this tab
        self.entries = {}
    
        # Create labels and entries dynamically
        labels_text = [
            ("Incasator name:", self.name_var, incasator[2]),
            ("Kiosklar soni:", self.kiosks_var, incasator[3]),
            ("MEIlar soni:", self.mei_var, incasator[4]),
            ("ICTlar soni:", self.ict_var, incasator[5]),
            ("NVlar soni:", self.nv_var, incasator[6]),
            ("Cashcodelar soni:", self.cc_var, incasator[7]),
            ("Custom1 lar soni:", self.c1_var, incasator[8]),
            ("Custom2 lar soni:", self.c2_var, incasator[9]),
            ("Masonlar soni:", self.mason_var, incasator[10]),
            ("TouchScreenlar soni:", self.ts_var, incasator[11]),
            ("Displaylar soni:", self.display_var, incasator[12]),
            ("DDR3lar soni:", self.ddr3_var, incasator[13]),
            ("Modemlar soni:", self.modem_var, incasator[14]),
            ("Simcardlar soni:", self.simcard_var, incasator[15]),
            ("Pul Aparat platalar soni:", self.ba_board_var, incasator[16]),
            ("Moterinsiy platalar soni:", self.motherboard_var, incasator[17]),
            ("Comport platalar soni:", self.c_board_var, incasator[18]),
            ("Blok pitanyalar soni:", self.ps_var, incasator[19]),
            ("Qog'ozlar soni:", self.paper_var, incasator[20])
        ]
    
        for label_text, var, value in labels_text:
            label = ctk.CTkLabel(scrollable_frame, text=label_text, text_color='white', fg_color='#020f12')
            label.pack(pady=5)
            entry = ctk.CTkEntry(scrollable_frame, fg_color='#020f12', textvariable=var)
            entry.pack(pady=5)
            var.set(value)
            # Store the entry widget in the dictionary
            self.entries[label_text] = entry
    
        # Store the entries dictionary in a way that associates it with the tab name
        if not hasattr(self, 'tab_entries'):
            self.tab_entries = {}
        self.tab_entries[tab_name] = self.entries
        


        save_button = ctk.CTkButton(scrollable_frame,image=ic.iconik("save",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#dad122',
                                         text_color='#DE3163',hover_color='#dad122',font=("Arial",16,'bold'),
                                          text="Save",
                                            command=lambda: self.save_incasator(tab_name,incasator[0]))
        save_button.place(rely=0.95,relx=0.01,anchor="sw")
    
        delete_button = ctk.CTkButton(scrollable_frame,image=ic.iconik("delete",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#DC143C',
                                         text_color='white',hover_color='#DC143C',font=("Arial",16,'bold'),
                                           text="Delete Incasator", command=lambda: self.delete_incasator(tab_name, int(incasator[0])))
        delete_button.place(rely=0.95,relx=0.85,anchor="sw")

    def delete_incasator(self, tab_name, incasator_id):
        try:
            # Debug: Print the type and value of incasator_id
            print(f"Type of incasator_id: {type(incasator_id)}, Value: {incasator_id}")
    
            # Ensure incasator_id is an integer
            if isinstance(incasator_id, int):
                # Correctly format incasator_id as a tuple with one element
                self.cursor.execute("DELETE FROM incasators WHERE id=?", (incasator_id,))
                self.conn.commit()
    
                # Debug: Print all tab names
                print(f"Available tab names: {list(self.tab_view._tab_dict.keys())}")
    
                # Delete the specific tab
                if tab_name in self.tab_view._tab_dict:
                    self.tab_view.delete(tab_name)
                    print(f"Deleted tab: {tab_name}")
                else:
                    print(f"Error: Tab {tab_name} not found")
    
                # Refresh tabs to update the view
                
            else:
                print("Error: incasator_id should be an integer.")
        except KeyError as e:
            print(f"KeyError: {e}. Possible issue with accessing or modifying the tab dictionary.")
        except Exception as e:
            print(f"Error in delete_incasator: {e}")
        self.on_close()
        IncasatorsWindow(self.controller, self.region)


   
            
            
            
            
    def show_error(self):
        error_label = ctk.CTkLabel(self, text="Error: Kiosk data not found.", fg="red")
        error_label.pack(pady=20)
        self.back_button = ctk.CTkButton(self, text="Back", command=self.on_close)
        self.back_button.pack(pady=10)        
            
            

    def add_new_incasator(self):
        new_incasator_name = ask_string("Input", "Please enter the new Incasator's name:", parent=self)
        
        next_id = self.get_next_incasator_id()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO incasators (
                id, Region, Incasator, Kiosks_n, MEI_n, ICT_n, NV_n, CASHCODE_n, CUSTOM1_n, CUSTOM2_n,
                MASON_n, Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n,
                comport_board_n, power_supply_n, paper_n
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (next_id, self.region, new_incasator_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.conn.commit()
        new_incasator = (next_id, self.region, new_incasator_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.create_incasator_tab(new_incasator)



    def get_next_incasator_id(self):
        self.cursor.execute("SELECT MAX(id) FROM incasators")
        max_id = self.cursor.fetchone()[0]
        return (max_id + 1) if max_id else 1

    def save_incasator(self, tab_name,incasator_id):
        try:
             # Retrieve data from the entry fields
            incasator_name = self.tab_entries[tab_name]['Incasator name:'].get()
            kiosks_n = int(self.tab_entries[tab_name]['Kiosklar soni:'].get())
            mei_n = int(self.tab_entries[tab_name]['MEIlar soni:'].get())
            ict_n = int(self.tab_entries[tab_name]['ICTlar soni:'].get())
            nv_n = int(self.tab_entries[tab_name]['NVlar soni:'].get())
            cashcode_n = int(self.tab_entries[tab_name]['Cashcodelar soni:'].get())
            custom1_n = int(self.tab_entries[tab_name]['Custom1 lar soni:'].get())
            custom2_n = int(self.tab_entries[tab_name]['Custom2 lar soni:'].get())
            mason_n = int(self.tab_entries[tab_name]['Masonlar soni:'].get())
            touchscreen_n = int(self.tab_entries[tab_name]['TouchScreenlar soni:'].get())
            display_n = int(self.tab_entries[tab_name]['Displaylar soni:'].get())
            ddr3_n = int(self.tab_entries[tab_name]['DDR3lar soni:'].get())
            modem_n = int(self.tab_entries[tab_name]['Modemlar soni:'].get())
            simcard_n = int(self.tab_entries[tab_name]['Simcardlar soni:'].get())
            ba_board_n = int(self.tab_entries[tab_name]['Pul Aparat platalar soni:'].get())
            motherboard_n = int(self.tab_entries[tab_name]['Moterinsiy platalar soni:'].get())
            comport_board_n = int(self.tab_entries[tab_name]['Comport platalar soni:'].get())
            power_supply_n = int(self.tab_entries[tab_name]['Blok pitanyalar soni:'].get())
            paper_n = int(self.tab_entries[tab_name]["Qog'ozlar soni:"].get())

            # Update the database
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE incasators
                SET Region=?,Incasator=?, kiosks_n=?, mei_n=?, ict_n=?, nv_n=?, cashcode_n=?, custom1_n=?, custom2_n=?, mason_n=?, touchscreen_n=?, display_n=?, ddr3_n=?, modem_n=?, simcard_n=?, ba_board_n=?, motherboard_n=?, comport_board_n=?, power_supply_n=?, paper_n=?
                WHERE id=?
            ''', (self.region,incasator_name, kiosks_n, mei_n, ict_n, nv_n, cashcode_n, custom1_n, custom2_n, mason_n, touchscreen_n, display_n, ddr3_n, modem_n, simcard_n, ba_board_n, motherboard_n, comport_board_n, power_supply_n, paper_n, incasator_id))
            self.conn.commit()

            #messagebox.showinfo("Success", "Incasator details saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the incasator: {e}")

        new_name = incasator_name
        # Debug: Print all tab names
        print(f"{self.tab_entries[tab_name]['Kiosklar soni:'].get()}")
        print(f"Available tab names: {list(self.tab_view._tab_dict.keys())}")
        print(f"New name for tab: {new_name} {self.tab_entries[tab_name]['Kiosklar soni:'].get()}")
        try:
            if tab_name in self.tab_view._tab_dict:
                if new_name != tab_name:  # Check if the new name is different
                    try:
                        self.tab_view.rename(old_name=tab_name, new_name=new_name)
                    except ValueError as e:
                        print(f"aa:{e}")
        except Exception as e:
            print(f"bb:{e}")
        self.on_close()
        IncasatorsWindow(self.controller, self.region)


class CTkTabview(ctk.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name_list = []
        self._tab_dict = {}
    def delete(self, name):
        try:
            if name in self._name_list:
                self._name_list.remove(name)
            if name in self._tab_dict:
                tab_widget = self._tab_dict.pop(name)
                tab_widget.grid_forget()
        except Exception as e:
            print(f"Error in delete: {e}")

    def refresh_tabs(self):
        try:
            for name in self._name_list:
                tab_widget = self._tab_dict.get(name)
                if tab_widget:
                    tab_widget.grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            print(f"Error in refresh_tabs: {e}")

    def rename(self, old_name, new_name):
        try:
            if old_name not in self._name_list:
                raise ValueError(f"old_name '{old_name}' does not exist")
            if new_name in self._name_list:
                raise ValueError(f"new_name '{new_name}' already exists")

            # Rename in _name_list
            index = self._name_list.index(old_name)
            self._name_list[index] = new_name

            # Rename in _tab_dict
            self._tab_dict[new_name] = self._tab_dict.pop(old_name)
            self._tab_dict[new_name].grid_forget()

            self.refresh_tabs()
        except Exception as e:
            print(f"Error in rename: {e}")



    






if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Incasators")
    app.screen_width = app.winfo_screenwidth()
    app.screen_height = app.winfo_screenheight()
    app.geometry(f"{app.screen_width}x{app.screen_height}+0+0")

    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    app.frames = {}
    for F in (IncasatorsPage,):
        page_name = F.__name__
        frame = F(master=container, controller=app)
        app.frames[page_name] = frame
        frame.pack(fill="both", expand=True)

    app.mainloop() 