import os
import torch
import open_clip
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torch.optim as optim
import torch.nn as nn
from open_clip import create_model_from_pretrained, get_tokenizer
import gradio as gr

MODEL_NAME = 'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224'


# Load the model and config files from the Hugging Face Hub
model, preprocess = create_model_from_pretrained(MODEL_NAME)
tokenizer = get_tokenizer(MODEL_NAME)

# Load the Processor and Model
# processor = AutoProcessor.from_pretrained('microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')

# device = torch.device("cpu")
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(f'Using device: {device}')
model.to(device)
model.eval()

transform = transforms.Compose([
    # transforms.RandAugment(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.481, 0.457, 0.408], std=[0.268, 0.261, 0.275])
])

classifier = nn.Sequential(
    nn.Linear(512, 512),
    nn.ReLU(),
    nn.Linear(512, 33)
)
classifier.load_state_dict(torch.load('models/openclip_dibas_finetuned.pth'))
classifier.to(device)
classifier.eval()

example_dir = "data/DIBaS_Dataset_png/"
class_names = os.listdir(example_dir)
class_names.sort()
class_map = {i: class_name  for i, class_name in enumerate(class_names)}

def classify(image):
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    image = transform(image).unsqueeze(0).to(device)
    # text = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    image_features = model.encode_image(image)
    # text_features = model.encode_text(text)
    # features = torch.cat((image_features, text_features), dim=1)
    output = classifier(image_features)
    _, predicted = torch.max(output.data, 1)
    y_hat = predicted.item()
    return class_map[y_hat]
    # logits_per_image, logits_per_text = model.logit_scale * image_features @ text_features.t()
    # probs = F.softmax(logits_per_image, dim=-1)


example_class_dirs = os.listdir(example_dir)

example_files = []
for class_dir in example_class_dirs:
    class_dir_path = os.path.join(example_dir, class_dir)
    files = [os.path.join(class_dir_path, f) for f in os.listdir(class_dir_path)]
    files = files[:3]
    example_files.extend(files)

# Filter out non-image files and limit to PNG images
example_files = [f for f in example_files if f.endswith(".png")]
example_labels = [f"{example_files[i].split("/")[-2]}_{(i)%5}"  for i in range(len(example_files))]

# example_images = [os.path.join(example_dir, f) for f in example_files if f.endswith(".png")]
# example_images = example_images[:5]  # Limit to 5 examples for demonstration



demo = gr.Interface(
    fn=classify,
    inputs=["image"],
    outputs=["label"],
    examples=example_files,
    examples_per_page=100,
    example_labels=example_labels,
    
)

demo.launch()