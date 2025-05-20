import requests
from bs4 import BeautifulSoup
import json

url = 'https://p1.trrsf.com/api/musa-soccer/ms-standings-games-light?idChampionship=1436&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
}

res = requests.get(url, headers=headers)

if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')

    rounds = soup.select('ul.rounds > li.round')
    all_rounds = []

    for round_li in rounds:
        round_title = round_li.find('h3', class_='header-round').get_text(strip=True)
        matches = round_li.select('ul > li.match')
        games = []

        for match in matches:
            try:
                home_team = match.select_one('a.shield.home').get('title')
                away_team = match.select_one('a.shield.away').get('title')

                home_goals = match.select_one('strong.goals.home').get_text(strip=True)
                away_goals = match.select_one('strong.goals.away').get_text(strip=True)

                date_time = match.select_one('strong.time.sports-date-gmt').get_text(strip=True)
                stadium = match.select_one('span.stadium').get_text(strip=True)

                games.append({
                    'mandante': home_team,
                    'visitante': away_team,
                    'placar': f'{home_goals} x {away_goals}',
                    'data_hora': date_time,
                    'estadio': stadium
                })
            except AttributeError:
                # Caso algum dado esteja ausente, o jogo é ignorado
                continue

        all_rounds.append({
            'rodada': round_title,
            'jogos': games
        })

    # Exibe o resultado em formato JSON
    print(json.dumps(all_rounds, indent=2, ensure_ascii=False))

else:
    print(f"Erro ao acessar a página: {res.status_code}")
