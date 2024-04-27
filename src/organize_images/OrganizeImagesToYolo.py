from PIL import Image
from pybboxes import BoundingBox
import os
import shutil

class OrganizeImagesToYolo:
    def __init__(self):
        self.PATH_TRAIN = '../src/images_to_yolo/train'
        self.PATH_VAL = '../src/images_to_yolo/val'

    def move_labels_of_train_to_val(self):
        file_list = os.listdir('{}/{}'.format(self.PATH_VAL, 'images'))

        for file in file_list:

            label_name = file.replace(".jpg", ".txt")
            label_path = '{}/labels/{}'.format(self.PATH_TRAIN, label_name)

            new_path_of_label = '{}/labels/{}'.format(self.PATH_VAL, label_name)
            shutil.move(label_path, new_path_of_label)

    def remove_images_of_val_in_folder_train(self):
        file_list = os.listdir('{}/{}'.format(self.PATH_VAL, 'images'))

        for file in file_list:
            label_path = '{}/images/{}'.format(self.PATH_TRAIN, file)
            os.remove(label_path)