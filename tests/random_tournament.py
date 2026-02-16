from trf import Game, Player, Tournament, DeprecatedTeam
import random
import string

MAX_NAME_SIZE = 30
MAX_FED_SIZE = 3
MAX_ID = 9999999999
MAX_XX_FIELDS_SIZE = 5


def latin(size: int, space: bool = True) -> str:
    return ''.join(random.choice(string.ascii_letters + (' ' if space else ''))
                   for _ in range(size)).strip()


def points(players) -> float:
    return min(99.5, random.randint(0, players*2) / 2)


def date() -> str:
    y = random.randint(1900, 3000)
    m = random.randint(1, 12)
    d = random.randint(1, 31)
    return f'{y:04}/{m:02}/{d:02}'


def game(players: int) -> Game:
    sr = random.randint(0, players)
    cl = random.choice('wb-')
    re = random.choice('-+WDL1=0HFUZwdlhfuz')
    return Game(opponent_id=sr, color=cl, result=re, round=0)


def games(players: int):
    size = random.randint(0, players-1)
    gs = [game(players) for _ in range(size)]
    for i, g in enumerate(gs):
        g.round = i+1
    return gs


def player(players) -> Player:
    sr = random.randint(0, players)
    name = latin(MAX_NAME_SIZE)
    sex = random.choice('mwMW')
    title = random.choice(['', 'GM', 'IM', 'WG', 'FM',
                          'WI', 'CM', 'WF', 'WC'])
    rating = random.randint(0, 3000)
    fed = latin(MAX_FED_SIZE)
    fide_id = random.randint(0, MAX_ID)
    bd = date()
    pts = points(players)
    rank = random.randint(0, players)
    gs = games(players)
    return Player(id=sr, name=name, sex=sex,
                  title=title, rating=rating,
                  federation=fed, fide_id=fide_id, birth_date=bd,
                  points=pts, rank=rank, games=gs)


def round_dates(players: int):
    size = random.randint(0, players)
    return [date() for _ in range(size)]


def xx_fields():
    size = random.randint(0, MAX_XX_FIELDS_SIZE)
    return {'XX'+latin(1, space=False): latin(MAX_NAME_SIZE)
            for _ in range(size)}


def tournament(players) -> Tournament:
    name = latin(MAX_NAME_SIZE)
    city = latin(MAX_NAME_SIZE)
    fed = latin(MAX_NAME_SIZE)
    sd = date()
    ed = date()
    np = players
    nrp = random.randint(0, players-1)
    nt = random.randint(0, players-1)
    type = latin(MAX_NAME_SIZE)
    ca = latin(MAX_NAME_SIZE)
    dca = latin(MAX_NAME_SIZE)
    rop = latin(MAX_NAME_SIZE)
    rd = round_dates(players)
    ps = [player(players) for _ in range(players)]
    xx = xx_fields()
    return Tournament(name=name, city=city, federation=fed, start_date=sd,
                      end_date=ed, num_players=np, num_rated_players=nrp,
                      num_teams=nt, type=type, chief_arbiter=ca,
                      deputy_arbiters=[dca], allotted_time=rop, round_dates=rd,
                      players=ps, xx_fields=xx)
