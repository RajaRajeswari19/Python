import pandas as pd
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Read the data from a CSV file into a pandas DataFrame
df = pd.read_csv("c:\\users\Windows\Documents\Python\inputFile.csv")
# print(df)

# Report 1 Summary
# Group the data by location and property type
grouped = df.groupby(['location', 'property_type'])

# To find the grouped location and then the average price and sqft.
grouped_location = df.groupby(['location'])
average_price = grouped_location['price'].mean()
average_sqft = grouped_location['square_footage'].mean()
averages_loc = grouped.agg({'price': 'mean', 'square_footage': 'mean'})

# To find the grouped propertytype and then average no of bedrooms and bathrooms
grouped_prop = df.groupby(['property_type'])
average_bedroom = grouped_prop['num_bedrooms'].mean()
average_bathroom = grouped_prop['num_bathrooms'].mean()
averages_prop = grouped_prop.agg({'num_bedrooms': 'mean', 'num_bathrooms': 'mean'})

# Merge the two sets of averages into one DataFrame
report = pd.merge(averages_loc, averages_prop, left_on='property_type', right_index=True)

# Sort the report by location and property type
report = report.sort_values(by=['location', 'property_type'])

# Convert the report DataFrame to a list of lists
data = [list(row) for row in report.to_records(index=True)]

# Add headers to the data
headers = ['Location', 'Property Type', 'Avg Price', 'Avg SqFt.', 'Avg No of Bedrooms', 'Avg No of Bathrooms']
data.insert(0, headers)

# Define the style for the table
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
])

# Create the table and add the style
table = Table(data)
table.setStyle(style)

# Create a PDF report with the table
pdf = SimpleDocTemplate("c:\\users\Windows\Documents\Python\summary.pdf", pagesize=letter)

pdf.build([table])

# Report2

# PDF Report Generation
documentTitle = "Real Estate Report Generation"

pdf = canvas.Canvas("c:\\users\Windows\Documents\Python\output.pdf", pagesize=letter)
width, height = letter
pdf.setFont("Helvetica-Bold", 14)
pdf.drawCentredString(300, 770, documentTitle)

pdf.setFont("Helvetica", 12)
pdf.drawString(50, 700, "The Average Price and Square Footage of properties by Location")
pdf.setFont("Helvetica", 10)

y = 670
for location in average_price.index:
    pdf.drawString(70, y, f"Location: {location}")
    pdf.drawString(70, y - 20, f"Average Price: {average_price[location]:,.2f}")
    pdf.drawString(70, y - 40, f"Average SqFt: {average_sqft[location]:,.2f} sqft")
    y -= 80

pdf.setFont("Helvetica", 12)
pdf.drawString(50, y, "The Average Number of Bedrooms and Bathrooms for each property type")
pdf.setFont("Helvetica", 10)
y -= 30
for property_type in average_bedroom.index:
    pdf.drawString(70, y, f"Property Type: {property_type}")
    pdf.drawString(70, y - 20, f"Average Bedroom: {average_bedroom[property_type]:,.2f}")
    pdf.drawString(70, y - 40, f"Average Bathroom: {average_bathroom[property_type]:,.2f}")
    y -= 80

# For saving the pdf
pdf.save()


