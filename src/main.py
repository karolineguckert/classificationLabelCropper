from PIL import Image
from pybboxes import BoundingBox


def teste():
    img = Image.open('src/images/0b982611-P0170017.jpg')
    labelContent = __get_label_lines('src/images/0b982611-P0170017.txt')

    firstContentDivided = labelContent[0].split(" ")
    type = firstContentDivided[0]


    width = 4608
    height = 3456
    image_size = (width, height)

    yolo_bbox = BoundingBox.from_yolo(*__create_yolo_bounding_box(firstContentDivided), image_size)
    teste2 = yolo_bbox.to_voc()

    print(yolo_bbox)  # x top left

    box = (teste2.x_tl - 30, teste2.y_tl - 30, teste2.x_br + 30, teste2.y_br + 30)
    img2 = img.crop(box)
    print(box)
    # img2.save('myimage_cropped.jpg')

    print(img2.size)


    # valor de base 30 30
    # valor de x = 395 - 60
    # valor de y = 484 - 60
    my_coco_box = [30, 30, 335, 424]
    coco_bbox = BoundingBox.from_coco(*my_coco_box, img2.size)
    print(coco_bbox.to_yolo())

    # img2.show()




def __create_yolo_bounding_box(content):
    x = float(content[1])  # corresponds to the first value of the definition of the yolo
    x_c = float(content[2])  # corresponds to the second value of the definition of the yolo
    y_c = float(content[3])  # corresponds to the third value of the definition of the yolo
    y = float(content[4])  # corresponds to the fourth value of the definition of the yolo

    return [x, x_c, y_c, y]


# Assistant method to get all lines from file with classifications
#
# label_path is the path of the label
def __get_label_lines(label_path):
    file = open(label_path, "r")
    content = file.readlines()

    file.close()

    return content


if __name__ == '__main__':
    teste()

