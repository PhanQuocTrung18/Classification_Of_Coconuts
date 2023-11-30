"""
Module evaluation

This module contains functions for evaluating a model on a test set.
"""

import torch
import torchvision
from torchvision import transforms, models
from torch.utils.data import DataLoader
from torch import nn
from sklearn.metrics import f1_score
from tqdm import tqdm

def evaluate_f1(model, test_loader, device):
    """
    Evaluate the F1 score of a model on a given test set.

    Parameters:
    - model (torch.nn.Module): The trained model.
    - test_loader (torch.utils.data.DataLoader): DataLoader for the test set.
    - device (torch.device): Device to which the model and data should be moved.

    Returns:
    - float: Weighted F1 score.
    """
    model.eval()
    all_true_labels = []
    all_predictions = []

    with torch.no_grad():
        for data in tqdm(test_loader, desc='Evaluating'):
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            all_predictions.extend(predicted.tolist())
            all_true_labels.extend(labels.tolist())

    weighted_f1 = f1_score(all_true_labels, all_predictions, average='weighted')
    print("Weighted F1 Score:", weighted_f1)
    return weighted_f1

if __name__ == "__main__":
    # Set up transforms and datasets
    test_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_data = torchvision.datasets.ImageFolder(
        root=r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\val', transform=test_transforms)

    # Set up MobileNetV2 model
    model_eval = models.mobilenet_v2(pretrained=True)
    NUM_CLASSES = 3
    model_eval.classifier[1] = nn.Linear(model_eval.last_channel, NUM_CLASSES)

    for param in model_eval.features.parameters():
        param.requires_grad = False

    # Set up device
    device_eval = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Load the trained model state
    model_eval.load_state_dict(torch.load(r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\Model\MobileNet_v2_model.pt', map_location=device_eval))
    # Create data loader for test set
    BATCH_SIZE = 64  # Thêm dòng này để đảm bảo BATCH_SIZE đã được định nghĩa
    TEST_LOADER = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)

    # Move model to device
    model_eval.to(device_eval)

    print("Start evaluating...")

    # Evaluate and print F1 Score
    f1_result = evaluate_f1(model_eval, TEST_LOADER, device_eval)
    print("Weighted F1 Result:", f1_result)

    print("Evaluation finished.")
