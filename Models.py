from modulefinder import replacePackageMap
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, Float, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///summoners4.db', echo = True)

class Summoner(Base):
    __tablename__ = 'summoner'
    puuid = Column('puuid', String, primary_key = True)
    groupId = Column(Integer, ForeignKey("group.id"))
    countryCode = Column(String)
    summonerName = Column(String)
    accountId = Column(String)
    profileIconId = Column(Integer)
    revisionDate = Column(Integer)
    summonerId = Column(String)
    summonerLevel = Column(Integer)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, onupdate=func.now())

    participant = relationship("Participant", back_populates="summoner")
    group = relationship("Group", back_populates="summoners")

    def __repr__(self):
        return f"<Summoner: {self.summonerName}>"

class Match(Base):
    __tablename__ = 'match'
    matchId = Column(String, primary_key = True)
    dataVersion = Column(String)
    participant_1 = Column(String) # puuid
    participant_2 = Column(String) # puuid
    participant_3 = Column(String) # puuid
    participant_4 = Column(String) # puuid
    participant_5 = Column(String) # puuid
    participant_6 = Column(String) # puuid
    participant_7 = Column(String) # puuid
    participant_8 = Column(String) # puuid
    participant_9 = Column(String) # puuid
    participant_10 = Column(String) # puuid
    gameCreation = Column(Integer)
    gameDuration = Column(Integer)
    gameEndTimestamp = Column(Integer)
    gameId = Column(Integer)
    gameMode = Column(String)
    gameName = Column(String)
    gameStartTimestamp = Column(Integer)
    gameType = Column(String)
    gameVersion = Column(String)
    mapId = Column(Integer)
    participants = Column(String) # complex field
    platformId = Column(String)
    queueId = Column(Integer)
    teams = Column(String) # List[TeamDTO]
    tournamentCode = Column(String)

    def __repr__(self):
        return f"<Match {self.matchId} played on {datetime.utcfromtimestamp(self.gameCreation).strftime('%Y-%m-%d %H:%M:%S')}>"

