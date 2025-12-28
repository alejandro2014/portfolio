from PIL import Image
import os
import sys

class ImageConverter:
    def __init__(self):
        self.target_quality = 75
        self.target_width = 1600

    def compress_image_and_preserve_date(self, input_path, output_path):
        img = Image.open(input_path)
        
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

input_image_path = sys.argv[1]
output_image_path = sys.argv[2]

image_converter = ImageConverter()
image_converter.compress_image_and_preserve_date(input_image_path, output_image_path)