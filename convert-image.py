from PIL import Image
import os
import sys


class ImageConverter:
    def __init__(self):
        self.target_quality = 75
        self.target_width = 1600

    def compress_images(self, input_path):
        images = os.listdir(input_path)
        images = [ i for i in images if i.endswith('.jpg') or i.endswith('.jpeg') ]

        for image in images:
            image_path = f"{input_path}/{image}"
            img = Image.open(image_path)

            output_directory = self.get_folder_name(img)

            if not os.path.exists(output_directory):
                os.mkdir(output_directory)

            output_path = f"{output_directory}/{image}"
            
            self.compress_image(img, output_path)

    def compress_image(self, img, output_path):
        size = self.calculate_new_size(img.size)
        
        if size is not None:
            img.thumbnail(size)
        
        img.save(output_path, "JPEG", optimize=True, quality=self.target_quality, exif=img.getexif())
        
    def calculate_new_size(self, original_size):
        target_width = self.target_width
        width, height = original_size

        if width <= target_width:
            return None
        
        aspect_ratio = width / height
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

        return new_width, new_height
    
    def get_folder_name(self, img):
        datetime_original = (img._getexif() or {}).get(36867)

        orig_split = datetime_original.split(' ')[0].split(':')

        return orig_split[0] + orig_split[1]

input_path = sys.argv[1]
image_converter = ImageConverter()
image_converter.compress_images(sys.argv[1])