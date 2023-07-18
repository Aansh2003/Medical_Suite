from PIL import Image
import torch
from torchvision import *
import torch.nn as nn


def classify(PATH):
    image = Image.open(PATH).convert('RGB')
    transformer = transforms.Compose([transforms.Resize((224,224)),transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    image = transformer(image)

    model = torch.hub.load('pytorch/vision:v0.10.0', 'densenet121', pretrained=True)
    model.classifier = nn.Sequential(
        nn.Linear(1024, 256),
        nn.Dropout(p=0.1),
        nn.ReLU(),
        nn.Linear(256, 4),
        nn.Softmax(dim=1)
    )
    model.load_state_dict(torch.load('/home/dragon/medical_project/Medical_Suite/models/dense_retinal.pt',map_location=torch.device('cpu')))

    image = image.unsqueeze(0)
    out = model(image)
    _,pred_t = torch.max(out, dim=1)
    prob = out.tolist()[0][int(pred_t)]
    print(pred_t,prob)
    return (int(pred_t),(prob))

if __name__ == "__main__":
    print(classify('/home/dragon/medical_project/Medical_Suite/data/retinal_classification/Testing/normal/2672_right.jpg'))