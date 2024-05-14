from PIL import Image
import os

class ImageCropper:

    def teste(self):
        images_to_crop_path = "../images_to_crop/images"
        images_list = os.listdir(images_to_crop_path)

        for image_name in images_list:
            # image_path = "../images_to_crop/images/{}".format(image_name)
            # original_image = Image.open(image_path)
            image_path = "../images_to_crop/images/{}".format(image_name)
            image = Image.open(image_path)
            print(image.size)
            x = image.size[0]
            y = image.size[1]

            half_of_x = x / 2
            half_of_y = y / 2

            x_0 = 0
            y_0 = 0


            self.__create_crop_from_image(image, image_name, (x_0, y_0, 2304, 1728), "1")
            self.__create_crop_from_image(image, image_name, (x_0, 1728, 2304, 3456), "2")
            self.__create_crop_from_image(image, image_name, (2304, y_0, 4608, 1728), "3")
            self.__create_crop_from_image(image, image_name, (2304, 1728, 4608, 3456), "4")

            # tuple_to_crop1 = (0, 0, 2304, 1728)
            # new_image1 = original_image.crop(tuple_to_crop1)
            #
            # new_image1_path = '../images_to_crop/images_cropped/1-{}'.format(image_name)
            # new_image1.save(new_image1_path)
            #
            # tuple_to_crop2 = (0, 1728, 2304, 3456)
            # new_image2 = original_image.crop(tuple_to_crop2)
            #
            # new_image2_path = '../images_to_crop/images_cropped/2-{}'.format(image_name)
            # new_image2.save(new_image2_path)
            #
            # tuple_to_crop3 = (2304, 0, 4608, 1728)
            # new_image3 = original_image.crop(tuple_to_crop3)
            #
            # new_image3_path = '../images_to_crop/images_cropped/3-{}'.format(image_name)
            # new_image3.save(new_image3_path)
            #
            # tuple_to_crop4 = (2304, 1728, 4608, 3456)
            # new_image4 = original_image.crop(tuple_to_crop4)
            #
            # new_image4_path = '../images_to_crop/images_cropped/4-{}'.format(image_name)
            # new_image4.save(new_image4_path)

    def __create_crop_from_image(self, image, image_name, tuple_to_crop, part):
        new_image = image.crop(tuple_to_crop)

        new_image_path = '../images_to_crop/images_cropped/{}-{}'.format(part, image_name)
        new_image.save(new_image_path)