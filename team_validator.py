from id_validator.main import IDValidator
import openpyxl
from openpyxl.drawing.image import Image


class TeamValidator:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validator = IDValidator(data_path)

    def validate(self):
        validation_statuses = self.validator.validate()
        print(validation_statuses)

        self.create_report(validation_statuses)

    def create_report(self, validation_statuses: dict):
        # create a new workbook
        workbook = openpyxl.Workbook()
        # create a new worksheet
        worksheet = workbook.active

        worksheet['A1'] = "Headshot valid?"
        worksheet['B1'] = "Date of birth"
        worksheet['C1'] = "Name"
        worksheet['D1'] = "Headshot"
        worksheet['E1'] = "ID"

        invalid_statuses = validation_statuses.get(False, [])
        for i, invalid in enumerate(invalid_statuses):
            index = i + 2
            worksheet[f'A{index}'] = invalid["headshot"]
            worksheet[f'B{index}'] = invalid["dob"]
            worksheet[f'C{index}'] = invalid["name"]

            headshot_image = Image(f'{self.data_path}/{invalid["base_name"]}/headshot.jpg')
            worksheet.add_image(headshot_image, f'D{index}')
            worksheet.column_dimensions['D'].width = headshot_image.width

            govt_id_image = Image(f'{self.data_path}/{invalid["base_name"]}/id.jpg')
            worksheet.add_image(govt_id_image, f'E{index}')
            worksheet.column_dimensions['E'].width = govt_id_image.width

            worksheet.row_dimensions[index].height = max(headshot_image.height, govt_id_image.height)

            # save the workbook
            workbook.save(f'{self.data_path}.xlsx')


if __name__ == '__main__':
    team_validator = TeamValidator("Young Boys-M-01: Mens 21+/data")
    team_validator.validate()
