# Coconut-Mature-Classification
This is a mini project of subject DPL302m. This repository hosts an AI-based system for accurately classifying the maturity of coconuts (young, mature, old) by utilizing computer vision techniques to make accurate maturity assessments based on coconut images.

# Table of Contents
* Motivation
* Web Application
* Dataset
* Installation
* Usage
* Training
* Training your own model
* Limits
* Contributors

# Motivation
### Background
* Coconut cultivation and its associated industries constitute pivotal components of economic activity in many tropical regions.
* Several products are derived from distinct categories of coconuts, including those in their young, mature, and old stages.
    
### Pain point
* Contemporary coconut farming practices heavily rely on traditional methods for assessing maturity, differentiating between young, mature, and old stages.
* The widespread use of manual assessments proves labor-intensive and poses efficiency challenges as coconut quantities escalate.
    
### Objective
* Develop a computer vision-based coconut maturity classification system.
* This system expects:
    * Facilitating decision-making in coconut processing industries. 
    * Reducing human labor and error in coconut quality assessment.

# Web Application

### Diagram
![diagram](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/121301557/63fd97c7-3290-44f0-a91e-ee75a751e360)

      
# Dataset
Link dataset: https://drive.google.com/drive/folders/1IoUpBAI8BWnbe_s-eyFtMbCO16AEHO8b?usp=sharing

### Data Source:
* The primary source of data for this project encompasses information derived from both online repositories, specifically Roboflow and Kaggle, and real-world datasets. The online repositories, Roboflow and Kaggle, offer a wealth of curated data. In parallel, real-world datasets supplement this digital information, ensuring the inclusion of authentic and varied instances.
* Sample data:
![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/121301557/9db1064a-fa4a-4774-b4d6-d86c6ff75c2f)

### Data Preprocessing
* Crop image: Crop all images in the dataset into squares
![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/121301557/8f4a2bd8-e66c-4b4d-8f63-0509d030954a)

### Data Distribution
* Original data:
    * Young Coconut: 407
    * Mature Coconut: 1142
    * Old Coconut: 1024
    * Other: 1061
![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/88047081/27f0c73a-cd22-42f1-9a3c-b9fb1b468213)


### Data Augmentation
* Augmentation on 'Young Coconut' class:
------------------------------------
    transforms.RandomHorizontalFlip(): Apply random horizontal flip to the image with a default probability of 0.5
    transforms.RandomRotation(10): Apply random rotation to the image with a rotation range of ±10 degrees
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)): Apply random resized crop to the image, resizing it to 224x224, with a scale factor between 0.8 and 1.0
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)): Apply random affine transformation to the image with a rotation range of 0 degrees and translation of 0.1 in both directions
    transforms.RandomPerspective(distortion_scale=0.2, p=0.5): Apply random perspective transformation to the image with a distortion scale of 0.2 and a probability of 0.5

* Data Distribution after augmentation on 'Young Coconut' class:
![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/121301557/71345fff-35d3-4c30-9fab-7457fdbcca1f)


* Augmentation on the whole dataset:
------------------------------------
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.1),
    transforms.RandomVerticalFlip(p=0.1),
    transforms.RandomRotation(degrees=15),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.2
    ),
    transforms.GaussianBlur(kernel_size=3),
    transforms.RandomResizedCrop(size=224, scale=(0.8, 1)),
    transforms.RandomGrayscale(p=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]

### Data Splitting
* Run file: ``` DataSplit.py ```
![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/88047081/f92cd668-38c5-45be-9a97-2436b01308dc)


# Installation
Follow these steps to install and run the project on your local machine.
### Prerequisites
Make sure you have the following prerequisites installed on your system:
- [Python](https://www.python.org/) (version 3.9 or later)
- [pip](https://pip.pypa.io/en/stable/)
### Clone the Repository
```bash
git clone https://github.com/TruongTrongTien/Coconut-Mature-Classification.git
cd Coconut-Mature-Classification
```

### Set up a Virtual Environment
Create a virtual environment to isolate project dependencies:
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows:
```bash
.\venv\Scripts\activate
```

- On UNIX or MacOS:
```bash
source venv/bin/activate
```

### Install Dependencies 
```bash
pip install -r requirements.txt
```

# Usage

### Run the Application
```bash
flask run
```

# Training

### Criterion
Cross Entropy Loss

### Optimizer
* Lion Optimizer, lr = 1e-4, weight decay = 1e-2
* Number of epochs: 30
* Result:
    * Train Loss:  0.0822
    * Val Loss: 0.1559
    * Train F1: 0.9578
    * Val F1: 0.9392
![model training chart](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/121301557/e9dc1fce-8e8e-4893-b81e-84b6979e1562)

# Training your own model
Within the project structure, meticulously curated files have been organized in the Web and Model folders, catering to the essential resources required for the comprehensive training of your individualized model.

# Challenges
### Dataset Limitations:
* Poor quality and insufficient quantity
* Challenges to model robustness
### Accuracy Challenges:
* Real-time scenarios affected by environmental conditions
* Sensitivity to camera placement
### Model Scope:
* Specialized for coconut classification from single-object images
* Potential for enhancement in handling complex scenes or multi-object scenarios
### Industrial Deployment Challenges:
* Practical constraints and conditions in industrial settings
* Demands careful consideration for successful deployment.

# Future works
### Diversification of Dataset:
* Strategic efforts to collect more diverse data
* Aiming for inclusivity in environmental conditions and coconut variations
### Model Optimization:
* Exploration of models tailored to the dataset's characteristics
* Rigorous optimization of the existing model parameters
### Evolution to Coconut Detection:
* Shifting focus from single-object coconut classification
* Transitioning towards a more comprehensive detection framework in images
### Integration into Industrial Workflow:
* Aligning the model for seamless integration into industrial processes
* Adapting to the practical constraints and requirements of an industrial setting.

# Contributors

### Thanks goes to these wonderful people:
* [Truong Trong Tien](https://github.com/TruongTrongTien)
* [Phan Quoc Trung](https://github.com/PhanQuocTrung18)
* [Diep Gia Dong](https://github.com/DiepDong)
* [Pham Quoc Hung](https://github.com/Hungpham03)
* [Mai Xuan Huu](https://github.com/MaiXuanHuu)
