"""
Train_Model

This module trains a model using MobileNetV2 architecture for coconut classification.
"""

import torch
import torchvision
from torchvision import transforms, models
from torch.utils.data import DataLoader
from torch import nn
from sklearn.metrics import f1_score
from tqdm import tqdm
from lion_pytorch import Lion
# Set up transforms and datasets
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

train_data = torchvision.datasets.ImageFolder(
    root=r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\train', transform=train_transforms)
val_data = torchvision.datasets.ImageFolder(
    root=r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\val', transform=val_transforms)

# Set up MobileNetV2 model
model = models.mobilenet_v2(pretrained=True)
NUM_CLASSES = 3
model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)

for param in model.features.parameters():
    param.requires_grad = False

# Print model parameters
print("# Parameters", sum(p.numel() for p in model.parameters()))

# Set up device and other training parameters
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EPOCHS = 30
BATCH_SIZE = 64

# Create data loaders
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)

# Move model to device
model.to(DEVICE)

# Set up loss, optimizer, and filename for saving the model
criterion = nn.CrossEntropyLoss()
optimizer = Lion(model.parameters(), lr=1e-4, weight_decay=1e-2)
MODEL_SAVE_PATH = 'MobileNetV2(test).pt'

# Set up early stopping parameters
PATIENCE = 5
BEST_VALIDATION_LOSS = float('inf')
NO_IMPROVEMENT_COUNT = 0

# Lists to store training and testing metrics
LOSS_TRAIN = []
LOSS_TEST = []
F1_TRAIN = []
F1_TEST = []

# Training loop
for EPOCH in range(EPOCHS):
    model.train()
    RUNNING_LOSS = 0.0
    PREDICTIONS_TRAIN = []
    TRUE_LABELS_TRAIN = []

    for I, DATA in tqdm(enumerate(train_loader), desc='train'):
        INPUTS, LABELS = DATA
        INPUTS = INPUTS.to(DEVICE)
        LABELS = LABELS.to(DEVICE)
        optimizer.zero_grad()
        OUTPUTS = model(INPUTS)
        LOSS = criterion(OUTPUTS, LABELS)
        LOSS.backward()
        optimizer.step()
        RUNNING_LOSS += LOSS.item()
        _, PREDICTED = torch.max(OUTPUTS.data, 1)
        PREDICTIONS_TRAIN.extend(PREDICTED.tolist())
        TRUE_LABELS_TRAIN.extend(LABELS.tolist())

    TRAIN_LOSS = RUNNING_LOSS / len(train_loader)
    TRAIN_F1 = f1_score(TRUE_LABELS_TRAIN, PREDICTIONS_TRAIN, average='weighted')

    LOSS_TRAIN.append(TRAIN_LOSS)
    F1_TRAIN.append(TRAIN_F1)

    model.eval()
    TEST_LOSS_VAL = 0.0
    PREDICTIONS = []
    TRUE_LABELS = []

    with torch.no_grad():
        for DATA in test_loader:
            INPUTS, LABELS = DATA
            INPUTS = INPUTS.to(DEVICE)
            LABELS = LABELS.to(DEVICE)
            OUTPUTS = model(INPUTS)
            LOSS = criterion(OUTPUTS, LABELS)
            TEST_LOSS_VAL += LOSS.item()
            _, PREDICTED = torch.max(OUTPUTS.data, 1)
            PREDICTIONS.extend(PREDICTED.tolist())
            TRUE_LABELS.extend(LABELS.tolist())

    TEST_LOSS_VAL /= len(test_loader)
    TEST_F1_VAL = f1_score(TRUE_LABELS, PREDICTIONS, average='weighted')

    LOSS_TEST.append(TEST_LOSS_VAL)
    F1_TEST.append(TEST_F1_VAL)

    print(f'Train Loss: {TRAIN_LOSS:.4f} - Train F1: {TRAIN_F1:.4f}')

    if TEST_LOSS_VAL < BEST_VALIDATION_LOSS:
        BEST_VALIDATION_LOSS = TEST_LOSS_VAL
        NO_IMPROVEMENT_COUNT = 0
        torch.save(model.state_dict(), MODEL_SAVE_PATH)

    else:
        NO_IMPROVEMENT_COUNT += 1

    if NO_IMPROVEMENT_COUNT >= PATIENCE:
        print(f'Early stopping after {EPOCH + 1} epochs due to no improvement in validation loss.')
        break

print('Finished Training')
