from pdf2image import convert_from_path
import os

# Define the directory containing the PDF files and the output directory
pdf_directory = '/home/plewis/towerslope/tower_Rhich_Trials'
output_directory = '/home/plewis/towerslope/tower_Rhich_Trials'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through all files in the PDF directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        # Convert the PDF to a list of images
        images = convert_from_path(pdf_path)
        
        # Save each image as a PNG file
        for i, image in enumerate(images):
            output_path = os.path.join(output_directory, f'{os.path.splitext(filename)[0]}_page_{i + 1}.png')
            image.save(output_path, 'PNG')

        print(f"{filename} has been converted to PNG and saved in {output_directory}")









