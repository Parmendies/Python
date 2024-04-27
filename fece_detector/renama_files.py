import os
import cv2


def rename_images(folder_path):
    # Get all file names in the folder
    filenames = [f for f in os.listdir(
        folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Sort filenames alphabetically
    filenames.sort()

    # Rename images with sequential numbers
    counter = 1
    for filename in filenames:
        # Check if the file is an image
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            # Generate new filename with sequential number
            new_filename = f"{counter}.{filename.split('.')[-1]}"

            # Rename the file
            old_filepath = os.path.join(folder_path, filename)
            new_filepath = os.path.join(folder_path, new_filename)
            os.rename(old_filepath, new_filepath)

            # Increment counter
            counter += 1


if __name__ == "__main__":
    # Enter the target folder path
    # Replace with the actual folder path
    folder_path = "/home/bimo/Python/fece_detector/face_db/omer"

    # Call the rename_images function
    rename_images(folder_path)
