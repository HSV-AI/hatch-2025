import PIL.Image as Image
from os import listdir, path
import os
from multiprocessing import Pool


def convert_file(input_file, output_file):
    # Open the TIFF image
    img = Image.open(input_file)
    # Save the image as a PNG file
    img.save(output_file, "PNG")
    # Close the image
    img.close()


def convert_tiff_to_png(input_folder, output_folder, limit=None):
    # Ensure the output folder exists
    if limit is None:
        limit = float('inf')

    if not path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of class dirs in the input folder
    class_dirs = [d for d in listdir(input_folder) if path.isdir(path.join(input_folder, d))]
    # Loop through each class dir
    # Get a list of all files in the input folder
    for class_dir in class_dirs:
        input_class_dir = path.join(input_folder, class_dir)
        output_class_dir = path.join(output_folder, class_dir)
        if not path.exists(output_class_dir):
            os.makedirs(output_class_dir)

        # Get a list of all files in the input folder
        files = listdir(input_class_dir)
        for i, file_name in enumerate(files):
            if i >= limit:
                break
            # Check if the file is a TIFF file
            if file_name.endswith(".tif") or file_name.endswith(".tiff"):
                # Open the TIFF image
                img = Image.open(path.join(input_class_dir, file_name))
                # Save the image as a PNG file
                img.save(path.join(output_class_dir, file_name.replace(".tif", ".png")), "PNG")
                print(f"Converted {file_name} to PNG")
                # Close the image
                img.close()
            else:
                print(f"Skipped {file_name} as it is not a TIFF file")
            

if __name__ == "__main__":
    input_folder = "data/DIBaS_Dataset/"
    output_folder = "data/DIBaS_Dataset_png/"
    convert_tiff_to_png(input_folder, output_folder, limit=3)