
from src.cropper.ClassificationLabelCropper import ClassificationLabelCropper
from src.organize_images.OrganizeImagesToYolo import OrganizeImagesToYolo

if __name__ == '__main__':
    # ClassificationLabelCropper().create_crops_from_all_images()
    # ClassificationLabelCropper().copy_images_cropped_to_folder_all_images()

    # ClassificationLabelCropper().copy_images_cropped_to_folder_all_images_by_type()

    # ClassificationLabelCropper().get_images_sizes()
    OrganizeImagesToYolo().remove_images_of_val_in_folder_train()