import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sqlite3
from kiosks_page import KiosksPage
from incasators_page import IncasatorsPage
from ba_page import BillAcceptor_Page
from printers import PrintersPage
from others import OthersPage



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

class HomePage(ctk.CTkFrame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.configure(fg_color='#020f12')
     
        label = ctk.CTkLabel(self, text="Maroqand Storage", font=("Helvetica", 25, "bold"), text_color="#DC143C", fg_color="#020f12")
        label.pack(pady=10)
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "../images/logo.png")
            pil_image = Image.open(image_path)
        except (FileNotFoundError, IOError) as e:
            print(f"Error loading image: {e}")
            self.destroy()
            raise
        
        pil_image = pil_image.convert("RGBA")
        self.tk_image = ImageTk.PhotoImage(pil_image)
        
        self.image_frame = ctk.CTkFrame(self, fg_color='#020f12')
        self.image_frame.pack(fill=ctk.BOTH, expand=True)
        
        self.image_label = ctk.CTkLabel(self.image_frame, image=self.tk_image, fg_color='#020f12', text="")
        self.image_label.pack(pady=10)  # Use pack or grid instead of place

        self.create_widgets()

    def create_widgets(self):

        self.bill = InterActiveButton(self, text="Bill Acceptorlar", width=250, height=50,command=self.go_to_ba)
        self.goods = InterActiveButton(self, text="Boshqa mahsulotlar", width=250, height=50,command=self.go_to_others)
        self.printers = InterActiveButton(self, text="Printerlar", width=250, height=50,command=self.go_to_printers)
        self.incasators = InterActiveButton(self, text="Incasatorlar", width=250, height=50,command=self.go_to_incasators)
        self.kiosks = InterActiveButton(self, text="Kiosklar", width=250, height=50, command=self.go_to_kiosks)

        self.bill.place(relx=0.1, rely=0.2)
        self.goods.place(relx=0.7, rely=0.2)
        self.printers.place(relx=0.2, rely=0.4)
        self.incasators.place(relx=0.415, rely=0.6)
        self.kiosks.place(relx=0.6, rely=0.4)
       
        dev_label1 =  ctk.CTkLabel(self, text="Developer:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        dev_label1.place(relx=0.02,rely=0.8)
        dev_label =  ctk.CTkLabel(self, text="F.Sattorov", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        dev_label.place(relx=0.115,rely=0.8)
        eng_label1 =  ctk.CTkLabel(self, text="Engineer:\nAsistant:", font=("Helvetica", 30, "bold"), text_color="#DC143C", fg_color="#020f12")
        eng_label1.place(relx=0.75,rely=0.8)
        eng_label =  ctk.CTkLabel(self, text="E.Sattorov\nSh.Ro'ziyev", font=("Helvetica", 30, "bold"), text_color="#000080", fg_color="#020f12")
        eng_label.place(relx=0.85,rely=0.8)
        

    def go_to_ba(self):
        self.controller.show_frame("BillAcceptor_Page")
    def go_to_printers(self):
        self.controller.show_frame("PrintersPage")
    def go_to_kiosks(self):
        self.controller.show_frame("KiosksPage")
    def go_to_incasators(self):
        self.controller.show_frame("IncasatorsPage")
    def go_to_others(self):
        self.controller.show_frame("OthersPage")


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Maroqand Storage")
        
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.db_connection = self.connect_db()
        for F in (HomePage,KiosksPage,IncasatorsPage,BillAcceptor_Page,PrintersPage,OthersPage):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def connect_db(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "../database/database.db")
            conn = sqlite3.connect(db_path)
            return conn
        except Exception as e:
            print("Error during connection:", str(e))
            return None

    def __del__(self):
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
