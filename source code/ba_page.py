import customtkinter as ctk
import os
from PIL import Image, ImageTk
import sqlite3
import images as ic

class BillAcceptor_Page(ctk.CTkFrame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.controller = controller
        self.db_connection = self.controller.db_connection
        self.configure(fg_color='#020f12')

        # List of image file names and variables to hold the image data
        image_files = ["MEI.png", "ICT.png", "NV.png","CashCode.png"]
        self.tk_images = []
        bill_accaptors = ["MEI", "ICT", "NV","CashCode"]
        for ba_id, bill_accaptor in enumerate(bill_accaptors):
            label = ctk.CTkLabel(self, text=f"{bill_accaptor} lar soni", font=("Helvetica", 25, "bold"), text_color="#DC143C", fg_color="#020f12")
            label.place(relx=0.12 + ba_id * 0.25, rely=0.2, relwidth=0.2, relheight=0.2, anchor="center")

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            for image_file in image_files:
                image_path = os.path.join(script_dir, f"../images/{image_file}")
                pil_image = Image.open(image_path)

                # Scale the image
                original_width, original_height = pil_image.size
                scale_factor = 1  # Adjust this scale factor as needed
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
                pil_image = pil_image.convert("RGBA")

                tk_image = ImageTk.PhotoImage(pil_image)
                self.tk_images.append(tk_image)

        except (FileNotFoundError, IOError) as e:
            print(f"Error loading image: {e}")
            self.destroy()
            raise

        # Create image frames and labels
        self.image_frames = []
        self.image_labels = []

        for idx, tk_image in enumerate(self.tk_images):
            frame = ctk.CTkFrame(self, fg_color='#020f12')
            frame.place(relx=0.02 + idx * 0.25, rely=0.3, relwidth=0.2, relheight=0.3)  # Adjust the frame size and position
            self.image_frames.append(frame)

            label = ctk.CTkLabel(frame, image=tk_image, fg_color='#020f12', text="")
            label.pack(expand=True, fill="both")  # Expand label to fill the frame
            self.image_labels.append(label)

        self.create_widgets()

    def create_widgets(self):
        
        
        self.home_button = ctk.CTkButton(self, image=ic.iconik("home",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#ECF0F1',
                                         text_color='#3498DB',hover_color='#ECF0F1',font=("Arial",16,'bold'),
                                             text="Home", command=self.go_home)
        self.home_button.place(relx=0.5, rely=0.05, anchor="center")  # Position the button below the image

        # Add the MEI label and entry
       

        # Fetch current values from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT MEI_n, ICT_n, NV_n,CASHCODE_n FROM storage WHERE id = 1')
        result = cursor.fetchone()
        mei_value = result[0] if result else 0
        ict_value = result[1] if result else 0
        nv_value = result[2] if result else 0
        cashcode_value = result[2] if result else 0

        # Create entries for each value
        self.entries = []
        values = [mei_value, ict_value, nv_value,cashcode_value]
        labels = ["MEI", "ICT", "NV","CASHCODE"]
        
        for idx, (value, label) in enumerate(zip(values, labels)):
            entry = ctk.CTkEntry(self, width=100)
            entry.insert(0, str(value))
            entry.place(relx=0.12 + idx * 0.25, rely=0.25, anchor="center")
            self.entries.append(entry)
        
        # Add a button to update all values in the database
        self.update_values_button = ctk.CTkButton(self,image=ic.iconik("update",32),bg_color='#020f12',fg_color='#020f12',
                                         border_width=2,corner_radius=32,border_color='#00FF00',
                                         text_color='#800080',hover_color='#00FF00',font=("Arial",16,'bold'),
                                         text="Update Values", command=self.update_values)
        self.update_values_button.place(relx=0.5, rely=0.7, anchor="center")


        dev_label1 =  ctk.CTkLabel(self, text="Developer:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        dev_label1.place(relx=0.02,rely=0.8)
        dev_label =  ctk.CTkLabel(self, text="F.Sattorov", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        dev_label.place(relx=0.115,rely=0.8)
        eng_label1 =  ctk.CTkLabel(self, text="Engineer:\nAsistant:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        eng_label1.place(relx=0.75,rely=0.8)
        eng_label =  ctk.CTkLabel(self, text="E.Sattorov\nSh.Ro'ziyev", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        eng_label.place(relx=0.85,rely=0.8)

    def update_values(self):
        new_values = [entry.get() for entry in self.entries]
    
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE storage SET MEI_n = ?, ICT_n = ?, NV_n = ?, CASHCODE_n=? WHERE id = 1', tuple(new_values))
        self.db_connection.commit()
    
        ctk.CTkLabel(self, text="Updated!", font=("Helvetica", 20, "bold"), text_color="green", fg_color="#020f12").place(relx=0.5, rely=0.75, anchor="center")
    
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
    for F in (BillAcceptor_Page,):
        page_name = F.__name__
        frame = F(master=container, controller=app)
        app.frames[page_name] = frame
        frame.pack(fill="both", expand=True)

    app.mainloop()
