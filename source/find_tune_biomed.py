import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from open_clip import create_model_from_pretrained, get_tokenizer
from transformers import AdamW
import os

# Custom dataset class
class CustomImageDataset(Dataset):
    def __init__(self, img_dir, transform=None):
        self.img_dir = img_dir
        self.transform = transform
        self.classes = sorted(os.listdir(img_dir))  # Sorted for consistency
        self.images = []
        self.labels = []
        # Load all image paths and labels
        for class_name in self.classes:
            class_dir = os.path.join(img_dir, class_name)
            if os.path.isdir(class_dir):
                for img_name in os.listdir(class_dir):
                    img_path = os.path.join(class_dir, img_name)
                    self.images.append(img_path)
                    self.labels.append(class_name)

        # self.images = [f for f in os.listdir(img_dir) if f.endswith('.tif')]
        # self.labels = [img.split('_')[0] for img in self.images]  # Assuming filenames are "label_imagename.jpg"

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

# Load BiomedCLIP model and tokenizer
model, preprocess = create_model_from_pretrained('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
tokenizer = get_tokenizer('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')

# Prepare dataset and dataloader
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = CustomImageDataset(img_dir='data/DIBaS_Dataset', transform=transform)
print(len(dataset))
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Prepare labels
unique_labels = list(set(dataset.labels))
label_to_id = {label: i for i, label in enumerate(unique_labels)}

# Fine-tuning setup
device = torch.device('cuda')
model = model.to(device)
optimizer = AdamW(model.parameters(), lr=1e-5)
criterion = torch.nn.CrossEntropyLoss()

# Fine-tuning loop
num_epochs = 5
for epoch in range(num_epochs):
    model.train()
    for images, labels in dataloader:

        print(f"Images {len(images)}")

        images = images.to(device)
        label_ids = torch.tensor([label_to_id[label] for label in labels]).to(device)
        
        optimizer.zero_grad()
        
        # Get image features
        image_features = model.encode_image(images)
        
        # Get text features for all labels
        text_inputs = tokenizer([f"this is a photo of {label}" for label in unique_labels])
        text_features = model.encode_text(text_inputs.to(device))
        
        # Compute logits
        logits = image_features @ text_features.T
        
        loss = criterion(logits, label_ids)
        loss.backward()
        optimizer.step()
        print(f"Loss: {loss.item()}")
    
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

# Save the fine-tuned model
torch.save(model.state_dict(), 'fine_tuned_biomedclip.pth')
