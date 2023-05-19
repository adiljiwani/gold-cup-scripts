from id_validator.main import IDValidator
import openpyxl
from openpyxl.drawing.image import Image
import csv
import os


class TeamValidator:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validator = IDValidator(data_path)

    def validate(self):
        validation_status_output_file = f"{self.data_path}/validation_status.csv"

        if not os.path.exists(validation_status_output_file):
            validation_statuses = self.validator.validate()
            print(validation_statuses)

            with open(validation_status_output_file, 'w', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(['Base name', 'Headshot', 'Date of birth', 'Name', 'Valid'])
                for status in validation_statuses:
                    writer.writerow([status["base_name"], status["headshot"], status["dob"], status["name"], status["valid"]])
        else:
            with open(validation_status_output_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                validation_statuses = []
                for row in reader:
                    validation_statuses.append({"base_name": row[0], "headshot": row[1], "dob": row[2], "name": row[3], "valid": row[4]})
                print(validation_statuses)

        self.create_report(validation_statuses)

    def create_report(self, validation_statuses: dict):
        # create a new workbook
        workbook = openpyxl.Workbook()
        # create a new worksheet
        worksheet = workbook.active

        worksheet['A1'] = "Valid?"
        worksheet['B1'] = "Headshot valid?"
        worksheet['C1'] = "Date of birth"
        worksheet['D1'] = "Name"
        worksheet['E1'] = "Headshot"
        worksheet['F1'] = "ID"

        for i, status in enumerate(validation_statuses):
            index = i + 2
            worksheet[f'A{index}'] = status["valid"]
            worksheet[f'B{index}'] = status["headshot"]
            worksheet[f'C{index}'] = status["dob"]
            worksheet[f'D{index}'] = status["name"]

            headshot_image = Image(f'{self.data_path}/{status["base_name"]}/headshot.jpg')
            worksheet.add_image(headshot_image, f'E{index}')
            worksheet.column_dimensions['E'].width = headshot_image.width * 0.140625

            govt_id_image = Image(f'{self.data_path}/{status["base_name"]}/id.jpg')
            worksheet.add_image(govt_id_image, f'F{index}')
            worksheet.column_dimensions['F'].width = govt_id_image.width * 0.140625

            worksheet.row_dimensions[index].height = max(headshot_image.height, govt_id_image.height) * 0.75

            # save the workbook
            workbook.save(f'{self.data_path}.xlsx')


if __name__ == '__main__':
    team_validator = TeamValidator("AK United- B-09: Boys 12-14 test/data")
    team_validator.validate()
