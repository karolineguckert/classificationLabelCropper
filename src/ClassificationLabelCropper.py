from PIL import Image
from pybboxes import BoundingBox


class ClassificationLabelCropper:

    def __init__(self):
        self.BORDER_DEFAULT = 30
        self.WIDTH = 4608
        self.HEIGHT = 3456

    # TODO incluir uma validação de fim de imagem para redyzir o tamanho de corte
    def create_crops_from_image(self, file_name):
        original_image = Image.open('images/originalImageToCrop/{}.jpg'.format(file_name))
        label_content = self.__get_label_lines('images/originalImageToCrop/{}.txt'.format(file_name))

        for i in range(len(label_content)):
            content = label_content[i].split(" ")
            class_type = content[0]

            new_image = self.__get_new_image_cropped(content, original_image)
            # new_image.save('./images/cropped/images/{}-{}.jpg'.format(file_name, i))

            # new_voc_bounding_box = BoundingBox.from_voc(*self.__get_new_image_bounding_box(new_image), new_image.size)
            # self.__create_label_file(new_voc_bounding_box, class_type, '{}-{}'.format(file_name, i))

    # Assistant method to create the bounding box in a txt file
    #
    # new_voc_bounding_box is the voc bounding box of the cropped image
    # class_type is the type of the object that is in the image
    # file_name is the name of the file
    def __create_label_file(self, new_voc_bounding_box, class_type, file_name):
        file = open('./images/cropped/labels/{}.txt'.format(file_name), 'a')
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
        return [
            self.BORDER_DEFAULT,
            self.BORDER_DEFAULT,
            new_image_width - self.BORDER_DEFAULT,
            new_image_height - self.BORDER_DEFAULT
        ]

    # Assistant method to create a new bounding box from the image cropped
    #
    # bounding_boxes is the bounding box from the image cropped
    def __get_new_voc_bounding_box(self, bounding_boxes):
        new_value_x_tl = self.__get_value_x_tl(bounding_boxes.x_tl)
        new_value_y_tl = bounding_boxes.y_tl
        new_value_x_br = bounding_boxes.x_br
        new_value_y_br = bounding_boxes.y_br

        # if(new_value_x_tl - 30) < 0:
        #     aux_x_tl = self.WIDTH - new_value_x_tl
        #
        #     if aux_x_tl == self.WIDTH:
        #         new_value_x_tl = 0
        #     else:
        #         new_value_x_tl = aux_x_tl + new_value_x_tl
        # else:
        #     new_value_x_tl = new_value_x_tl - self.BORDER_DEFAULT

        if(new_value_y_tl - 30) < 0:
            aux_y_tl = self.WIDTH - new_value_y_tl

            if aux_y_tl == self.WIDTH:
                new_value_y_tl = 0
            else:
                new_value_y_tl = aux_y_tl + new_value_y_tl
        else:
            new_value_y_tl = new_value_y_tl - self.BORDER_DEFAULT

        if (new_value_x_br + 30) > self.WIDTH:
            aux_x_br = self.WIDTH - new_value_x_br

            if aux_x_br == 0:
                new_value_x_br = 0
            else:
                new_value_x_br = aux_x_br + new_value_x_br
        else:
            new_value_x_br = new_value_x_br + self.BORDER_DEFAULT

        if (new_value_y_br + 30) > self.WIDTH:
            aux_y_br = self.WIDTH - new_value_y_br

            if aux_y_br == 0:
                new_value_y_br = 0
            else:
                new_value_y_br = aux_y_br + new_value_y_br
        else:
            new_value_y_br = new_value_y_br + self.BORDER_DEFAULT

        return (
            new_value_x_tl,
            new_value_y_tl,
            new_value_x_br,
            new_value_y_br
        )

    def __get_value_x_tl(self, x_tl):
        if(x_tl - self.BORDER_DEFAULT) < 0:
            aux_x_tl = self.WIDTH - x_tl

            if aux_x_tl == self.WIDTH:
                new_value_x_tl = 0
            else:
                new_value_x_tl = aux_x_tl + x_tl
        else:
            new_value_x_tl = x_tl - self.BORDER_DEFAULT

        return new_value_x_tl

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
