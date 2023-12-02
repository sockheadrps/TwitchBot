from PIL import Image
import os

def resize_images(input_folder, output_folder, target_size=(250, 700)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        print(filename)

        # Open the image
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize(target_size)

            # Save the resized image
            resized_img.save(output_path)

if __name__ == "__main__":
    input_folder = "./chars"
    output_folder = "./output"
    target_size = (230, 680)

    resize_images(input_folder, output_folder, target_size)
    print("Image resizing complete.")
