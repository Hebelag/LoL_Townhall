from typing import Dict, List, Tuple
from RiotAPIInterface import RiotAPIInterface
import json
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import func
from Models import Summoner, Match, Challenge, Participant
import logging

Base = declarative_base()


class RiotDatabase():
    
    def __init__(self) -> None:
        self.riot_api = RiotAPIInterface()
        try:
            self.engine = create_engine('sqlite:///summoners3.db', echo = True)
            self.meta = MetaData()
            self.conn = self.engine.connect()
            self.sessionmaker = sessionmaker(bind = self.engine)
            self.session = self.sessionmaker()
        except Exception as e:
            logging.warning(e)

    def insert_summoner_into_db(self, summoner: Summoner) -> Summoner:
        try:
            existing_summoner = (
                self.session.query(Summoner).filter(Summoner.summonerName == summoner.summonerName).first()
            )
            if existing_summoner is None:
                self.session.add(summoner)
                self.session.commit()
            else:
                logging.warning(f"User {summoner.summonerName} already exists!")
            return self.session.query(Summoner).filter(Summoner.summonerName == summoner.summonerName).first()
        except IntegrityError as e:
            logging.warning(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            logging.warning(f"Unexpected error when inserting new summoner: {e}")
            raise e
    
    def insert_match_into_db(self, match: Match) -> Match:
        try:
            existing_match = (
                self.session.query(Match).filter(Match.matchId == match.matchId).first()
            )
            if existing_match is None:
                self.session.add(match)
                self.session.commit()
            else:
                logging.warning(f"Match {match.matchId} already exists!")
            return self.session.query(Match).filter(Match.matchId == match.matchId).first()
        except IntegrityError as e:
            logging.warning(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            logging.warning(f"Unexpected error when inserting new match: {e}")
            raise e

    def insert_participant_into_db(self, participant: Participant) -> Participant:
        try:
            self.session.add(participant)
            self.session.commit()
        except IntegrityError as e:
            logging.warning(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            logging.warning(f"Unexpected error when inserting new participant: {e}")
            raise e
        
    def insert_challenge_into_db(self, challenge: Challenge) -> Challenge:
        try:
            self.session.add(challenge)
            self.session.commit()
        except IntegrityError as e:
            logging.warning(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            logging.warning(f"Unexpected error when inserting new challenge: {e}")
            raise e

    def get_all_match_ids_from_db(self) -> List[str]:
        return self.session.query(Match.matchId).all()

    def get_all_matches_from_db(self) -> List[Match]:
        return self.session.query(Match).all()

    def get_all_summoners_from_db(self) -> List[Summoner]:
        return self.session.query(Summoner).all()

    def get_newest_match_from_db(self) -> Match:
        return self.session.query(Match).filter(Match.gameCreation == func.max(Match.gameCreation).select()).one()

    def get_latest_timestamp_from_db(self) -> int:
        timestamp = self.session.query(func.max(Match.gameCreation)).first()[0]
        if timestamp is None:
            return 0
        else:
            return timestamp

    def get_participant_by_match_and_puuid(self, matchId: str, puuid: str) -> Participant:
        print("Match ID: " + matchId + "| PUUID: " + puuid)
        participant = self.session.query(Participant).filter(Participant.matchId == matchId, Participant.puuid == puuid).one_or_none()
        if participant is None:
            raise SQLAlchemyError
        else:
            return participant
    
    def fetch_new_summoner(self, summoner_name: str) -> None:
        summoner_info = self.riot_api.get_summoner_info_from_summoner_name(summoner_name=summoner_name)
        summoner = Summoner(
            puuid = summoner_info['puuid'],
            summonerName = summoner_info['name'],
            accountId = summoner_info['accountId'],
            profileIconId = summoner_info['profileIconId'],
            revisionDate = summoner_info['revisionDate'],
            summonerId = summoner_info['id'],
            summonerLevel = summoner_info['summonerLevel']
        )
        self.insert_summoner_into_db(summoner=summoner)

    def get_puuid_from_summoner_name_db(self, summoner_name: str) -> str:
        return self.get_summoner_by_summoner_name(summoner_name=summoner_name).puuid

    def get_summoner_by_summoner_name(self, summoner_name: str) -> Summoner:
        return self.session.query(Summoner).filter(Summoner.summonerName == summoner_name).one_or_none()


    def convert_match_json_to_orm(self, match_json: Dict) -> Tuple[Match, List[Participant], List[Challenge]]:
        match_history = Match(
            matchId = match_json['metadata']['matchId'],
            dataVersion = match_json['metadata']['dataVersion'],
            participant_1 = match_json['metadata']['participants'][0],
            participant_2 = match_json['metadata']['participants'][1],
            participant_3 = match_json['metadata']['participants'][2],
            participant_4 = match_json['metadata']['participants'][3],
            participant_5 = match_json['metadata']['participants'][4],
            participant_6 = match_json['metadata']['participants'][5],
            participant_7 = match_json['metadata']['participants'][6],
            participant_8 = match_json['metadata']['participants'][7],
            participant_9 = match_json['metadata']['participants'][8],
            participant_10 = match_json['metadata']['participants'][9],
            gameCreation = match_json['info']['gameCreation'],
            gameDuration = match_json['info']['gameDuration'],
            gameEndTimestamp = match_json['info']['gameEndTimestamp'],
            gameId = match_json['info']['gameId'],
            gameMode = match_json['info']['gameMode'],
            gameName = match_json['info']['gameName'],
            gameStartTimestamp = match_json['info']['gameStartTimestamp'],
            gameType = match_json['info']['gameType'],
            gameVersion = match_json['info']['gameVersion'],
            mapId = match_json['info']['mapId'],
            participants = json.dumps(match_json['info']['participants']),
            platformId = match_json['info']['platformId'],
            queueId = match_json['info']['queueId'],
            teams = json.dumps(match_json['info']['teams']),
            tournamentCode = match_json['info']['tournamentCode']
        )

        participant_list: List[Participant] = []

        for participant in match_json['info']['participants']:
            participant_obj = Participant(
                puuid = participant['puuid'],
                matchId = match_json['metadata']['matchId'],
                assists = participant['assists'],
                baronKills = participant['baronKills'],
                bountyLevel = participant['bountyLevel'],
                champExperience = participant['champExperience'],
                champLevel = participant['champLevel'],
                championId = participant['championId'],
                championName = participant['championName'],
                championTransform = participant['championTransform'],
                consumablesPurchased = participant['consumablesPurchased'],
                damageDealtToBuildings = participant['damageDealtToBuildings'],
                damageDealtToObjectives = participant['damageDealtToObjectives'],
                damageDealtToTurrets = participant['damageDealtToTurrets'],
                damageSelfMitigated = participant['damageSelfMitigated'],
                deaths = participant['deaths'],
                detectorWardsPlaced = participant['detectorWardsPlaced'],
                doubleKills = participant['doubleKills'],
                dragonKills = participant['dragonKills'],
                firstBloodAssist = participant['firstBloodAssist'],
                firstBloodKill = participant['firstBloodKill'],
                firstTowerAssist = participant['firstTowerAssist'],
                firstTowerKill = participant['firstTowerKill'],
                gameEndedInEarlySurrender = participant['gameEndedInEarlySurrender'],
                gameEndedInSurrender = participant['gameEndedInSurrender'],
                goldEarned = participant['goldEarned'],
                goldSpent = participant['goldSpent'],
                individualPosition = participant['individualPosition'],
                inhibitorKills = participant['inhibitorKills'],
                inhibitorTakedowns = participant['inhibitorTakedowns'],
                inhibitorsLost = participant['inhibitorsLost'],
                item0 = participant['item0'],
                item1 = participant['item1'],
                item2 = participant['item2'],
                item3 = participant['item3'],
                item4 = participant['item4'],
                item5 = participant['item5'],
                item6 = participant['item6'],
                itemsPurchased = participant['itemsPurchased'],
                killingSprees = participant['killingSprees'],
                kills = participant['kills'],
                lane = participant['lane'],
                largestCriticalStrike = participant['largestCriticalStrike'],
                largestKillingSpree = participant['largestKillingSpree'],
                largestMultiKill = participant['largestMultiKill'],
                longestTimeSpentLiving = participant['longestTimeSpentLiving'],
                magicDamageDealt = participant['magicDamageDealt'],
                magicDamageDealtToChampions = participant['magicDamageDealtToChampions'],
                magicDamageTaken = participant['magicDamageTaken'],
                neutralMinionsKilled = participant['neutralMinionsKilled'],
                nexusKills = participant['nexusKills'],
                nexusTakedowns = participant['nexusTakedowns'],
                nexusLost = participant['nexusLost'],
                objectivesStolen = participant['objectivesStolen'],
                objectivesStolenAssists = participant['objectivesStolenAssists'],
                participantId = participant['participantId'],
                pentaKills = participant['pentaKills'],
                perks = json.dumps(participant['perks']),
                physicalDamageDealt = participant['physicalDamageDealt'],
                physicalDamageDealtToChampions = participant['physicalDamageDealtToChampions'],
                physicalDamageTaken = participant['physicalDamageTaken'],
                profileIcon = participant['profileIcon'],
                quadraKills = participant['quadraKills'],
                riotIdName = participant['riotIdName'],
                riotIdTagline = participant['riotIdTagline'],
                role = participant['role'],
                sightWardsBoughtInGame = participant['sightWardsBoughtInGame'],
                spell1Casts = participant['spell1Casts'],
                spell2Casts = participant['spell2Casts'],
                spell3Casts = participant['spell3Casts'],
                spell4Casts = participant['spell4Casts'],
                summoner1Casts = participant['summoner1Casts'],
                summoner1Id = participant['summoner1Id'],
                summoner2Casts = participant['summoner2Casts'],
                summoner2Id = participant['summoner2Id'],
                summonerId = participant['summonerId'],
                summonerLevel = participant['summonerLevel'],
                summonerName = participant['summonerName'],
                teamEarlySurrendered = participant['teamEarlySurrendered'],
                teamId = participant['teamId'],
                teamPosition = participant['teamPosition'],
                timeCCingOthers = participant['timeCCingOthers'],
                timePlayed = participant['timePlayed'],
                totalDamageDealt = participant['totalDamageDealt'],
                totalDamageDealtToChampions = participant['totalDamageDealtToChampions'],
                totalDamageShieldedOnTeammates = participant['totalDamageShieldedOnTeammates'],
                totalDamageTaken = participant['totalDamageTaken'],
                totalHeal = participant['totalHeal'],
                totalHealsOnTeammates = participant['totalHealsOnTeammates'],
                totalMinionsKilled = participant['totalMinionsKilled'],
                totalTimeCCDealt = participant['totalTimeCCDealt'],
                totalTimeSpentDead = participant['totalTimeSpentDead'],
                totalUnitsHealed = participant['totalUnitsHealed'],
                tripleKills = participant['tripleKills'],
                trueDamageDealt = participant['trueDamageDealt'],
                trueDamageDealtToChampions = participant['trueDamageDealtToChampions'],
                trueDamageTaken = participant['trueDamageTaken'],
                turretKills = participant['turretKills'],
                turretTakedowns = participant['turretTakedowns'],
                turretsLost = participant['turretsLost'],
                unrealKills = participant['unrealKills'],
                visionScore = participant['visionScore'],
                visionWardsBoughtInGame = participant['visionWardsBoughtInGame'],
                wardsKilled = participant['wardsKilled'],
                wardsPlaced = participant['wardsPlaced'],
                win = participant['win']
            )
            participant_list.append(participant_obj)
        challenge_list: List[Challenge] = []
        for participant in match_json['info']['participants']:

            part_chal: Dict = participant['challenges']
            challenge = Challenge(
                puuid = participant.get('puuid'),
                matchId = match_json.get('metadata').get('matchId'),
                abilityUses = part_chal.get('abilityUses'),
                acesBefore15Minutes = part_chal.get('acesBefore15Minutes'),
                alliedJungleMonsterKills = part_chal.get('alliedJungleMonsterKills'),
                baronTakedowns = part_chal.get('baronTakedowns'),
                blastConeOppositeOpponentCount = part_chal.get('blastConeOppositeOpponentCount'),
                bountyGold = part_chal.get('bountyGold'),
                buffsStolen = part_chal.get('buffsStolen'),
                completeSupportQuestInTime = part_chal.get('completeSupportQuestInTime'),
                controlWardTimeCoverageInRiverOrEnemyHalf = part_chal.get('controlWardTimeCoverageInRiverOrEnemyHalf'),
                controlWardsPlaced = part_chal.get('controlWardsPlaced'),
                damagePerMinute = part_chal.get('damagePerMinute'),
                damageTakenOnTeamPercentage = part_chal.get('damageTakenOnTeamPercentage'),
                dancedWithRiftHerald = part_chal.get('dancedWithRiftHerald'),
                deathsByEnemyChamps = part_chal.get('deathsByEnemyChamps'),
                dodgeSkillShotsSmallWindow = part_chal.get('dodgeSkillShotsSmallWindow'),
                doubleAces = part_chal.get('doubleAces'),
                dragonTakedowns = part_chal.get('dragonTakedowns'),
                earlyLaningPhaseGoldExpAdvantage = part_chal.get('earlyLaningPhaseGoldExpAdvantage'),
                effectiveHealAndShielding = part_chal.get('effectiveHealAndShielding'),
                elderDragonKillsWithOpposingSoul = part_chal.get('elderDragonKillsWithOpposingSoul'),
                elderDragonMultikills = part_chal.get('elderDragonMultikills'),
                enemyChampionImmobilizations = part_chal.get('enemyChampionImmobilizations'),
                enemyJungleMonsterKills = part_chal.get('enemyJungleMonsterKills'),
                epicMonsterKillsNearEnemyJungler = part_chal.get('epicMonsterKillsNearEnemyJungler'),
                epicMonsterKillsWithin30SecondsOfSpawn = part_chal.get('epicMonsterKillsWithin30SecondsOfSpawn'),
                epicMonsterSteals = part_chal.get('epicMonsterSteals'),
                epicMonsterStolenWithoutSmite = part_chal.get('epicMonsterStolenWithoutSmite'),
                firstTurretKilledTime = part_chal.get('firstTurretKilledTime'),
                flawlessAces = part_chal.get('flawlessAces'),
                fullTeamTakedown = part_chal.get('fullTeamTakedown'),
                gameLength = part_chal.get('gameLength'),
                getTakedownsInAllLanesEarlyJungleAsLaner = part_chal.get('getTakedownsInAllLanesEarlyJungleAsLaner'),
                goldPerMinute = part_chal.get('goldPerMinute'),
                hadOpenNexus = part_chal.get('hadOpenNexus'),
                immobilizeAndKillWithAlly = part_chal.get('immobilizeAndKillWithAlly'),
                initialBuffCount = part_chal.get('initialBuffCount'),
                initialCrabCount = part_chal.get('initialCrabCount'),
                jungleCsBefore10Minutes = part_chal.get('jungleCsBefore10Minutes'),
                junglerTakedownsNearDamagedEpicMonster = part_chal.get('junglerTakedownsNearDamagedEpicMonster'),
                kTurretsDestroyedBeforePlatesFall = part_chal.get('kTurretsDestroyedBeforePlatesFall'),
                kda = part_chal.get('kda'),
                killAfterHiddenWithAlly = part_chal.get('killAfterHiddenWithAlly'),
                killedChampTookFullTeamDamageSurvived = part_chal.get('killedChampTookFullTeamDamageSurvived'),
                killsNearEnemyTurret = part_chal.get('killsNearEnemyTurret'),
                killsOnOtherLanesEarlyJungleAsLaner = part_chal.get('killsOnOtherLanesEarlyJungleAsLaner'),
                killsOnRecentlyHealedByAramPack = part_chal.get('killsOnRecentlyHealedByAramPack'),
                killsUnderOwnTurret = part_chal.get('killsUnderOwnTurret'),
                killsWithHelpFromEpicMonster = part_chal.get('killsWithHelpFromEpicMonster'),
                knockEnemyIntoTeamAndKill = part_chal.get('knockEnemyIntoTeamAndKill'),
                landSkillShotsEarlyGame = part_chal.get('landSkillShotsEarlyGame'),
                laneMinionsFirst10Minutes = part_chal.get('laneMinionsFirst10Minutes'),
                laningPhaseGoldExpAdvantage = part_chal.get('laningPhaseGoldExpAdvantage'),
                legendaryCount = part_chal.get('legendaryCount'),
                lostAnInhibitor = part_chal.get('lostAnInhibitor'),
                maxCsAdvantageOnLaneOpponent = part_chal.get('maxCsAdvantageOnLaneOpponent'),
                maxKillDeficit = part_chal.get('maxKillDeficit'),
                maxLevelLeadLaneOpponent = part_chal.get('maxLevelLeadLaneOpponent'),
                moreEnemyJungleThanOpponent = part_chal.get('moreEnemyJungleThanOpponent'),
                multiKillOneSpell = part_chal.get('multiKillOneSpell'),
                multiTurretRiftHeraldCount = part_chal.get('multiTurretRiftHeraldCount'),
                multikills = part_chal.get('multikills'),
                multikillsAfterAggressiveFlash = part_chal.get('multikillsAfterAggressiveFlash'),
                mythicItemUsed = part_chal.get('mythicItemUsed'),
                outerTurretExecutesBefore10Minutes = part_chal.get('outerTurretExecutesBefore10Minutes'),
                outnumberedKills = part_chal.get('outnumberedKills'),
                outnumberedNexusKill = part_chal.get('outnumberedNexusKill'),
                perfectDragonSoulsTaken = part_chal.get('perfectDragonSoulsTaken'),
                perfectGame = part_chal.get('perfectGame'),
                pickKillWithAlly = part_chal.get('pickKillWithAlly'),
                playedChampSelectPosition = part_chal.get('playedChampSelectPosition'),
                poroExplosions = part_chal.get('poroExplosions'),
                quickCleanse = part_chal.get('quickCleanse'),
                quickFirstTurret = part_chal.get('quickFirstTurret'),
                quickSoloKills = part_chal.get('quickSoloKills'),
                riftHeraldTakedowns = part_chal.get('riftHeraldTakedowns'),
                saveAllyFromDeath = part_chal.get('saveAllyFromDeath'),
                scuttleCrabKills = part_chal.get('scuttleCrabKills'),
                skillshotsDodged = part_chal.get('skillshotsDodged'),
                skillshotsHit = part_chal.get('skillshotsHit'),
                snowballsHit = part_chal.get('snowballsHit'),
                soloBaronKills = part_chal.get('soloBaronKills'),
                soloKills = part_chal.get('soloKills'),
                stealthWardsPlaced = part_chal.get('stealthWardsPlaced'),
                survivedSingleDigitHpCount = part_chal.get('survivedSingleDigitHpCount'),
                survivedThreeImmobilizedInFight = part_chal.get('survivedThreeImmobilizedInFight'),
                takedownOnFirstTurret = part_chal.get('takedownOnFirstTurret'),
                takedowns = part_chal.get('takedowns'),
                takedownsAfterGainingLevelAdvantage = part_chal.get('takedownsAfterGainingLevelAdvantage'),
                takedownsBeforeJungleMinionSpawn = part_chal.get('takedownsBeforeJungleMinionSpawn'),
                takedownsFirstXMinutes = part_chal.get('takedownsFirstXMinutes'),
                takedownsInAlcove = part_chal.get('takedownsInAlcove'),
                takedownsInEnemyFountain = part_chal.get('takedownsInEnemyFountain'),
                teamBaronKills = part_chal.get('teamBaronKills'),
                teamDamagePercentage = part_chal.get('teamDamagePercentage'),
                teamElderDragonKills = part_chal.get('teamElderDragonKills'),
                teamRiftHeraldKills = part_chal.get('teamRiftHeraldKills'),
                threeWardsOneSweeperCount = part_chal.get('threeWardsOneSweeperCount'),
                tookLargeDamageSurvived = part_chal.get('tookLargeDamageSurvived'),
                turretPlatesTaken = part_chal.get('turretPlatesTaken'),
                turretTakedowns = part_chal.get('turretTakedowns'),
                turretsTakenWithRiftHerald = part_chal.get('turretsTakenWithRiftHerald'),
                twentyMinionsIn3SecondsCount = part_chal.get('twentyMinionsIn3SecondsCount'),
                unseenRecalls = part_chal.get('unseenRecalls'),
                visionScoreAdvantageLaneOpponent = part_chal.get('visionScoreAdvantageLaneOpponent'),
                visionScorePerMinute = part_chal.get('visionScorePerMinute'),
                wardTakedowns = part_chal.get('wardTakedowns'),
                wardTakedownsBefore20M = part_chal.get('wardTakedownsBefore20M'),
                wardsGuarded = part_chal.get('wardsGuarded')
            )
            challenge_list.append(challenge)

        return (match_history, participant_list, challenge_list)


    def fetch_newest_matches_by_user(self, puuid:str) -> None:
        # Very time intensive function
        timestamp: int = self.get_newest_match_from_db()
        new_fetched_matches: List[str] = self.riot_api.get_match_list_by_timestamp(puuid=puuid, last_match_timestamp=timestamp)
        for matchId in new_fetched_matches:
            match_json = self.riot_api.get_match_data_as_json(matchId=matchId)
            match, participants, challenges = self.convert_match_json_to_orm(match_json)
            self.insert_match_into_db(match=match)
            for participant in participants:
                self.insert_participant_into_db(participant=participant)
            for challenge in challenges:
                self.insert_challenge_into_db(challenge=challenge)

    def get_all_matches_from_one_user(self, puuid: str) -> List[Participant]:
        response = self.session.query(Participant).filter(Participant.puuid == puuid).all()

    def get_alltime_stats_by_summoner_name(self, summoner_name: str) -> None:
        puuid = self.get_puuid_from_summoner_name_db(summoner_name=summoner_name)
        
        # matches = [match for match in match_list_db if ]

    