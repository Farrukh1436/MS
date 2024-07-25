# kiosks_page.py
import customtkinter as ctk
import sqlite3

import images as ic

class KiosksPage(ctk.CTkFrame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller
        self.db_connection = self.controller.db_connection
        self.configure(fg_color='#020f12')
        self.create_widgets()
        self.refresh_buttons()

    def create_widgets(self):
        


        self.home_button = ctk.CTkButton(self, image=ic.iconik("home",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#ECF0F1',
                                         text_color='#3498DB',hover_color='#ECF0F1',font=("Arial",16,'bold'),
                                            text="Home", command=self.go_home)
        self.home_button.place(relx=0.95, rely=0.02, anchor="center")  # Position the button below the image


        self.new_kiosk_button = ctk.CTkButton(self,image=ic.iconik("add",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#00FF00',
                                         text_color='#800080',hover_color='#00FF00',font=("Arial",16,'bold'),
                                          text="Add New Kiosk", command=self.add_new_kiosk)
        self.new_kiosk_button.pack(pady=10)

        self.delete_kiosk_button = ctk.CTkButton(self,image=ic.iconik("delete",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#DC143C',
                                         text_color='white',hover_color='#DC143C',font=("Arial",16,'bold'),
                                          text="Delete Selected Kiosks", command=self.delete_selected_kiosks)
        self.delete_kiosk_button.pack(pady=10)

        # Search entry and button
        self.search_frame = ctk.CTkFrame(self,fg_color="#020f12")
        self.search_frame.pack(pady=10)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Enter Kiosk ID")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", self.s_kiosk)

        self.search_button = ctk.CTkButton(self.search_frame,image=ic.iconik("search",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#5DADE2',
                                         text_color='white',hover_color='#5DADE2',font=("Arial",16,'bold'),
                                           text="Search", command=self.search_kiosk)
        self.search_button.pack(side="left", padx=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=780,fg_color="#020f12", height=500)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def refresh_buttons(self, search_kiosk_id=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.kiosk_checkbuttons = []

        cursor = self.db_connection.cursor()
        if search_kiosk_id:
            cursor.execute('SELECT id, Kiosk_ID FROM kiosks WHERE Kiosk_ID=?', (search_kiosk_id,))
        else:
            cursor.execute('SELECT id, Kiosk_ID FROM kiosks')
        rows = cursor.fetchall()
        for row in rows:
            kiosk_id = row[1]
            frame = ctk.CTkFrame(self.scrollable_frame,fg_color="#020f12")
            frame.pack(fill="x", padx=5, pady=5)

            button = ctk.CTkButton(frame, text=f"Kiosk {kiosk_id}", command=lambda id=kiosk_id: self.open_kiosk_window(id))
            button.pack(side="left", padx=10, pady=5)

            condition_var = ctk.IntVar(value=0)
            condition_check = ctk.CTkCheckBox(frame, text=f"Delete Kiosk {kiosk_id}", variable=condition_var)
            condition_check.pack(side="right", padx=10, pady=5)

            self.kiosk_checkbuttons.append((kiosk_id, condition_var))

    def delete_selected_kiosks(self):
        cursor = self.db_connection.cursor()
        for kiosk_id, condition_var in self.kiosk_checkbuttons:
            if condition_var.get() == 1:
                cursor.execute('DELETE FROM kiosks WHERE Kiosk_ID=?', (kiosk_id,))
        self.db_connection.commit()
        self.refresh_buttons()

    def add_new_kiosk(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO kiosks (Kiosk_ID, Region, Incasator, Bill_Aceptor, BA_condition, PRINTER, P_condition)
            VALUES (?, "Default Region", "Default Incasator", "Default Bill Acceptor", 0, "Default Printer", 0)
        ''', (self.get_next_kiosk_id(),))
        self.db_connection.commit()
        self.refresh_buttons()

    def get_next_kiosk_id(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT MAX(Kiosk_ID) FROM kiosks')
        max_id = cursor.fetchone()[0]
        return (max_id or 0) + 1

    def open_kiosk_window(self, kiosk_id):
        print(f"Opening kiosk window for Kiosk_ID: {kiosk_id}")  # Debugging statement
        KioskWindow(self, kiosk_id)

    def go_home(self):
        self.controller.show_frame("HomePage")
    def s_kiosk(self,event):
        search_kiosk_id = self.search_entry.get()
        self.refresh_buttons(search_kiosk_id)
    def search_kiosk(self):
        search_kiosk_id = self.search_entry.get()
        self.refresh_buttons(search_kiosk_id)

class KioskWindow(ctk.CTkToplevel):
    def __init__(self, parent, kiosk_id):
        super().__init__(parent)
        self.title("Kiosk Details")
        self.config(bg='#020f12')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width }x{self.screen_height}+0+0")
        self.kiosk_id = kiosk_id
        self.parent = parent
        self.db_connection = parent.controller.db_connection
        



        regions = ["Andijon viloyati","Buxoro viloyati","Farg'ona viloyati",
                        "Jizzax viloyati","Qashqadaryo viloyati","Xorazm viloyati",
                        "Namangan viloyati","Navoiy viloyati","Samarqand viloyati",
                        "Surxondaryo viloyati","Sirdaryo viloyati","Toshkent viloyati",
                        "Qoraqalpog'iston Respublikasi","Toshkent shahri"]
        bill_accaptors = ["MEI", "ICT", "NV","CashCode"]
        printers = ["Custom1", "Custom2", "MASUNG"]

        
        # Initialize widgets
        self.region_label = ctk.CTkLabel(self,font=("Helvetica", 18, "bold"), text="Region: ",bg_color='#020f12',fg_color='#020f12')
        self.region_label.pack(pady=5)
        self.region_combo = ctk.CTkComboBox (self, values=regions,width=280, 
                                             fg_color='#020f12',
                                             command=self.get_incasator,
                                             font=("Arial",15,'bold'),
        border_color="#FBAB7E", dropdown_fg_color="#0093E9")
        self.region_combo.pack(pady=5)
        
        self.incasator_label = ctk.CTkLabel(self,font=("Helvetica", 18, "bold"), text="Incasator: ",bg_color='#020f12',fg_color='#020f12')
        self.incasator_label.pack(pady=5)
        self.incasator_combo = ctk.CTkComboBox (self,width=280, fg_color='#020f12',font=("Arial",15,'bold'),
        border_color="#FBAB7E", dropdown_fg_color="#0093E9")
        self.incasator_combo.pack(pady=5)


        self.kiosk_id_label = ctk.CTkLabel(self, font=("Helvetica", 18, "bold"),text="Kiosk ID: ",fg_color='#020f12')
        self.kiosk_id_label.pack(pady=5)
        self.kiosk_id_entry = ctk.CTkEntry(self)  # Entry widget for Kiosk ID
        self.kiosk_id_entry.pack(pady=5)





        



        
       
        
        self.ba_label = ctk.CTkLabel(self, font=("Helvetica", 18, "bold"),text="Pul aparat: ",bg_color='#020f12',fg_color='#020f12')
        self.ba_label.pack(pady=5)
        self.ba_combo = ctk.CTkComboBox (self, values=bill_accaptors,width=280, fg_color='#020f12',font=("Arial",15,'bold'),
        border_color="#FBAB7E", dropdown_fg_color="#0093E9")
        self.ba_combo.pack(pady=5)

        self.ba_condition_var = ctk.IntVar()
        self.ba_condition_check = ctk.CTkCheckBox(self,font=("Helvetica", 18, "bold"), text="BA holati",bg_color='#020f12', variable=self.ba_condition_var)
        self.ba_condition_check.pack(pady=5)


        self.printer_label = ctk.CTkLabel(self,font=("Helvetica", 18, "bold"), text="Printer: ",bg_color='#020f12',fg_color='#020f12')
        self.printer_label.pack(pady=5)
        self.printer_combo = ctk.CTkComboBox (self, values=printers,width=280, fg_color='#020f12',font=("Arial",15,'bold'),
        border_color="#FBAB7E", dropdown_fg_color="#0093E9")
        self.printer_combo.pack(pady=5)



        self.p_condition_var = ctk.IntVar()
        self.p_condition_check = ctk.CTkCheckBox(self,font=("Helvetica", 18, "bold"), text="P holati",bg_color='#020f12', variable=self.p_condition_var)
        self.p_condition_check.pack(pady=5)
        

        
        
        self.save_button = ctk.CTkButton(self,image=ic.iconik("save",64),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#dad122',
                                         text_color='#DE3163',hover_color='#dad122',font=("Arial",40,'bold'),
                                         text="Save",height=75,width=300, 
                                         command=self.save_changes)
        self.save_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self,image=ic.iconik("back",64),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#00FFFF',
                                         text_color='#DE3163',hover_color='#00FFFF',font=("Arial",40,'bold'),
                                          text="Back",height=75,width=300, command=self.go_back)
        self.back_button.pack(pady=5)
        dev_label1 =  ctk.CTkLabel(self, text="Developer:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        dev_label1.place(relx=0.02,rely=0.8)
        dev_label =  ctk.CTkLabel(self, text="F.Sattorov", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        dev_label.place(relx=0.115,rely=0.8)
        eng_label1 =  ctk.CTkLabel(self, text="Engineer:\nAsistant:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        eng_label1.place(relx=0.75,rely=0.8)
        eng_label =  ctk.CTkLabel(self, text="E.Sattorov\nSh.Ro'ziyev", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        eng_label.place(relx=0.85,rely=0.8)
        # Fetch and display initial data
        self.fetch_data()

        # Bring window to the top and focus it
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(0, lambda: self.attributes('-topmost', False))

        # Bind the close event to handle window close properly
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_incasator(self, event=None):
        selected_region = self.region_combo.get()
    
        # Fetch incasators for the selected region from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT Incasator FROM incasators WHERE Region=?', (selected_region,))
        incasators = cursor.fetchall()
    
        # Clear previous values and populate with new ones
        self.incasator_combo.configure(values=[name[0] for name in incasators])
    
        if incasators:
            # If incasators exist for the selected region, populate the combobox with them
            self.incasator_combo.set(incasators[0][0])  # Set the first incasator as default
        else:
            # If no incasators exist for the selected region, set to "Default Incasator"
            self.incasator_combo.configure(values=["Default Incasator"])
            self.incasator_combo.set("Default Incasator")

    def fetch_data(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM kiosks WHERE Kiosk_ID=?', (self.kiosk_id,))
        self.kiosk_data = cursor.fetchone()
    
        if self.kiosk_data:
            # Update entry fields with fetched data
            self.kiosk_id_entry.delete(0, 'end')
            self.kiosk_id_entry.insert(0, self.kiosk_data[1])
            
            # Select the region from the fetched data
            if self.kiosk_data[2] in self.region_combo._values:
                self.region_combo.set(self.kiosk_data[2])
            else:
                self.region_combo.set("Buxoro viloyati")  # Default fallback value
    
            # Fetch and set incasators for the selected region
            self.get_incasator()
            if self.kiosk_data[3] in self.incasator_combo._values:
                self.incasator_combo.set(self.kiosk_data[3])
            else:
                self.incasator_combo.set("Default Incasator")  # Default fallback value
    
            if self.kiosk_data[4] in self.ba_combo._values:
                self.ba_combo.set(self.kiosk_data[4])
            else:
                self.ba_combo.set("MEI")  # Default fallback value
            self.ba_condition_var.set(self.kiosk_data[5])
            
            if self.kiosk_data[6] in self.printer_combo._values:
                self.printer_combo.set(self.kiosk_data[6])
            else:
                self.printer_combo.set("MASUNG")  # Default fallback value
            self.p_condition_var.set(self.kiosk_data[7])
        else:
            self.show_error()


    def save_changes(self):
        self.fetch_data
        cursor = self.db_connection.cursor()
        cursor.execute('''
            UPDATE kiosks
            SET Kiosk_ID=?, Region=?, Incasator=?, Bill_Aceptor=?, BA_condition=?, PRINTER=?, P_condition=?
            WHERE Kiosk_ID=?
        ''', (
            self.kiosk_id_entry.get(),
            self.region_combo.get(),
            self.incasator_combo.get(),
            self.ba_combo.get(),
            self.ba_condition_var.get(),
            self.printer_combo.get(),
            self.p_condition_var.get(),
            self.kiosk_id
        ))
        self.db_connection.commit()
        self.parent.refresh_buttons()  # Refresh main page buttons
        self.fetch_data()  # Fetch and display updated data
        ctk.CTkLabel(self, text="Saved!", font=("Helvetica", 40, "bold"), text_color='#dad122', bg_color="#020f12",fg_color="#020f12").pack(pady=10)
    

    def show_error(self):
        error_label = ctk.CTkLabel(self, text="Error: Kiosk data not found.", fg="red")
        error_label.pack(pady=20)
        self.back_button = ctk.CTkButton(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=10)

    def go_back(self):
        self.destroy()
        self.parent.refresh_buttons()  # Ensure main page is updated

    def on_closing(self):
        self.go_back()

# Main application entry point
if __name__ == "__main__":
    app = ctk.CTk(fg_color='#020f12')
    app.title("Kiosks Management")
    app.geometry("800x600")

    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    app.frames = {}
    for F in (KiosksPage,):
        page_name = F.__name__
        frame = F(master=container, controller=app)
        app.frames[page_name] = frame
        frame.pack(fill="both", expand=True)

    app.mainloop()
