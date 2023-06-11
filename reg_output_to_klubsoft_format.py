import csv
import os
from datetime import datetime
from download_images_from_iicanada import download_images
from download_images_from_iicanada import Player, Team

base_folder = "2023"

input_file = f'{base_folder}/gold_cup_2023__team_registration.csv'

# Indexes at which the data begins. The Indexes before this are not useful.
column_start_index = 9
row_start_index = 3

# Create a list to store the processed data
processed_data = []

data_dir_for_teams_to_validate = []

teams = list[Team]()


def convert_date_of_birth(date_str):
    # check the input format
    if '/' in date_str:
        # convert from '%m/%d/%Y' format to '%Y/%m/%d' format
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        new_date_str = datetime.strftime(date_obj, '%Y/%m/%d')
    elif '-' in date_str:
        # convert from '%Y-%m-%d' format to '%Y/%m/%d' format
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = datetime.strftime(date_obj, '%Y/%m/%d')
    else:
        # invalid format
        raise ValueError(f"Invalid date format for {date_str}. Use either '%m/%d/%Y' or '%Y-%m-%d'.")
    return new_date_str


# Read the input CSV file
with open(input_file, 'r') as file:
    reader = csv.reader(file)

    # Skip useless rows
    for row in range(row_start_index):
        next(reader)

    for row in reader:
        row = row[column_start_index:]
        # Extract the required values from the input row
        team_name = row[0]
        category = row[1]
        region = row[2]
        is_tm_player_coach = row[3]
        tm_player_coach = row[4]
        team_manager_full_name = row[5]
        team_manager_date_of_birth = row[6]
        team_manager_email_address = row[7]
        team_manager_phone_number = row[8]
        num_coaches = 2
        coaches = []
        for i in range(10, 10 + int(num_coaches) * 5, 5):
            coach_full_name = row[i]
            coach_date_of_birth = row[i + 1]
            coach_email_address = row[i + 2]
            coach_phone_number = row[i + 3]
            is_certified = row[i + 4]
            headshot = row[i + 12]
            govt_id = row[i + 14]
            waiver = row[i + 16]
            coaches.append({
                'Full Name': coach_full_name,
                'Date of Birth': coach_date_of_birth,
                'Email Address': coach_email_address,
                'Phone Number': coach_phone_number,
                'Is Certified': is_certified
            })

        first_player_index = 42
        players = list[Player]()
        for i in range(first_player_index, len(row) - 18, 19):
            player_full_name = row[i]
            player_date_of_birth = row[i + 1]
            player_email_address = row[i + 2]
            player_phone_number = row[i + 3]
            headshot = row[i + 13]
            govt_id = row[i + 15]
            waiver = row[i + 17]
            if player_full_name not in ['', 'X']:
                player = Player(
                    full_name=player_full_name,
                    dob=convert_date_of_birth(player_date_of_birth),
                    email_address=player_email_address,
                    headshot=headshot,
                    govt_id=govt_id
                )
                players.append(player)
                # print(vars(player))
        # Create a dictionary to store the processed data for this row
        processed_row = {
            'Team Name': team_name,
            'Category': category,
            'Region': region,
            'Is TM Player/Coach': is_tm_player_coach,
            'TM Player/Coach': tm_player_coach,
            'Team Manager Full Name': team_manager_full_name,
            'Team Manager Date of Birth': team_manager_date_of_birth,
            'Team Manager Email Address': team_manager_email_address,
            'Team Manager Phone Number': team_manager_phone_number,
            'Coaches': coaches,
            'Players': players
        }
        # Append the processed row to the list of processed data
        processed_data.append(processed_row)

        team = Team(name=team_name, category=category, players=players)
        teams.append(team)

        data_dir_for_teams_to_validate.append(f'{base_folder}/{team_name}-{category}')

        output_file = f'{base_folder}/{team_name}-{category}/{team_name}-{category}-output.csv'

        if not os.path.exists(f"{base_folder}/{team_name}-{category}"):
            os.makedirs(f"{base_folder}/{team_name}-{category}")
            print(f"{team_name}")

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(['Teamname', 'TeamShortName', 'PlayerName', 'email'])
            for player in players:
                player_full_name = player.full_name

                writer.writerow([team.name, 'FCB', player.full_name, player.email_address])

download_images(teams=teams)
