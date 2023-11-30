"""
data_augmentation

This module performs data augmentation on images in the specified directory.
"""

import os
import random
from torchvision import transforms
from PIL import Image

# Đường dẫn đến thư mục chứa ảnh gốc
ORIGINAL_DUANON_PATH = r"C:\Users\ACER\Desktop\Coconut-Mature-Classification\dua non"

# Số lượng ảnh bạn muốn tạo
NUM_AUGMENTED_IMAGES = 600

# Biến đổi dữ liệu
DATA_AUGMENTATION = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.RandomPerspective(distortion_scale=0.2, p=0.5),
])

# Lấy số cuối cùng trong tên ảnh gốc
last_image_number = max(
    (int(file.split('.')[0]) for file in os.listdir(ORIGINAL_DUANON_PATH) if file.endswith('.jpg')),
    default=0
)
image_count = last_image_number + 1
original_images = [file for file in os.listdir(ORIGINAL_DUANON_PATH) if file.endswith('.jpg')]

# Lặp để tạo thêm ảnh mới
for i in range(NUM_AUGMENTED_IMAGES):
    original_image_path = os.path.join(ORIGINAL_DUANON_PATH, random.choice(original_images))
    new_image_name = f'{image_count}.jpg'
    new_image_path = os.path.join(ORIGINAL_DUANON_PATH, new_image_name)
    image = Image.open(original_image_path)
    augmented_image = DATA_AUGMENTATION(image)
    augmented_image = augmented_image.convert('RGB')
    augmented_image.save(new_image_path, 'JPEG')
    image_count += 1

print("Finished")