class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key = True, autoincrement = "auto")
    puuid = Column(String, ForeignKey("summoner.puuid"))
    matchId = Column(String, ForeignKey("match.matchId"))
    assists = Column(Integer)
    baronKills = Column(Integer)
    bountyLevel = Column(Integer)
    champExperience = Column(Integer)
    champLevel = Column(Integer)
    championId = Column(Integer)
    championName = Column(String)
    championTransform = Column(Integer)
    consumablesPurchased = Column(Integer)
    damageDealtToBuildings = Column(Integer)
    damageDealtToObjectives = Column(Integer)
    damageDealtToTurrets = Column(Integer)
    damageSelfMitigated = Column(Integer)
    deaths = Column(Integer)
    detectorWardsPlaced = Column(Integer)
    doubleKills = Column(Integer)
    dragonKills = Column(Integer)
    firstBloodAssist = Column(Boolean)
    firstBloodKill = Column(Boolean)
    firstTowerAssist = Column(Boolean)
    firstTowerKill = Column(Boolean)
    gameEndedInEarlySurrender = Column(Boolean)
    gameEndedInSurrender = Column(Boolean)
    goldEarned = Column(Integer)
    goldSpent = Column(Integer)
    individualPosition = Column(String)
    inhibitorKills = Column(Integer)
    inhibitorTakedowns = Column(Integer)
    inhibitorsLost = Column(Integer)
    item0 = Column(Integer)
    item1 = Column(Integer)
    item2 = Column(Integer)
    item3 = Column(Integer)
    item4 = Column(Integer)
    item5 = Column(Integer)
    item6 = Column(Integer)
    itemsPurchased = Column(Integer)
    killingSprees = Column(Integer)
    kills = Column(Integer)
    lane = Column(String)
    largestCriticalStrike = Column(Integer)
    largestKillingSpree = Column(Integer)
    largestMultiKill = Column(Integer)
    longestTimeSpentLiving = Column(Integer)
    magicDamageDealt = Column(Integer)
    magicDamageDealtToChampions = Column(Integer)
    magicDamageTaken = Column(Integer)
    neutralMinionsKilled = Column(Integer)
    nexusKills = Column(Integer)
    nexusTakedowns = Column(Integer)
    nexusLost = Column(Integer)
    objectivesStolen = Column(Integer)
    objectivesStolenAssists = Column(Integer)
    participantId = Column(Integer)
    pentaKills = Column(Integer)
    perks = Column(String) #Normally PerksDTO
    physicalDamageDealt = Column(Integer)
    physicalDamageDealtToChampions = Column(Integer)
    physicalDamageTaken = Column(Integer)
    profileIcon = Column(Integer)
    quadraKills = Column(Integer)
    riotIdName = Column(String)
    riotIdTagline = Column(String)
    role = Column(String)
    sightWardsBoughtInGame = Column(Integer)
    spell1Casts = Column(Integer)
    spell2Casts = Column(Integer)
    spell3Casts = Column(Integer)
    spell4Casts = Column(Integer)
    summoner1Casts = Column(Integer)
    summoner1Id = Column(Integer)
    summoner2Casts = Column(Integer)
    summoner2Id = Column(Integer)
    summonerId = Column(String)
    summonerLevel = Column(Integer)
    summonerName = Column(String)
    teamEarlySurrendered = Column(Boolean)
    teamId = Column(Integer)
    teamPosition = Column(String)
    timeCCingOthers = Column(Integer)
    timePlayed = Column(Integer)
    totalDamageDealt = Column(Integer)
    totalDamageDealtToChampions = Column(Integer)
    totalDamageShieldedOnTeammates = Column(Integer)
    totalDamageTaken = Column(Integer)
    totalHeal = Column(Integer)
    totalHealsOnTeammates = Column(Integer)
    totalMinionsKilled = Column(Integer)
    totalTimeCCDealt = Column(Integer)
    totalTimeSpentDead = Column(Integer)
    totalUnitsHealed = Column(Integer)
    tripleKills = Column(Integer)
    trueDamageDealt = Column(Integer)
    trueDamageDealtToChampions = Column(Integer)
    trueDamageTaken = Column(Integer)
    turretKills = Column(Integer)
    turretTakedowns = Column(Integer)
    turretsLost = Column(Integer)
    unrealKills = Column(Integer)
    visionScore = Column(Integer)
    visionWardsBoughtInGame = Column(Integer)
    wardsKilled = Column(Integer)
    wardsPlaced = Column(Integer)
    win = Column(Boolean)

    summoner = relationship("Summoner", back_populates="participant")

    def __repr__(self) -> str:
        return f"Summoner {self.summonerName} with PartId {self.participantId} played in {self.matchId} as {self.championName}."

