from id_validator.main import IDValidator
import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.styles import Font
import csv
import os

base_folder = "2023"

TITLE_ROW_HEIGHT = 50
DEFAULT_COLUMN_WIDTH = 40
FONT_SIZE = 25
IMAGE_DIMENSION = 400


def get_name_and_dob_for_player(info_file) -> [str, str]:
    with open(info_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        name = rows[0][0]
        dob = rows[1][0]
        return name, dob


def get_emails(info_file) -> [str]:
    emails = []
    with open(info_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            emails.append(row[3])
    return emails


class TeamValidator:
    def __init__(self, team_name):
        self.data_path = f"{base_folder}/{team_name}"
        self.team_name = team_name
        self.validator = IDValidator(f"{self.data_path}/data")

    def validate(self):
        validation_status_output_file = f"{self.data_path}/data/validation_status.csv"

        if not os.path.exists(validation_status_output_file):
            validation_statuses = self.validator.validate()
            print(validation_statuses)

            with open(validation_status_output_file, 'w', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(['Base name', 'Headshot', 'Date of birth', 'Name', 'Valid'])
                for status in validation_statuses:
                    writer.writerow(
                        [status["base_name"], status["headshot"], status["dob"], status["name"], status["valid"]])
        else:
            with open(validation_status_output_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                validation_statuses = []
                for row in reader:
                    validation_statuses.append(
                        {"base_name": row[0], "headshot": row[1], "dob": row[2], "name": row[3], "valid": row[4]})
                print(validation_statuses)

        self.create_report(validation_statuses)

    def create_report(self, validation_statuses: dict):
        output_file = f"{self.data_path}/{self.team_name}-output.csv"
        emails = get_emails(output_file)
        print(emails)

        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        worksheet['A1'] = "Valid?"
        worksheet['B1'] = "Headshot valid?"
        worksheet['C1'] = "DOB valid?"
        worksheet['D1'] = "Name valid?"
        worksheet['E1'] = "Name"
        worksheet['F1'] = "DOB"
        worksheet['G1'] = "Email"
        worksheet['H1'] = "Headshot"
        worksheet['I1'] = "ID"
        worksheet.column_dimensions['A'].width = DEFAULT_COLUMN_WIDTH
        worksheet.column_dimensions['B'].width = DEFAULT_COLUMN_WIDTH
        worksheet.column_dimensions['C'].width = DEFAULT_COLUMN_WIDTH
        worksheet.column_dimensions['D'].width = DEFAULT_COLUMN_WIDTH
        worksheet.column_dimensions['E'].width = DEFAULT_COLUMN_WIDTH
        worksheet.column_dimensions['F'].width = DEFAULT_COLUMN_WIDTH
        worksheet.column_dimensions['G'].width = DEFAULT_COLUMN_WIDTH
        worksheet.row_dimensions[1].height = TITLE_ROW_HEIGHT

        for i, status in enumerate(validation_statuses):
            index = i + 2
            worksheet[f'A{index}'] = status["valid"]
            worksheet[f'B{index}'] = status["headshot"]
            worksheet[f'C{index}'] = status["dob"]
            worksheet[f'D{index}'] = status["name"]

            headshot_image = Image(f'{self.data_path}/data/{status["base_name"]}/headshot.jpg')
            headshot_image.width, headshot_image.height = IMAGE_DIMENSION, IMAGE_DIMENSION
            worksheet.add_image(headshot_image, f'H{index}')
            worksheet.column_dimensions['H'].width = headshot_image.width * 0.140625

            govt_id_image = Image(f'{self.data_path}/data/{status["base_name"]}/id.jpg')
            govt_id_image.width, govt_id_image.height = IMAGE_DIMENSION, IMAGE_DIMENSION
            worksheet.add_image(govt_id_image, f'I{index}')
            worksheet.column_dimensions['I'].width = govt_id_image.width * 0.140625

            worksheet.row_dimensions[index].height = max(headshot_image.height, govt_id_image.height) * 0.75

            base_name = status["base_name"]
            info_file = f"{self.data_path}/data/{base_name}/info.txt"
            worksheet[f'E{index}'], worksheet[f'F{index}'] = get_name_and_dob_for_player(info_file)

            worksheet[f'G{index}'] = emails[int(status["base_name"])]

        font = Font(size=FONT_SIZE)
        for row in workbook.active.iter_rows():
            for cell in row:
                cell.font = font

        workbook.save(f'{self.data_path}/{self.team_name}-report.xlsx')

if __name__ == '__main__':
    team_names = [
        "Free Agents-Girls 15-17",
    ]
    for team_name in team_names:
        team_validator = TeamValidator(team_name)
        team_validator.validate()