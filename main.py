import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Resources.Functions.allow import allow_menu
from Resources.Functions.block import block_menu
from Resources.Functions.update import update_db
import pystray, threading


class FirewallGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aegis Firewall")
        self.geometry("400x300")
        self.resizable(False, False)

        # ==== Background ====
        bg_image = Image.open("Resources\\Assets\\bg.png").resize((400, 300))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        tk.Label(self, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

        # ==== Centered frame for elements ====
        main_frame = tk.Frame(self, bg="#172445")
        main_frame.place(relx=0.5, rely=0.6, anchor="center")

        # ==== Left: Logo ====
        img_frame = tk.Frame(main_frame, width=150, height=250, bg="#172445")
        img_frame.pack(side="left", fill="y")
        img_frame.pack_propagate(False)

        img = Image.open("Resources\\Assets\\icon.png").resize((120, 140))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg="#172445")
        img_label.image = photo
        img_label.pack(pady=20)

        # ==== Right: Buttons ====
        btn_frame = tk.Frame(main_frame, bg="#172445")
        btn_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # Declare self.destroy as window close event
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Associate buttons with their functions
        btn_texts = ["Allow", "Block", "Online Blacklist", "Exit"]
        btn_actions = [allow_menu, block_menu, update_db, self.destroy]

        for i, text in enumerate(btn_texts):
            btn = tk.Button(
                btn_frame,
                text=text,
                width=15,
                command=btn_actions[i],
                bg="#1f2e5a", 
                fg="white", 
                relief="flat",
                cursor="hand2"
            )
            
            btn.pack(pady=8, fill="x")


def run_gui():
    gui = FirewallGUI()
    gui.mainloop()


if __name__ == "__main__":
    # Run the GUI in a separate thread so it does not to overlap the tray icon thread
    def on_clicked():
        threading.Thread(target=run_gui, daemon=True).start()

    def on_quit(icon):
        icon.stop()

    image = Image.open("Resources\\Assets\\icon.png")
    menu = pystray.Menu(
        pystray.MenuItem("Open GUI", on_clicked),
        pystray.MenuItem("Exit", on_quit)
    )

    # Start the system tray icon
    icon = pystray.Icon("Firewall", image, "Firewall", menu)
    icon.run()
    
