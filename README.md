# Forked from [StarterKit](https://github.com/HSV-AI/hackathon-starterkit)

Working area for the 2025 HudsonAlpha Tech Challenge - https://hudsonalpha.org/techchallenge/

# Challenge: Microscope Vision Challenge

Explore the use of advanced microscopy and cutting-edge computer vision techniques—leveraging Large Language Models (LLMs), Large Vision Models (LVMs), or custom machine learning algorithms—to rapidly and accurately identify pathogens, disease biomarkers, and other relevant patterns in microscopic images. By advancing the speed and precision of image analysis, participants can help transform fields ranging from medical diagnostics to environmental science, enabling faster data-driven decisions and groundbreaking discoveries.

# Approach:

Use AI techniques, models, product to the maximum extent possible to create a submission to this challenge.

## Ideation

The first step was to ask Perplexity (free tier) and ChatGPT (paid tier) what to do:

```
I want to try and work on a challenge for a hackathon. Here's the description of the challenge:
"Explore the use of advanced microscopy and cutting-edge computer vision techniques—leveraging Large Language Models (LLMs), Large Vision Models (LVMs), or custom machine learning algorithms—to rapidly and accurately identify pathogens, disease biomarkers, and other relevant patterns in microscopic images. By advancing the speed and precision of image analysis, participants can help transform fields ranging from medical diagnostics to environmental science, enabling faster data-driven decisions and groundbreaking discoveries."

What would you suggest as a one day project to solve this challenge
```

Perplexity Chat Link - https://www.perplexity.ai/search/i-want-to-try-and-work-on-a-ch-dDXaeGPaS6auDMROwg6kPA

ChatGPT Link - https://chatgpt.com/share/e/67c32037-67c4-8007-bb80-9f655b8ded38

## Models:

- [BiodmedCLIP](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) - a biomedical vision-language foundation model that is pretrained on PMC-15M, a dataset of 15 million figure-caption pairs extracted from biomedical research articles in PubMed Central, using contrastive learning.

- [CXR-Pixtral](https://huggingface.co/williampeoch/cxr-pixtral) - a fine-tuned version of the Pixtral-12B (Mistral AI) model, specifically designed for Medical Report Generation (MRG) from chest X-ray images. It excels in generating detailed and accurate medical reports based on chest X-rays.

## Datasets:

- [Image Data Resource](https://idr.openmicroscopy.org/cell/) - a public repository of image datasets from published scientific studies, where the community can submit, search and access high-quality bio-image data.
- [Environmental Microorganism Dataset](https://github.com/NEUZihan/EMDS-5) - In EMDS-5, there are 21 classes of environmental microorganisms (EMs).
In each calss, there are 20 EM original images and their corresponding binary groud truth images. 
Furthermore, there are two ground truth image sets: the first is for single objects (EMDS5-GTS), and the second is for multple objects (EMDS5-GTM).
- [Digital Image of Bacterial Species](https://github.com/gallardorafael/DIBaS-Dataset) - a dataset of 33 bacterial species with around 20 images for each species.
- [BiomedParseData](https://huggingface.co/datasets/microsoft/BiomedParseData) - official dataset repository for "A foundation model for joint segmentation, detection and recognition of biomedical objects across nine modalities".
- [CXR_BioXAi_Hackathon_2024](https://huggingface.co/datasets/romprr/CXR_BioXAi_Hackathon_2024) - No information provided
- [BIOSCAN-30k](https://huggingface.co/datasets/Voxel51/BIOSCAN-30k) - images of insects - found through hugging face search.
- [Lymphnode Cancer Biopsy Dataset](https://huggingface.co/datasets/LuminaAI/RCL-Lymphnode-Cancer-Biopsy-100K) - contains 100k biopsy images of lymphnode cancer tissues, divided into two classes: benign and malignant. Each sample is stored in a separate image file, organized into respective class folders. 