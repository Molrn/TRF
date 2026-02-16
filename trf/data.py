from collections import defaultdict
from functools import cached_property

from dataclasses import dataclass, field


@dataclass
class Game(object):
    opponent_id: int | None
    color: str
    result: str
    round: int


@dataclass
class NationalPlayer(object):
    player_id: int
    name: str = ''
    sex: str = ''
    classification: str = ''
    rating: int = 0
    origin: str = ''
    national_id: str = ''
    birth_date: str = ''


@dataclass
class Player(object):
    id: int
    name: str = ''
    sex: str = 'm'
    title: str = ''
    rating: int = 0
    federation: str = ''
    fide_id: int | None = None
    birth_date: str = ''
    points: float = 0
    rank: int | None = None
    games: list[Game] = field(default_factory=list)
    national_player_by_federation: dict = field(default_factory=dict)


@dataclass
class Team(object):
    id: int = 0
    name: str = ''
    nickname: str = ''
    strength_factor: int = 0
    match_points: float = 0.0
    game_points: float = 0.0
    rank: int | None = None
    player_ids: list[int] = field(default_factory=list)


@dataclass
class DeprecatedTeam(object):
    name: str = ''
    player_ids: list[int] = field(default_factory=list)


@dataclass
class RoundBye(object):
    type: str
    round: int
    pairing_numbers: list[int]


@dataclass
class AcceleratedRound(object):
    match_points: float | None
    game_points: float | None
    first_round: int
    last_round: int | None
    first_id: int
    last_id: int


@dataclass
class ProhibitedPairing(object):
    first_round: int
    last_round: int | None
    pairing_numbers: list[int]


@dataclass
class TeamPABs(object):
    match_points: float | None
    game_points: float
    team_id_by_round: dict[int, int]


@dataclass
class TeamForfeitedMatch(object):
    type: str
    round: int
    white_team_id: int
    black_team_id: int


@dataclass
class OOdOTeamPairing(object):
    round: int
    team_id: int
    opponent_team_id: int
    boards: list[int | None]


@dataclass
class AbnormalPointsAssignment(object):
    type: str
    match_points: float
    game_points: float | None
    round: int | None
    pairing_numbers: list[int | None]


@dataclass
class Tournament(object):
    name: str = ''
    city: str = ''
    federation: str = ''
    start_date: str = ''
    end_date: str = ''
    num_players: int = 0
    num_rated_players: int = 0
    num_teams: int = 0
    type: str = ''
    encoded_type: str = ''
    chief_arbiter: str = ''
    deputy_arbiters: list[str] = field(default_factory=list)
    allotted_time: str = ''
    time_control: str = ''
    round_dates: list[str] = field(default_factory=list)
    num_rounds: int = 0
    initial_color: str = ''
    individuals_point_system: dict[str, float] = field(default_factory=dict)
    teams_point_system: dict[str, float] = field(default_factory=dict)
    starting_rank_method: str = ''
    pairing_controller_id: str = ''
    tie_breaks: list[str] = field(default_factory=list)
    standings_tie_breaks: list[str] = field(default_factory=list)
    board_color_sequence: str = ''

    teams: list[Team] = field(default_factory=list)
    deprecated_teams: list[DeprecatedTeam] = field(default_factory=list)
    players: list[Player] = field(default_factory=list)
    accelerated_rounds: list[AcceleratedRound] = field(default_factory=list)
    prohibited_pairings: list[ProhibitedPairing] = field(default_factory=list)
    round_byes: list[RoundBye] = field(default_factory=list)
    team_pabs: TeamPABs | None = None
    team_forfeited_matches: list[TeamForfeitedMatch] = field(default_factory=list)
    oodo_team_pairings: list[OOdOTeamPairing] = field(default_factory=list)
    abnormal_points_assignments: list[AbnormalPointsAssignment] = field(default_factory=list)
    informative_team_pairings_records: list[str] = field(default_factory=list)
    informative_team_results_records: list[str] = field(default_factory=list)


    xx_fields: dict[str, str] = field(default_factory=dict)
    bb_fields: dict[str, str] = field(default_factory=dict)

    @property
    def num_rounds_estimation(self):
        """An estimation of how many rounds where played in this tournament."""

        if self.num_rounds:
            return self.num_rounds

        if 'XXR' in self.xx_fields:
            return int(self.xx_fields['XXR'])

        if self.round_dates:
            return len(self.round_dates)

        return max(len(p.games) for p in self.players) or len(self.players)-1

    @cached_property
    def national_players_by_federation(self) -> dict[str, list[NationalPlayer]]:
        players_by_federation: dict[str, list[NationalPlayer]] = defaultdict(list)
        for player in self.players:
            for federation, national_player in player.national_player_by_federation.items():
                players_by_federation[federation].append(national_player)
        return players_by_federation
