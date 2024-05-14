from PIL import Image
import os

class ImageCropper:

    def teste(self):
        images_to_crop_path = "../images_to_crop/images"
        images_list = os.listdir(images_to_crop_path)

        for image_name in images_list:
            image_path = "../images_to_crop/images/{}".format(image_name)
            image = Image.open(image_path)
            x = image.size[0]
            y = image.size[1]

            half_of_x = x / 2
            half_of_y = y / 2

            x_0 = 0
            y_0 = 0

            self.__create_crop_from_image(image, image_name, (x_0, y_0, half_of_x, half_of_y), "1")
            self.__create_crop_from_image(image, image_name, (x_0, half_of_y, half_of_x, y), "2")
            self.__create_crop_from_image(image, image_name, (half_of_x, y_0, x, half_of_y), "3")
            self.__create_crop_from_image(image, image_name, (half_of_x, half_of_y, x, y), "4")

    def __create_crop_from_image(self, image, image_name, tuple_to_crop, part):
        new_image = image.crop(tuple_to_crop)

        new_image_path = '../images_to_crop/images_cropped/{}-{}'.format(part, image_name)
        new_image.save(new_image_path)