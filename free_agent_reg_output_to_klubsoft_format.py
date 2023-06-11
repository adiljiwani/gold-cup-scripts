import csv
import os
from datetime import datetime
from download_images_from_iicanada import download_images
from download_images_from_iicanada import Player, Team

base_folder = "2023"

input_file = f'{base_folder}/gold_cup_2023__girls_15_17_player_registration.csv'

# Indexes at which the data begins. The Indexes before this are not useful.
column_start_index = 9
row_start_index = 3

# Create a list to store the processed data
processed_data = []

data_dir_for_teams_to_validate = []

players = list[Player]()


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

    players = list[Player]()
    for row in reader:
        row = row[column_start_index:]
        # Extract the required values from the input row
        player_full_name = row[0]
        category = "Girls 15-17"
        player_date_of_birth = row[1]
        player_email_address = row[2]
        player_phone_number = row[3]
        headshot = row[13]
        govt_id = row[15]
        player = Player(
            full_name=player_full_name,
            dob=convert_date_of_birth(player_date_of_birth),
            email_address=player_email_address,
            headshot=headshot,
            govt_id=govt_id
        )
        players.append(player)
        print(vars(player))

        team_name = "Free Agents"
        output_file = f'{base_folder}/{team_name}-{category}/{team_name}-{category}-output.csv'

        if not os.path.exists(f"{base_folder}/{team_name}-{category}"):
            os.makedirs(f"{base_folder}/{team_name}-{category}")

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(['Teamname', 'TeamShortName', 'PlayerName', 'email'])
            for player in players:
                player_full_name = player.full_name

                writer.writerow(["Free Agent", 'FCB', player.full_name, player.email_address])

team = Team(team_name, category, players)
download_images(teams=[team])
