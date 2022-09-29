from tkinter import ttk
import tkinter as tk
class Sidebar(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.img_canvas = tk.Canvas(self, width=128, height=128, bg='white')
        self.img_canvas.pack()

        self.summoner_icon = tk.PhotoImage(file="./ProfileIcons/0.png")
        self.img_canvas.create_image(
            (128, 128),
            image=self.summoner_icon,
            anchor="se"
        )

        self.summoner_name_button = ttk.Button(self, text="Guest")
        self.separator_1 = ttk.Separator(self, orient="horizontal")
        self.summoner_cumulat_st_button = ttk.Button(self, text="Cumulative Stats")
        self.match_history_button = ttk.Button(self, text="Match History")
        self.group_st_button = ttk.Button(self, text="Group Stats")
        self.record_st_button = ttk.Button(self, text="Records")

        self.summoner_name_button.pack()
        self.separator_1.pack(fill="x", pady=20)
        self.summoner_cumulat_st_button.pack(fill="x")
        self.group_st_button.pack(fill="x", pady=10)
        self.record_st_button.pack(fill="x")
    
    def command_summoner_name_button(self, main_fcn):
        self.summoner_name_button.configure(command=main_fcn)
    
    def command_match_history_button(self, main_fcn):
        self.match_history_button.configure(command=main_fcn)

    def command_group_st_button(self, main_fcn):
        self.group_st_button.configure(command=main_fcn)

x = tk.Tk()
z = tk.Frame(x)
a = ttk.Button(z)
b = ttk.Separator(z, orient="vertical")
y = Sidebar(z)
y.grid(column=0, row=0, rowspan=6)
b.grid(column=1, row=0, rowspan=6, sticky="ns", padx=2)
a.grid(column=2, row=2, rowspan=3)
z.pack()
x.mainloop()

