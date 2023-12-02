api_key = 'b94ac61d-b060-4892-8242-923bf2303a38' # <- apiKey <- важная вещь, передается в hedaers  -> x-api-key
auth = '7d940184-0c2d-47c9-a423-165f91042421' # <- authorization <- нужная вещь, передается в headers -> authorization, меняется(неизвестно как и когда)


headers = {
    'authority': 'api-bifrost.oddin.gg',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'authorization': auth,
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://bifrost.oddin.gg',
    'referer': 'https://bifrost.oddin.gg/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-api-key': api_key,
    'x-display-resolution': '590x826',
    'x-locale': 'RU',
    'x-sbi': '690823c0-742f-4c4d-8e1e-2706fd98378e',
}
