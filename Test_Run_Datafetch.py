from RiotDatabase import RiotDatabase

db = RiotDatabase()
x = db.get_newest_match_from_db()
print(x)
#db.fetch_new_summoner("Hebelag")

HEBELAG_PUUID = "t_98ES-6qtkXVKa0SmqXA7-btqktMLNt9MqFGQ0tZ4MniDE8wMcqzKpL2bDYsQJapuHp5DDKxFDx2g"

db.fetch_newest_matches_by_user(puuid = HEBELAG_PUUID)