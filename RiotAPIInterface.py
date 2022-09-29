from ratelimit import limits, sleep_and_retry
import requests
from typing import Any, List, Dict

class RequestError(Exception):
    pass

class RiotAPIInterface:  
    API_KEY = "nothing to see here"
    def __init__(self) -> None:
        pass

    @sleep_and_retry
    @limits(calls=95, period=120)
    def call_riot_api(self, url: str) -> requests.Response:
        response = None
        try:
            response = requests.get(url)
            status_code = response.status_code
            if status_code != 200:
                print(status_code)
                raise RequestError
        except RequestError:
            print("Somfing wong")
            return

        return response
        

    def get_match_data_as_json(self, matchId: str) -> Dict:
        match_url = "https://europe.api.riotgames.com/lol/match/v5/matches/" + matchId + "?api_key=" + self.API_KEY
        response = self.call_riot_api(match_url).json()
        return response

    def get_summoner_info_from_summoner_name(self, summoner_name: str) -> Any:
        summoner_info_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + self.API_KEY
        response = self.call_riot_api(summoner_info_url)
        # for now just give puuid, but here is summoner_level hidden etc
        return response.json()

    def get_match_list_by_timestamp(self, puuid: str, last_match_timestamp: int) -> List[str]:
        print("Last_Match_TimeStamp: " + str(last_match_timestamp))
        match_list_url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?startTime=" + str(last_match_timestamp) + "&api_key=" + self.API_KEY
        response = self.call_riot_api(match_list_url)
        print(response)
        return response.json()
        
    def get_match_list_by_count(self, puuid: str, count: int) -> List[str]:
        match_list_url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?count=" + str(count) + "&api_key=" + self.API_KEY
        response = self.call_riot_api(match_list_url)
        return response.json()
