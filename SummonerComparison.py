from tkinter import ttk
import tkinter as tk

class SummonerComparison(ttk.Frame):
    def __init__(self, container, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)
        self.summoner_name_title = ttk.Label(self, text="Enter Summoner Name")
        self.summoner_name_title.pack()

        self.summoner_name = tk.StringVar()
        self.summoner_puuid = tk.StringVar()
        self.summoner_name_entry = ttk.Entry(
            self, textvariable=self.summoner_name)
        self.summoner_name_entry.pack()

        self.summoner_search_btn = ttk.Button(self, text="Search")
        self.summoner_search_btn.pack()

        self.summoner_search_status = ttk.Label(self, text="")
        self.summoner_search_status.pack()
    
    def summoner_search_btn_clicked(self) -> None:
        self.summoner_search_status['text'] = "Searching..."
        summoner_name = self.summoner_name.get()
        if summoner_name == "":
            self.summoner_search_status['text'] = "Can\'t search for no user!"
            return
        summoner = self.riot_db.get_summoner_by_summoner_name(
            summoner_name=summoner_name)
        if summoner is None:
            self.summoner_search_status['text'] = "User " + summoner_name + \
                " not found in database, user needs to register!"
            return
        else:
            self.summoner_search_status['text'] = "User " + \
                summoner_name + " found!"
            self.summoner_puuid.set(summoner.puuid)
            newest_match = self.riot_db.get_newest_match_from_db()
            participunto = self.riot_db.get_participant_by_match_and_puuid(
                newest_match.matchId, self.summoner_puuid.get())
            for text_field in Cumulative:
                self.endpoint_textbox_dict[text_field.name]['text'] = participunto.__dict__.get(
                    text_field.name)


    def setup_summoner_search_cmd(self, command):
        self.summoner_search_btn.configure(command=command)
