from PIL import Image
from pybboxes import BoundingBox
import os
import shutil


class ClassificationLabelCropper:

    def __init__(self):
        self.TYPE_QUANTITY = 6
        self.BORDER_DEFAULT = 30
        self.WIDTH = 4608
        self.HEIGHT = 3456
        self.list_of_borders = []
        self.PATH_TO_CROP = 'images/originalImageToCrop'
        self.PATH_FINALLY = './images/originalImageFinallyCropped'
        self.PATH_CROPPED = './images/cropped'
        self.PATH_ALL_IMAGES = './images/allImageCropped'
        self.PATH_ALL_IMAGES_BY_TYPE = './images/allImagesCroppedByType'

    def copy_images_cropped_to_folder_all_images_by_type(self):
        file_list = os.listdir('{}/'.format(self.PATH_CROPPED))
        self.__create_all_folders_for_all_images_by_type()

        for file in file_list:
            label_file_list = os.listdir('{}/{}/labels'.format(self.PATH_CROPPED, file))

            for label_file in label_file_list:
                image_file = label_file.replace(".txt", ".jpg")

                original_label_path = '{}/{}/labels/{}'.format(self.PATH_CROPPED, file, label_file)
                original_image_path = '{}/{}/images/{}'.format(self.PATH_CROPPED, file, image_file)

                content = self.__get_label_lines(original_label_path)
                content_splitted = content[0].split(' ')
                class_type = content_splitted[0]

                copy_label_path = '{}/{}/labels/{}'.format(self.PATH_ALL_IMAGES_BY_TYPE, class_type, label_file)
                copy_image_path = '{}/{}/images/{}'.format(self.PATH_ALL_IMAGES_BY_TYPE, class_type, image_file)

                shutil.copy(original_label_path, copy_label_path)
                shutil.copy(original_image_path, copy_image_path)

    # Assistant method to create copies of labels and images to folder all images cropped
    #
    def copy_images_cropped_to_folder_all_images(self):
        file_list = os.listdir('{}/'.format(self.PATH_CROPPED))

        self.__create_folder_for_all_images("images")
        self.__create_folder_for_all_images("labels")

        for file in file_list:
            sub_file_list = os.listdir('{}/{}'.format(self.PATH_CROPPED, file))

            for sub_file in sub_file_list:
                if sub_file == 'images':
                    images_list = os.listdir('{}/{}/images/'.format(self.PATH_CROPPED, file))
                    self.__create_copies_from_images_cropped(images_list, file, "images")
                else:
                    labels_list = os.listdir('{}/{}/labels/'.format(self.PATH_CROPPED, file))
                    self.__create_copies_from_images_cropped(labels_list, file, "labels")

    # Assistant method to create all images cropped
    #
    def create_crops_from_all_images(self):
        file_list = os.listdir('{}/images'.format(self.PATH_TO_CROP))
        for file in file_list:
            file_name = file.replace(".jpg", "")
            self.__create_crops_from_image(file_name)


    def get_images_sizes(self):
        file_list = os.listdir('{}/images'.format(self.PATH_ALL_IMAGES))
        print(file_list)



    # Assistant method to create copies to folder all images cropped
    #
    def __create_copies_from_images_cropped(self, list_of_elements, file, folder_name):
        for i in range(len(list_of_elements)):
            element = list_of_elements[i]
            original_element_path = '{}/{}/{}/{}'.format(self.PATH_CROPPED, file, folder_name, element)
            copy_element_path = '{}/{}/{}'.format(self.PATH_ALL_IMAGES, folder_name, element)
            shutil.copy(original_element_path, copy_element_path)

    # Assistant method to create cropped images from the original image
    #
    # file_name is the name of the file
    def __create_crops_from_image(self, file_name):
        image_path = '{}/images/{}.jpg'.format(self.PATH_TO_CROP, file_name)
        label_path = '{}/labels/{}.txt'.format(self.PATH_TO_CROP, file_name)
        self.__create_folders(file_name)

        original_image = Image.open(image_path)
        label_content = self.__get_label_lines(label_path)

        for i in range(len(label_content)):
            self.list_of_borders.clear()
            content = label_content[i].split(" ")
            class_type = content[0]

            new_image = self.__get_new_image_cropped(content, original_image)
            new_image_path = '{}/{}/images/{}-{}.jpg'.format(self.PATH_CROPPED, file_name, file_name, i)
            new_image.save(new_image_path)

            new_voc_bounding_box = BoundingBox.from_voc(*self.__get_new_image_bounding_box(new_image), new_image.size)
            self.__create_label_file(new_voc_bounding_box, class_type, '{}-{}'.format(file_name, i), file_name)

        shutil.move(image_path, '{}/{}.jpg'.format(self.PATH_FINALLY, file_name))
        shutil.move(label_path, '{}/{}.txt'.format(self.PATH_FINALLY, file_name))

    # Assistant method to create folder type to path all images by type
    #
    def __create_folder_to_a_type(self, folder_name):
        try:
            os.mkdir('{}/{}'.format(self.PATH_ALL_IMAGES_BY_TYPE, folder_name))
        except OSError as error:
            print(error)

        try:
            os.mkdir('{}/{}/images'.format(self.PATH_ALL_IMAGES_BY_TYPE, folder_name))
        except OSError as error:
            print(error)

        try:
            os.mkdir('{}/{}/labels'.format(self.PATH_ALL_IMAGES_BY_TYPE, folder_name))
        except OSError as error:
            print(error)

    # Assistant method to create all folders of type to path all images by type
    #
    def __create_all_folders_for_all_images_by_type(self):
        for i in range(self.TYPE_QUANTITY):
            self.__create_folder_to_a_type(i)

    # Assistant method to create folder to path all images
    #
    def __create_folder_for_all_images(self, folder_name):
        try:
            os.mkdir('{}/{}'.format(self.PATH_ALL_IMAGES, folder_name))
        except OSError as error:
            print(error)

    # Assistant method to create folders to path cropped
    #
    # file_name is the name of the file
    def __create_folders(self, file_name):
        os.mkdir('{}/{}'.format(self.PATH_CROPPED, file_name))
        os.mkdir('{}/{}/images'.format(self.PATH_CROPPED, file_name))
        os.mkdir('{}/{}/labels'.format(self.PATH_CROPPED, file_name))

    # Assistant method to create the bounding box in a txt file
    #
    # new_voc_bounding_box is the voc bounding box of the cropped image
    # class_type is the type of the object that is in the image
    # file_name is the name of the file
    def __create_label_file(self, new_voc_bounding_box, class_type, file_name_formatted, file_name):
        new_file_path = '{}/{}/labels/{}.txt'.format(self.PATH_CROPPED, file_name, file_name_formatted)

        file = open(new_file_path, 'a')
        file.write(self.__format_bounding_box(new_voc_bounding_box.to_yolo().values, class_type))

        file.close()

    # Assistant method to create yolo bounding box from text file
    #
    # content is the line text from file
    def __create_yolo_bounding_box(self, content):
        x = float(content[1])  # corresponds to the first value of the definition of the yolo
        x_c = float(content[2])  # corresponds to the second value of the definition of the yolo
        y_c = float(content[3])  # corresponds to the third value of the definition of the yolo
        y = float(content[4])  # corresponds to the fourth value of the definition of the yolo

        return [x, x_c, y_c, y]

    # Assistant method to format the bounding box to save in a txt file
    #
    # bounding_box is the tuple resultant for the cropped image
    # class_type is the type of the object that is in the image
    def __format_bounding_box(self, bounding_box, class_type):
        x = bounding_box[0]  # corresponds to the first value of the definition of the yolo
        x_c = bounding_box[1]  # corresponds to the second value of the definition of the yolo
        y_c = bounding_box[2]  # corresponds to the third value of the definition of the yolo
        y = bounding_box[3]  # corresponds to the fourth value of the definition of the yolo
        return "{} {} {} {} {}".format(class_type, x, x_c, y_c, y)

    # Assistant method to get a new image cropped from the original
    #
    # content is the line text from file
    # original_image the original image without cropping
    def __get_new_image_cropped(self, content, original_image):
        original_yolo_bounding_box = self.__get_original_yolo_bounding_box(content)
        original_voc_bounding_box = original_yolo_bounding_box.to_voc()

        new_voc_bounding_box = self.__get_new_voc_bounding_box(original_voc_bounding_box)

        return original_image.crop(new_voc_bounding_box)

    # Assistant method to get the new bounding box from the image cropped
    #
    # new_image is the original image cropped
    def __get_new_image_bounding_box(self, new_image):
        new_image_width = new_image.size[0]
        new_image_height = new_image.size[1]

        border_of_x_br = new_image_width - self.list_of_borders[2]
        border_of_y_br = new_image_height - self.list_of_borders[3]

        new_value_x_tl = self.list_of_borders[0]
        new_value_y_tl = self.list_of_borders[1]

        if new_image_width < (new_value_x_tl + self.list_of_borders[2]):
            new_value_x_br = new_image_width
        else:
            new_value_x_br = border_of_x_br

        if new_image_height < (new_value_y_tl + self.list_of_borders[3]):
            new_value_y_br = new_image_height
        else:
            new_value_y_br = border_of_y_br

        return [
            new_value_x_tl,
            new_value_y_tl,
            new_value_x_br,
            new_value_y_br
        ]

    # Assistant method to create a new bounding box from the image cropped
    #
    # bounding_boxes is the bounding box from the image cropped
    def __get_new_voc_bounding_box(self, bounding_boxes):
        new_value_x_tl = self.__get_value_x_tl(bounding_boxes.x_tl)
        new_value_y_tl = self.__get_value_y_tl(bounding_boxes.y_tl)
        new_value_x_br = self.__get_value_x_br(bounding_boxes.x_br)
        new_value_y_br = self.__get_value_y_br(bounding_boxes.y_br)

        return (
            new_value_x_tl,
            new_value_y_tl,
            new_value_x_br,
            new_value_y_br
        )

    # Assistant method to get the transformed value with border of the original image
    #
    # x_tl is the value from x of the top left
    def __get_value_x_tl(self, x_tl):
        if (x_tl - self.BORDER_DEFAULT) < 0:
            aux_x_tl = self.BORDER_DEFAULT - x_tl

            if self.BORDER_DEFAULT == aux_x_tl or x_tl == 0:
                new_value_x_tl = 0
                self.list_of_borders.append(0)
            else:
                new_value_x_tl = aux_x_tl + x_tl
                self.list_of_borders.append(aux_x_tl)
        else:
            new_value_x_tl = x_tl - self.BORDER_DEFAULT
            self.list_of_borders.append(self.BORDER_DEFAULT)

        return new_value_x_tl

    # Assistant method to get the transformed value with border of the original image
    #
    # y_tl is the value from y of the top left
    def __get_value_y_tl(self, y_tl):
        if (y_tl - self.BORDER_DEFAULT) < 0:
            aux_y_tl = self.BORDER_DEFAULT - y_tl

            if self.BORDER_DEFAULT == aux_y_tl or y_tl == 0:
                new_value_y_tl = 0
                self.list_of_borders.append(0)
            else:
                new_value_y_tl = aux_y_tl + y_tl
                self.list_of_borders.append(aux_y_tl)
        else:
            new_value_y_tl = y_tl - self.BORDER_DEFAULT
            self.list_of_borders.append(self.BORDER_DEFAULT)

        return new_value_y_tl

    # Assistant method to get the transformed value with border of the original image
    #
    # x_br is the value from x of the bottom right
    def __get_value_x_br(self, x_br):
        if (x_br + self.BORDER_DEFAULT) > self.WIDTH:
            aux_x_br = self.WIDTH - x_br
            if x_br != self.WIDTH:
                if aux_x_br == 0:
                    new_value_x_br = 0
                    self.list_of_borders.append(0)
                else:
                    new_value_x_br = aux_x_br + x_br
                    self.list_of_borders.append(aux_x_br)
            else:
                new_value_x_br = x_br
                self.list_of_borders.append(0)
        else:
            new_value_x_br = x_br + self.BORDER_DEFAULT
            self.list_of_borders.append(self.BORDER_DEFAULT)

        return new_value_x_br

    # Assistant method to get the transformed value with border of the original image
    #
    # y_br is the value from y of the bottom right
    def __get_value_y_br(self, y_br):
        if (y_br + self.BORDER_DEFAULT) > self.HEIGHT:
            aux_y_br = self.HEIGHT - y_br

            if y_br != self.HEIGHT:
                if aux_y_br == 0:
                    new_value_y_br = 0
                    self.list_of_borders.append(0)
                else:
                    new_value_y_br = aux_y_br + y_br
                    self.list_of_borders.append(aux_y_br)
            else:
                new_value_y_br = y_br
                self.list_of_borders.append(0)
        else:
            new_value_y_br = y_br + self.BORDER_DEFAULT
            self.list_of_borders.append(self.BORDER_DEFAULT)

        return new_value_y_br

    # Assistant method to get the original bounding box from the image
    #
    # content is the line text from file
    def __get_original_yolo_bounding_box(self, content):
        return BoundingBox.from_yolo(*self.__create_yolo_bounding_box(content), self.__get_image_size())

    # Assistant method to get the original size from the image
    #
    def __get_image_size(self):
        return self.WIDTH, self.HEIGHT

    # Assistant method to get all lines from file with classifications
    #
    # label_path is the path of the label
    def __get_label_lines(self, label_path):
        file = open(label_path, "r")
        content = file.readlines()

        file.close()

        return content