class Challenge(Base):
    __tablename__ = 'challenge'
    id = Column(Integer, primary_key = True, autoincrement = "auto")
    puuid = Column(String, ForeignKey("summoner.puuid"))
    matchId = Column(String, ForeignKey("match.matchId"))

    abilityUses = Column(Integer)
    acesBefore15Minutes = Column(Integer)
    alliedJungleMonsterKills = Column(Float)
    baronTakedowns = Column(Integer)
    blastConeOppositeOpponentCount = Column(Integer)
    bountyGold = Column(Integer)
    buffsStolen = Column(Integer)
    completeSupportQuestInTime = Column(Integer)
    controlWardTimeCoverageInRiverOrEnemyHalf = Column(Float)
    controlWardsPlaced = Column(Integer)
    damagePerMinute = Column(Float)
    damageTakenOnTeamPercentage = Column(Float)
    dancedWithRiftHerald = Column(Integer)
    deathsByEnemyChamps = Column(Integer)
    dodgeSkillShotsSmallWindow = Column(Integer)
    doubleAces = Column(Integer)
    dragonTakedowns = Column(Integer)
    earlyLaningPhaseGoldExpAdvantage = Column(Integer)
    effectiveHealAndShielding = Column(Integer)
    elderDragonKillsWithOpposingSoul = Column(Integer)
    elderDragonMultikills = Column(Integer)
    enemyChampionImmobilizations = Column(Integer)
    enemyJungleMonsterKills = Column(Integer)
    epicMonsterKillsNearEnemyJungler = Column(Integer)
    epicMonsterKillsWithin30SecondsOfSpawn = Column(Integer)
    epicMonsterSteals = Column(Integer)
    epicMonsterStolenWithoutSmite = Column(Integer)
    firstTurretKilledTime = Column(Float)
    flawlessAces = Column(Integer)
    fullTeamTakedown = Column(Integer)
    gameLength = Column(Float)
    getTakedownsInAllLanesEarlyJungleAsLaner = Column(Integer)
    goldPerMinute = Column(Float)
    hadOpenNexus = Column(Integer)
    immobilizeAndKillWithAlly = Column(Integer)
    initialBuffCount = Column(Integer)
    initialCrabCount = Column(Integer)
    jungleCsBefore10Minutes = Column(Float)
    junglerTakedownsNearDamagedEpicMonster = Column(Integer)
    kTurretsDestroyedBeforePlatesFall = Column(Integer)
    kda = Column(Float)
    killAfterHiddenWithAlly = Column(Integer)
    killedChampTookFullTeamDamageSurvived = Column(Integer)
    killsNearEnemyTurret = Column(Integer)
    killsOnOtherLanesEarlyJungleAsLaner = Column(Integer)
    killsOnRecentlyHealedByAramPack = Column(Integer)
    killsUnderOwnTurret = Column(Integer)
    killsWithHelpFromEpicMonster = Column(Integer)
    knockEnemyIntoTeamAndKill = Column(Integer)
    landSkillShotsEarlyGame = Column(Integer)
    laneMinionsFirst10Minutes = Column(Integer)
    laningPhaseGoldExpAdvantage = Column(Integer)
    legendaryCount = Column(Integer)
    lostAnInhibitor = Column(Integer)
    maxCsAdvantageOnLaneOpponent = Column(Integer)
    maxKillDeficit = Column(Integer)
    maxLevelLeadLaneOpponent = Column(Integer)
    moreEnemyJungleThanOpponent = Column(Float)
    multiKillOneSpell = Column(Integer)
    multiTurretRiftHeraldCount = Column(Integer)
    multikills = Column(Integer)
    multikillsAfterAggressiveFlash = Column(Integer)
    mythicItemUsed = Column(Integer)
    outerTurretExecutesBefore10Minutes = Column(Integer)
    outnumberedKills = Column(Integer)
    outnumberedNexusKill = Column(Integer)
    perfectDragonSoulsTaken = Column(Integer)
    perfectGame = Column(Integer)
    pickKillWithAlly = Column(Integer)
    playedChampSelectPosition = Column(Integer)
    poroExplosions = Column(Integer)
    quickCleanse = Column(Integer)
    quickFirstTurret = Column(Integer)
    quickSoloKills = Column(Integer)
    riftHeraldTakedowns = Column(Integer)
    saveAllyFromDeath = Column(Integer)
    scuttleCrabKills = Column(Integer)
    skillshotsDodged = Column(Integer)
    skillshotsHit = Column(Integer)
    snowballsHit = Column(Integer)
    soloBaronKills = Column(Integer)
    soloKills = Column(Integer)
    stealthWardsPlaced = Column(Integer)
    survivedSingleDigitHpCount = Column(Integer)
    survivedThreeImmobilizedInFight = Column(Integer)
    takedownOnFirstTurret = Column(Integer)
    takedowns = Column(Integer)
    takedownsAfterGainingLevelAdvantage = Column(Integer)
    takedownsBeforeJungleMinionSpawn = Column(Integer)
    takedownsFirstXMinutes = Column(Integer)
    takedownsInAlcove = Column(Integer)
    takedownsInEnemyFountain = Column(Integer)
    teamBaronKills = Column(Integer)
    teamDamagePercentage = Column(Float)
    teamElderDragonKills = Column(Integer)
    teamRiftHeraldKills = Column(Integer)
    threeWardsOneSweeperCount = Column(Integer)
    tookLargeDamageSurvived = Column(Integer)
    turretPlatesTaken = Column(Integer)
    turretTakedowns = Column(Integer)
    turretsTakenWithRiftHerald = Column(Integer)
    twentyMinionsIn3SecondsCount = Column(Integer)
    unseenRecalls = Column(Integer)
    visionScoreAdvantageLaneOpponent = Column(Float)
    visionScorePerMinute = Column(Float)
    wardTakedowns = Column(Integer)
    wardTakedownsBefore20M = Column(Integer)
    wardsGuarded = Column(Integer)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)
    founderPuuid = Column(String) #aka puuid
    icon_blob = Column(BLOB)
    createdAt = Column(DateTime, server_default=func.now())

    summoners = relationship("Summoner", back_populates="group")

    def __repr__(self) -> str:
        return f"Group {self.name} "





Base.metadata.create_all(engine)