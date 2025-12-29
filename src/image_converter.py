from PIL import Image
import io
import os


class ImageConverter:
    def __init__(self, target_quality=75, target_width=1600):
        self.target_quality = target_quality
        self.target_width = target_width

    """
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
    """
    def compress_image(self, file):
        img = Image.open(file.file)
        size = self.calculate_new_size(img.size)
        
        if size is not None:
            img.thumbnail(size)
        
        output = io.BytesIO()
        img.save(output, "JPEG", optimize=True, quality=self.target_quality, exif=img.getexif())
        output.seek(0)

        return output
        
    def calculate_new_size(self, original_size):
        target_width = self.target_width
        width, height = original_size

        if width <= target_width:
            return None
        
        aspect_ratio = width / height
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

        return new_width, new_height
    """
    def get_folder_name(self, img):
        datetime_original = (img._getexif() or {}).get(36867)

        orig_split = datetime_original.split(' ')[0].split(':')

        return orig_split[0] + orig_split[1]
    """