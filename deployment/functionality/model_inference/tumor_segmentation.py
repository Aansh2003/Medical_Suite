import torch.nn as nn
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy
import cv2
try:
    from functionality.model_inference.UNet import UNet
except:
    from UNet import UNet


transform = transforms.Compose([
    transforms.Resize((256,256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5],
                         std=[0.225, 0.225, 0.225])
])

def segment(PATH,extension=""):
    model = UNet()
    model.load_state_dict(torch.load('/home/dragon/medical_project/Medical_Suite/models/unet_model2.pt',map_location=torch.device('cpu')))

    image = Image.open(PATH).convert('RGB')
    required_size = image.size
    transformed_image = transform(image)

    model.eval()
    output = torch.round(model(transformed_image.unsqueeze(0)))

    final_transform = transforms.Compose([
        transforms.Resize(required_size),
        transforms.Grayscale(),
        transforms.ToPILImage()
    ])

    for value in output:
        mask = final_transform(value)

    image = numpy.array(image.convert('RGB'))
    mask = numpy.array(mask.convert('RGB'))

    color = numpy.array([0,255,0], dtype='uint8')

    masked_img = numpy.where(mask, color, image)
    out = cv2.addWeighted(image, 0.8, masked_img, 0.2,0)

    FINAL_PATH = '/home/dragon/medical_project/Medical_Suite/deployment/segmented_images/'+'mask'+PATH[PATH.rfind('/')+1:]
    cv2.imwrite(FINAL_PATH+extension,out)

    return FINAL_PATH


if __name__ == "__main__":
    segment('/home/dragon/medical_project/Medical_Suite/data/tumor_segmentation/dataset/0.png')