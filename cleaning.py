import pandas as pd
import csv

with open('nba_player_dataset/Player_Per_Game.csv', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
data = pd.DataFrame(data[1:], columns=data[0])

data['season'] = pd.to_numeric(data['season'], errors='coerce')
data['mp_per_game'] = pd.to_numeric(data['mp_per_game'], errors='coerce')
data['pts_per_game'] = pd.to_numeric(data['pts_per_game'], errors='coerce')
data['ast_per_game'] = pd.to_numeric(data['ast_per_game'], errors='coerce')
data['trb_per_game'] = pd.to_numeric(data['trb_per_game'], errors='coerce')
data['g'] = pd.to_numeric(data['g'], errors='coerce')

data = data.loc[data['season'] >= 2000]
data = data.loc[data['mp_per_game'] >= 20.0]
data = data.loc[data['g'] >= 40]
data = data[['season','player','team','pos','mp_per_game','pts_per_game','ast_per_game','trb_per_game','g']]
data = data.dropna()

season_data = data.copy()
season_data["impact_score"] = (data["pts_per_game"] + data["ast_per_game"] + data["trb_per_game"]) / data["mp_per_game"]

career_data = data.groupby(['player'])[['pts_per_game', 'ast_per_game', 'trb_per_game', 'mp_per_game']].mean().reset_index()
career_data["impact_score"] = (career_data["pts_per_game"] + career_data["ast_per_game"] + career_data["trb_per_game"]) / career_data["mp_per_game"]

career_position_data = data.groupby(['pos'])[['pts_per_game', 'ast_per_game', 'trb_per_game', 'mp_per_game']].mean().reset_index()
career_position_data["impact_score"] = (career_position_data["pts_per_game"] + career_position_data["ast_per_game"] + career_position_data["trb_per_game"]) / career_position_data["mp_per_game"]

# print(data.head()) 

cols = ['mp_per_game', 'pts_per_game', 'ast_per_game', 'trb_per_game', 'impact_score']
season_data[cols] = season_data[cols].round(3)

cols_career = ['mp_per_game', 'pts_per_game', 'ast_per_game', 'trb_per_game', 'impact_score']
career_data[cols_career] = career_data[cols_career].round(3)

cols_position = ['mp_per_game', 'pts_per_game', 'ast_per_game', 'trb_per_game', 'impact_score']
career_position_data[cols_position] = career_position_data[cols_position].round(3)

season_data.to_csv('season_data.csv', index=False)
career_data.to_csv('career_data.csv', index=False)
career_position_data.to_csv('career_position_data.csv', index=False)

best_season = season_data.groupby('player')['impact_score'].max().reset_index()
best_season.columns = ['player', 'best_season_impact']

comparison = career_data[['player', 'impact_score']].rename(columns={'impact_score': 'career_avg_impact'})
comparison = comparison.merge(best_season, on='player')

comparison.to_csv('comparison_data.csv', index=False)