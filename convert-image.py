from PIL import Image
from PIL.ExifTags import TAGS
import os

class ImageConverter:        
    def compress_image_and_preserve_date(self, input_path, output_path):
        img = Image.open(input_path)
        #old_exif = img.getexif()
        #new_exif = self.truncate_exif(old_exif)
        #new_exif = self.encode_exif(new_exif)

        
        """
        original_size = image.size
        aspect_ratio = original_size[0] / original_size[1]
        new_width = 800
        new_height = int(new_width / aspect_ratio)
        """
        
        size = (img.size[0]/3,  img.size[1]/3)
        img.thumbnail(size)
        
        img.save(output_path, "JPEG", optimize=True, quality=75, exif=img.getexif())
        
    def truncate_exif(self, exif_data):
        new_exif = {}
        
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    new_exif[306] = value
                    break
        
        return new_exif
        
    def encode_exif(self, exif):
        exif_bytes = b''

        for k, v in exif.items():
           try:
               if isinstance(v, str):
                   v_bytes = v.encode('utf-8')
               else:
                   v_bytes = str(v).encode('utf-8')
               exif_bytes += get_marker(k) + v_bytes
           except Exception as e:
               print(f"Warning: Could not encode EXIF tag {k}: {e}")
        
        return exif_bytes

input_image_path = 'picture1.jpg'
output_image_path = 'picture1-out.jpg'

image_converter = ImageConverter()
image_converter.compress_image_and_preserve_date(input_image_path, output_image_path)