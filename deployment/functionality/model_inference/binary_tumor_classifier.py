from PIL import Image
import torch
from torchvision import *
import torch.nn as nn


def classify(PATH):
    image = Image.open(PATH).convert('RGB')
    transformer = transforms.Compose([transforms.Resize((256,256)),transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    image = transformer(image)
<<<<<<< HEAD
    model = models.resnet50(pretrained=True)
    nr_filters = model.fc.in_features
    model.fc = nn.Linear(nr_filters, 4)
    model.load_state_dict(torch.load('/home/dragon/Medical_Suite/models/resnet50_4-way.pt',map_location=torch.device('cpu')))
    image = image.unsqueeze(0)
    out = model(image)
    _,pred_t = torch.max(out, dim=1)
    prob = max((torch.softmax(out,dim=1)).tolist()[0])
    print(pred_t,prob)
    return (int(pred_t),float(prob))
=======
    model = models.densenet121(pretrained=False)
    model.classifier = nn.Sequential(
        nn.Linear(1024, 256),
        nn.Dropout(p=0.1),
        nn.ReLU(),
        nn.Linear(256, 4)
    )
    model.load_state_dict(torch.load('/home/dragon/Medical_Suite/models/densenet121.pt',map_location=torch.device('cpu')))
    image = image.unsqueeze(0)
    out = model(image)
    _,pred_t = torch.max(out, dim=1)
    return (int(pred_t),float((torch.softmax(out,dim=1).max())))
>>>>>>> 627738138e15f0cc1e5f848d2427a06aa792667d
    

if __name__=="__main__":
    classify('/home/dragon/Medical_Suite/deployment/uploads/file1')
    