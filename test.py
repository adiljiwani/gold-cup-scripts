import openpyxl
from openpyxl.drawing.image import Image

# create a new workbook
workbook = openpyxl.Workbook()

# create a new worksheet
worksheet = workbook.active

# add an image to the worksheet
img = Image('KFC/data/0/headshot.jpg')
# img.height = 300
worksheet['A1'] = 'Hello'
worksheet.add_image(img, 'B1')
worksheet.row_dimensions[1].height = img.height
worksheet.column_dimensions['B'].width = img.width

# save the workbook
workbook.save('test.xlsx')