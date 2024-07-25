import customtkinter as ctk
import sqlite3
import images as ic

class OthersPage(ctk.CTkFrame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.controller = controller
        self.db_connection = self.controller.db_connection
        self.configure(fg_color='#020f12')
        
       
        
        self.home_button = ctk.CTkButton(self, image=ic.iconik("home",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#ECF0F1',
                                         text_color='#3498DB',hover_color='#ECF0F1',font=("Arial",16,'bold'),
                                            text="Home", command=self.go_home)
        self.home_button.place(relx=0.5, rely=0.03, anchor="center")  # Adjust the button position

        # Create the scrollable frame with padding at the bottom
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color='#020f12')
        self.scrollable_frame.pack(pady=(60, 20), padx=20, fill="both", expand=True)
        
        self.create_widgets()

        # Add a button to update all values in the database
        self.update_values_button = ctk.CTkButton(self,image=ic.iconik("update",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#00FF00',
                                         text_color='#800080',hover_color='#00FF00',font=("Arial",16,'bold'),
                                           text="Update Values", command=self.update_values)
        self.update_values_button.place(relx=0.5, rely=0.9, anchor="center")

        dev_label1 = ctk.CTkLabel(self, text="Developer:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        dev_label1.place(relx=0.02, rely=0.9, anchor="sw")
        dev_label = ctk.CTkLabel(self, text="F.Sattorov", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        dev_label.place(relx=0.115, rely=0.9, anchor="sw")
        seng_label1 = ctk.CTkLabel(self, text="Engineer:\nAssistant:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        seng_label1.place(relx=0.75, rely=0.9, anchor="sw")
        seng_label = ctk.CTkLabel(self, text="E.Sattorov\nSh.Ro'ziyev", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        seng_label.place(relx=0.85, rely=0.9, anchor="sw")

    def create_widgets(self):
        equipments = ["Touchscreen", "Display", "DDR3", "Modem", "Simcard", "BA_board", "Motherboard",
                      "Comport Board", "Power Supply", "Paper"]

        # Fetch current values from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT Touchscreen_n, Display_n, DDR3_n, Modem_n, Simcard_n, BA_board_n, motherboard_n, '
                       'comport_board_n, power_supply_n, paper_n FROM storage WHERE id = 1')
        result = cursor.fetchone()
        
        values = result if result else [0] * 10

        self.entries = []
        num_cols = 5
        tk_images = ic.l_im(equipments, scale_factor=0.5)
        
        image_frames = []
        image_labels = []
        for idx, (equipment, value, tk_image) in enumerate(zip(equipments, values, tk_images)):
            col_index = idx % num_cols
            row_index = idx // num_cols
        
            # Top Text Label
            label = ctk.CTkLabel(self.scrollable_frame, text=f"{equipment} lar soni", font=("Helvetica", 25, "bold"), text_color="#DC143C", fg_color="#020f12")
            label.grid(row=row_index * 3, column=col_index, padx=25, pady=(50, 10), sticky="nsew")
        
            # Middle Image Frame
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color='#020f12')
            frame.grid(row=row_index * 3 + 1, column=col_index, padx=50, pady=10, sticky="nsew")
            image_frames.append(frame)
        
            # Image Label inside the Frame
            label_i = ctk.CTkLabel(frame, image=tk_image, fg_color='#020f12', text="")
            label_i.pack(expand=True, fill="both")
            image_labels.append(label_i)
        
            # Bottom Entry
            entry = ctk.CTkEntry(self.scrollable_frame, width=100)
            entry.insert(0, str(value))
            entry.grid(row=row_index * 3 + 2, column=col_index, padx=50, pady=(10, 50), sticky="nsew")
            self.entries.append(entry)

    def update_values(self):
        new_values = [entry.get() for entry in self.entries]

        try:
            cursor = self.db_connection.cursor()
            cursor.execute('UPDATE storage SET Touchscreen_n=?, Display_n=?, DDR3_n=?, Modem_n=?, '
                           'Simcard_n=?, BA_board_n=?, motherboard_n=?, comport_board_n=?, power_supply_n=?, paper_n=? WHERE id = 1', tuple(new_values))
            self.db_connection.commit()

            update_label = ctk.CTkLabel(self, text="Updated!", font=("Helvetica", 20, "bold"), text_color="green", fg_color="#020f12")
            update_label.place(relx=0.5, rely=0.87, anchor="center")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            error_label = ctk.CTkLabel(self, text="Update Failed!", font=("Helvetica", 20, "bold"), text_color="red", fg_color="#020f12")
            error_label.place(relx=0.5, rely=0.87, anchor="center")

    def go_home(self):
        self.controller.show_frame("HomePage")
        


# Main application entry point
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Bill Acceptors Management")
    app.geometry("800x600")

    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    app.frames = {}
    for F in (OthersPage,):
        page_name = F.__name__
        frame = F(master=container, controller=app)
        app.frames[page_name] = frame
        frame.pack(fill="both", expand=True)

    app.mainloop()
