from src.betboom_parse.utils import hash_decoder


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