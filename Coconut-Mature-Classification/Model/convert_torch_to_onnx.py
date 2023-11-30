"""
Convert torch model to onnx model

This module convert torch model to onnx model
"""

import torch
from torchvision import models

TORCH_MODEL_PATH = ""                           # Add torch model directory
EXPORT_MODEL_PATH = ""                          # Add onnx model directory

model = models.mobilenet_v2(num_classes=4)      # Modify your model
model.load_state_dict(torch.load(TORCH_MODEL_PATH))
dummy_input = torch.randn(1, 3, 224, 224)       # Modify your desired model input

torch.onnx.export(model,
                  dummy_input,
                  EXPORT_MODEL_PATH,
                  verbose=False,
                  opset_version=12,
                  do_constant_folding=True,
                  input_names = ["images"],
                  output_names = ["output"],
                  dynamic_axes={"images" : {0 : "batch_size"},
                                "output" : {0 : "batch_size"}
                                }
)
