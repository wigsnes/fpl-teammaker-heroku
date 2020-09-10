import streamlit as st
import pandas as pd
from fpl import predict_team, get_overview_data, extract_player_roster, \
extract_teams_data, extract_player_types

pd.options.display.float_format = "{:,.2f}".format

def get_team_limit(max_players_from_team):
	max_players_from_team['ARS'] = int(st.text_input('ARS:', 3))
	max_players_from_team['AVL'] = int(st.text_input('AVL:', 3))
	max_players_from_team['BHA'] = int(st.text_input('BHA:', 3))
	max_players_from_team['BUR'] = int(st.text_input('BUR:', 3))
	max_players_from_team['CHE'] = int(st.text_input('CHE:', 3))
	max_players_from_team['CRY'] = int(st.text_input('CRY:', 3))
	max_players_from_team['EVE'] = int(st.text_input('EVE:', 3))
	max_players_from_team['FUL'] = int(st.text_input('FUL:', 3))
	max_players_from_team['LEE'] = int(st.text_input('LEE:', 3))
	max_players_from_team['LEI'] = int(st.text_input('LEI:', 3))
	max_players_from_team['LIV'] = int(st.text_input('LIV:', 3))
	max_players_from_team['MCI'] = int(st.text_input('MCI:', 3))
	max_players_from_team['MUN'] = int(st.text_input('MUN:', 3))
	max_players_from_team['NEW'] = int(st.text_input('NEW:', 3))
	max_players_from_team['SHU'] = int(st.text_input('SHU:', 3))
	max_players_from_team['SOU'] = int(st.text_input('SOU:', 3))
	max_players_from_team['TOT'] = int(st.text_input('TOT:', 3))
	max_players_from_team['WBA'] = int(st.text_input('WBA:', 3))
	max_players_from_team['WHU'] = int(st.text_input('WHU:', 3))
	max_players_from_team['WOL'] = int(st.text_input('WOL:', 3))

	return max_players_from_team


st.markdown("<h1 style='text-align: center;'>Welcome to FPL TeamMaker</h1>", \
			unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Use Data Science to build your \
			team and win!</h3>", unsafe_allow_html=True)

transfer = False
wildcard = False
gw = 1
budget = 1000
old_data_weight = 0.4
new_data_weight = 0.6
form_weight = 0.5
max_players_from_team = {}
current_team = []
num_transfers = 1


gw = int(st.text_input('Enter the Gameweek you want to make team for:', '1'))
if gw == 1:
	st.write('Starting below, please provide how many players you want from each team.\
		Use this in cases when a particular team does not have a fixture for the week.')
	max_players_from_team = get_team_limit(max_players_from_team)

elif gw > 1 and gw <= 4:
	transfer_or_wildcard = st.radio('Select your mode of team making:', ('Transfer',\
								'New Team / Wildcard'))
	if transfer_or_wildcard == 'Transfer':
		transfer = True
	else:
		wildcard = True

	old_data_weight = float(st.text_input('Enter the weight you want to give to last \
								season\'s  data (0-1.0):', 0.4))
	new_data_weight = float(st.text_input('Enter the weight you want to give to current \
								season\'s  data (0-1.0):', 0.6))
	form_weight = float(st.text_input('Enter the weight you want to give to player form \
							(0-1.0):', 0.5))
	budget = float(st.text_input('Enter your budget x 10 (For transfers, enter \
								 the leftover budget using current team):', 1000))

	if transfer:
		num_transfers = int(st.text_input('Enter the number of transfers to be made:', 1))
		overview_data_json = get_overview_data()
		teams_df = extract_teams_data(overview_data_json)
		player_types_df = extract_player_types(overview_data_json)
		player_df = extract_player_roster(overview_data_json, player_types_df, teams_df)
		player_df = player_df[['code', 'first_name', 'second_name', 'team_code']]
		players = st.write('Please look at the list below and enter a comma \
								 separated list of player codes you have in your team. \
								 Note that they are ordered alphabetically by team name.', \
								 player_df)
		current_team = st.text_input('')
		current_team = list(map(int, current_team.split(',')))

	else:
		st.write('Starting below, please provide how many players you want from each team.\
		Use this in cases when a particular team does not have a fixture for the week.')
		max_players_from_team = get_team_limit(max_players_from_team)

else:
	transfer_or_wildcard = st.radio('Select your mode of team making:', ('Transfer',\
								'New Team / Wildcard'))
	if transfer_or_wildcard == 'Transfer':
		transfer = True
	else:
		wildcard = True


	form_weight = float(st.text_input('Enter the weight you want to give to player form \
							(0-1.0):', 0.5))
	budget = float(st.text_input('Enter your budget x 10 (For transfers, enter \
								 the leftover budget using current team):', 1000))

	if transfer:
		num_transfers = int(st.text_input('Enter the number of transfers to be made:', 1))
		overview_data_json = get_overview_data()
		teams_df = extract_teams_data(overview_data_json)
		player_types_df = extract_player_types(overview_data_json)
		player_df = extract_player_roster(overview_data_json, player_types_df, teams_df)
		player_df = player_df[['code', 'first_name', 'second_name', 'team_code']]
		players = st.write('Please look at the list below and enter a comma \
								 separated list of player codes you have in your team. \
								 Note that they are ordered alphabetically by team name.', \
								 player_df)
		current_team = st.text_input('')
		current_team = list(map(int, current_team.split(',')))

	else:
		st.write('Starting below, please provide how many players you want from each team.\
		Use this in cases when a particular team does not have a fixture for the week.')
		max_players_from_team = get_team_limit(max_players_from_team)

if st.button('Get Team'):
	team, points, cost = predict_team(transfer, wildcard, gw, budget, old_data_weight, \
				 new_data_weight, form_weight, max_players_from_team, \
				 current_team, num_transfers)
	team['Cost'] /= 10
	team = team.rename(columns = {"First": "First Name", "Second": "Second Name"})
	st.write(team)
	st.write('Potential points of whole team:', points)
	st.write('Cost of the team:', cost)
