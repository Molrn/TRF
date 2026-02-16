from .entry import ENTRIES, NationalPlayerEntry
from .data import (
    AcceleratedRound,
    DeprecatedTeam,
    Game,
    NationalPlayer,
    Player,
    ProhibitedPairing,
    Team,
    Tournament,
    RoundBye,
    TeamPABs,
    TeamForfeitedMatch,
    OOdOTeamPairing,
    AbnormalPointsAssignment,
)
from .exception import TrfException
import io


def dump(fp, tournament: Tournament):
    """Dumps the tournament and saves the trf in the file fp points to"""

    _dump_tournament(fp, tournament)


def dumps(tournament: Tournament) -> str:
    """Dumps the tournament and returns the trf"""

    fp = io.StringIO()
    _dump_tournament(fp, tournament)
    return fp.getvalue()


def load(fp) -> Tournament:
    """Parses the trf file fp points to and returns it as a tournament"""

    return _parse_tournament(fp.readlines())


def loads(s: str) -> Tournament:
    """Parses the trf in s and returns it as a tournament"""

    return _parse_tournament(s.split('\n'))


def _dump_tournament(fp, tournament):
    for entry_ in ENTRIES:
        entry_.dump(fp, tournament)

    for federation, national_players in tournament.national_players_by_federation.items():
        NationalPlayerEntry(federation).dump(fp, tournament)

    for field, value in tournament.xx_fields.items():
        fp.write(f'{field} {value}\n')

    for field, value in tournament.bb_fields.items():
        fp.write(f'{field} {value}\n')


_FEDERATIONS = [
    'AFG', 'ALB', 'ALG', 'AND', 'ANG', 'ANT', 'ARG', 'ARM', 'ARU', 'AUS', 'AUT',
    'AZE', 'BAH', 'BRN', 'BAN', 'BAR', 'BLR', 'BEL', 'BIZ', 'BER', 'BHU', 'BOL',
    'BIH', 'BOT', 'BRA', 'BRU', 'BUL', 'BUR', 'BDI', 'CAM', 'CMR', 'CAN', 'CPV',
    'CAY', 'CAF', 'CHA', 'CHI', 'CHN', 'CGO', 'COL', 'COM', 'CRC', 'CIV', 'CRO',
    'CUB', 'CYP', 'CZE', 'COD', 'DEN', 'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'ESA',
    'ENG', 'GEQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FAI', 'FIJ', 'FIN', 'FRA', 'GAB',
    'GAM', 'GEO', 'GER', 'GHA', 'GRE', 'GRL', 'GRN', 'GUM', 'GUA', 'GCI', 'GUY',
    'HAI', 'HON', 'HKG', 'HUN', 'ISL', 'IND', 'INA', 'IRI', 'IRQ', 'IRL', 'IOM',
    'ISR', 'ITA', 'IVB', 'JAM', 'JPN', 'JCI', 'JOR', 'KAZ', 'KEN', 'KOS', 'KUW',
    'KGZ', 'LAO', 'LAT', 'LBN', 'LES', 'LBR', 'LBA', 'LIE', 'LTU', 'LUX', 'MAC',
    'MAD', 'MAW', 'MAS', 'MDV', 'MLI', 'MLT', 'MTN', 'MRI', 'MEX', 'MDA', 'MNC',
    'MGL', 'MNE', 'MAR', 'MOZ', 'MYA', 'NAM', 'NRU', 'NEP', 'NED', 'AHO', 'NCL',
    'NZL', 'NCA', 'NIG', 'NGR', 'MKD', 'NOR', 'OMA', 'PAK', 'PLW', 'PLE', 'PAN',
    'PNG', 'PAR', 'PER', 'PHI', 'POL', 'POR', 'PUR', 'QAT', 'ROU', 'RUS', 'RWA',
    'SKN', 'LCA', 'VIN', 'SMR', 'STP', 'KSA', 'SCO', 'SEN', 'SRB', 'SEY', 'SLE',
    'SGP', 'SVK', 'SLO', 'SOL', 'SOM', 'RSA', 'KOR', 'SSD', 'ESP', 'SRI', 'SUD',
    'SUR', 'SWE', 'SUI', 'SYR', 'TJK', 'TAN', 'THA', 'TLS', 'TOG', 'TGA', 'TPE',
    'TTO', 'TUN', 'TUR', 'TKM', 'UGA', 'UKR', 'UAE', 'USA', 'URU', 'ISV', 'UZB',
    'VAN', 'VEN', 'VIE', 'WLS', 'YEM', 'ZAM', 'ZIM',
]


def _parse_tournament(lines):
    tournament = Tournament()

    for line in lines:
        for entry_ in ENTRIES:
            if line.startswith(entry_.din + ' '):
                entry_.load(tournament, line[4:])
                break

        din = line[:3]
        if din in _FEDERATIONS:
            NationalPlayerEntry(din).load(tournament, line[4:])

        if line.startswith('XX'):
            field, value = line.split(' ', 1)
            tournament.xx_fields[field] = value.strip()
            
        elif line.startswith('BB'):
            field, value = line.split(' ', 1)
            tournament.bb_fields[field] = value.strip()

    return tournament
