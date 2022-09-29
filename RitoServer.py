from typing import Dict, List
import os.path
import os
import sqlite3
import tkinter as tk
from tkinter import Y, ttk

from RiotDatabase import RiotDatabase
from RiotAPIInterface import RiotAPIInterface
from Constants import *
from ScrollableFrame import ScrollableFrame
from SummonerComparison import SummonerComparison

# DONE: Convert txt data to database (sqlite3?)
# GOING: Create database-inserts/calls + optional calls to RiotAPI if outdated etc.
# DONE: Alternative for InfoTypes: Mapping of DB-Column to Displayed Name
# TODO: Divide the DisplayValuesStatistics into useful categories ->
# CUMULATIVE, MATCH_HISTORY, RECORDS (different institutes/groups)
# https://www.pythontutorial.net/tkinter/tkinter-notebook/
# https://blog.teclado.com/tkinter-scrollable-frames/
# TODO: Map SpellIDs, ProfileIconIDs etc. to actual pictures [VERY TIME CONSUMING]
# TODO: Handle exceptions at API call
# TODO: Update UI


# Information: 20 calls per second, 100 calls every 2 minutes => ca. 1 call per second average

# Data to save: totalDamageDealtToChampions, matchID, gameEndTimestamp

# Save matchID-Data globally
# When searching one matchID, compare all match participants with summoner_list -> if inside, queue stat refresh
# try using rate limiting package

# workflow:
# 0. Check summoner_list for updates
# 1. foreach summoner in summoner list
# 2. get the newest matches since last match in match_history_list OR if timestamp > last_match_timestamp
# 3. foreach match not in match_history_list
# 4. go through all puuids in this match
# 5. if puuid in summoner list
# 6. fill a list which will be subsequently worked through to add each data point
# 7. foreach summoner in filled_list from 6.
# 8. look for chosen key (e.g. totalDamageDealtToChampions), and add to PERSONAL damage pool
# 9. save this damage dict
# 10. save match_list
# 11. repeat every hour


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.riot_db = RiotDatabase()
        self.setup_gui_window()
        self.setup_summoner_search_prompt()
        self.change_to_cumulative_tab()
        self.setup_match_history()

    def setup_gui_window(self) -> None:
        self.title("Hebelag\'s cumulative LoL Statistics")

        self.window_width = 1280
        self.window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width/2 - self.window_width/2)
        center_y = int(screen_height/2 - self.window_height/2)

        self.geometry(
            f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.resizable(False, False)

    def setup_summoner_search_prompt(self) -> None:
        self.summoner_comparison = SummonerComparison(self)
        

        

        
        self.summoner_search_btn['command'] = self.summoner_search_btn_clicked
        

        

    def change_to_cumulative_tab(self) -> None:
        frame = ScrollableFrame(self)
        endpoint_columns = 4
        for i in range(0, endpoint_columns):
            frame.scrollable_frame.columnconfigure(i, weight=2)
        self.endpoint_textbox_dict: Dict[str, ttk.Label] = {}
        row_count = 0
        endpoint_loop_count = 0

        for entry in Cumulative:
            temp_text_field_label = ttk.Label(
                frame.scrollable_frame, text=entry.value)
            temp_text_field_label.grid(
                column=endpoint_loop_count, row=row_count, padx=5, pady=5)

            temp_text_field = ttk.Label(frame.scrollable_frame, text="0")
            temp_text_field.grid(column=endpoint_loop_count,
                                 row=row_count + 1, padx=5, pady=5)
            self.endpoint_textbox_dict[entry.name] = temp_text_field
            endpoint_loop_count += 1
            if endpoint_loop_count % endpoint_columns == 0:
                row_count += 2
                endpoint_loop_count = 0

        frame.grid(column=1, columnspan=4, row=0, rowspan=8)

    def change_to_summoner_frame(self) -> None:
        
        pass

    def setup_match_history(self) -> None:
        # https://tkdocs.com/tutorial/grid.html
        pass

    


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
#while True:
#    RiotDB.fetch_new_matches()
#    RiotDB.save_summoner_db()
#    for i in range(300, 0, -1):
#        sys.stdout.write("Updating in " + str(i) + " seconds. \r")
#        sys.stdout.write("\033[K")
#        time.sleep(1)
