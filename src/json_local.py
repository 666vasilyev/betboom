from src.utils import hash_decoder


def get_json_for_all_matches(sport_id: int):
    return {
    'operationName': 'allMatch',
    'variables': {
        'first': 20,
        'liveOnly': False,
        'historic': False,
        'favourites': None,
        'sports': [
            f'{hash_decoder(f"sport/od:sport:{sport_id}")}', 
        ],
    },
    'extensions': {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': 'fe60acf530a627da8bd6f6578b1119a3e1e7cbc6abbb2a72497591a68cdfec20',
        },
    },
}

# TODO: убрать odds и extensions и проверить работает или нет
def get_application_json(match_id: int, winner: int, odd: float) -> dict:
    return {
    'operationName': 'ticketRestrictions',
    'variables': {
        'ticket': {
            'bets': [
                {
                    'stake': 10,
                    'selections': [
                        {
                            'outcomeId': hash_decoder(f'outcome/od:match:{match_id}/1|variant=way:two/1-variant=way:two|way=two/{winner}'),
                            'odds': odd,
                            'marketInfo': None,
                        },
                    ],
                    'systems': [
                        1,
                    ],
                    'bonuses': [],
                },
            ],
            'oddsChanges': 'NONE',
            'currency': 'RUB',
        },
    },
    'extensions': {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': 'de032391f8b72ecb4a2d916aa564800b8b0b05a913b54439d8859d6487ce931d',
        },
    },
}
def get_confirmation_json(match_id: int, winner: int, odd: float) -> dict:
    return {
    'operationName': 'acceptTicket',
    'variables': {
        'input': {
            'bets': [
                {
                    'stake': 10,
                    'selections': [
                        {
                            'outcomeId': hash_decoder(f'outcome/od:match:{match_id}/1|variant=way:two/1-variant=way:two|way=two/{winner}'),
                            'odds': odd,
                            'marketInfo': None,
                        },
                    ],
                    'systems': [
                        1,
                    ],
                    'bonuses': [],
                },
            ],
            'oddsChanges': 'NONE',
            'currency': 'RUB',
        },
    },
    'extensions': {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': '65797a92ea49abf3d26dcbc8efab4c1f747b8b273645dab83a486853c83bb260',
        },
    },
}