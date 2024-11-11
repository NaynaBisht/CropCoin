import torch
import time
import random
import os
from PIL import Image
from torchvision import transforms
import torchvision
import torch.nn as nn
import math
from tqdm import tqdm
from check import Stock

# Define your custom model architecture
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.alpha = 0.7
        self.base = torchvision.models.resnet18(pretrained=True)
        
        for param in list(self.base.parameters())[:-15]:
            param.requires_grad = False

        self.base.classifier = nn.Sequential()
        self.base.fc = nn.Sequential()
        
        self.block1 = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
        )
        
        self.block2 = nn.Sequential(
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 9)
        )
        
        self.block3 = nn.Sequential(
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        x = self.base(x)
        x = self.block1(x)
        y1, y2 = self.block2(x), self.block3(x)
        return y1, y2

# Load the saved model weights
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Model().to(device)
model.load_state_dict(torch.load("_model.pth", map_location=device))
model.eval()

# Define your labels
fruit_labels = ['banana', 'capsicum', 'cucumber', 'oranges', 'potato', 'tomato']
fresh_labels = ['Fresh', 'Spoiled']

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Adjust as per model input size
    transforms.ToTensor()
])

# Directory containing test images
test_folder = "C:/Users/vinay/Downloads/archive/dataset/Test/rottentamto"  # Replace with your actual folder path

# Function to predict freshness and output results
def predict_freshness(image_path):
    # Load and transform the image
    img = Image.open(image_path).convert('RGB')
    img_transformed = transform(img).unsqueeze(0).to(device)

    # Prediction
    with torch.no_grad():
        pred_fruit, pred_fresh = model(img_transformed)
        pred_fresh_class = torch.argmax(pred_fresh, axis=1).item()

    # Generate freshness percentage based on freshness class
    freshness_percentage = random.uniform(76, 92) if pred_fresh_class == 1 else random.uniform(83, 98)

    freshness_status = fresh_labels[pred_fresh_class]
    status = list()
    status.append([freshness_status, freshness_percentage])
    return status

s = Stock()
# Loop through each image in the test folder every second
for filename in os.listdir(test_folder):
    if filename.lower().endswith(('.png')):  # Ensure only image files are processed
        img_path = os.path.join(test_folder, filename)
        status = predict_freshness(img_path)
        s.fluctuate(status)
        time.sleep(10)  # Wait for 1 second before processing the next image
