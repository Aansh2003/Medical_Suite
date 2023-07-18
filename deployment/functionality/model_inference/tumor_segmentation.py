import torch.nn as nn
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy
import cv2

class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()

        self.enc1 = UNet.encoder_decoder_block(input_channels=3,output_channels=32)
        self.enc2 = UNet.encoder_decoder_block(input_channels=32,output_channels=64)
        self.enc3 = UNet.encoder_decoder_block(input_channels=64,output_channels=128)
        self.enc4 = UNet.encoder_decoder_block(input_channels=128,output_channels=256)

        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.bottleneck = UNet.encoder_decoder_block(input_channels=256,output_channels=512)

        self.upconv1 = nn.ConvTranspose2d(in_channels=512,out_channels=256,kernel_size=2,stride=2)
        self.upconv2 = nn.ConvTranspose2d(in_channels=256,out_channels=128,kernel_size=2,stride=2)
        self.upconv3 = nn.ConvTranspose2d(in_channels=128,out_channels=64,kernel_size=2,stride=2)
        self.upconv4 =  nn.ConvTranspose2d(in_channels=64,out_channels=32,kernel_size=2,stride=2)

        self.dec1 = UNet.encoder_decoder_block(input_channels=512,output_channels=256)
        self.dec2 = UNet.encoder_decoder_block(input_channels=256,output_channels=128)
        self.dec3 = UNet.encoder_decoder_block(input_channels=128,output_channels=64)
        self.dec4 = UNet.encoder_decoder_block(input_channels=64,output_channels=32)

        self.final_conv = nn.Conv2d(in_channels=32,out_channels=1,kernel_size=1)

        
    def forward(self, x):
        #encoding
        encoding1 = self.enc1(x)
        encoding2 = self.pool1(encoding1)
        encoding2 = self.enc2(encoding2)
        encoding3 = self.pool2(encoding2)
        encoding3 = self.enc3(encoding3)
        encoding4 = self.pool3(encoding3)
        encoding4= self.enc4(encoding4)
        bottleneck = self.pool4(encoding4)

        bottleneck = self.bottleneck(bottleneck)
        #decoding and concat
        decoding1 = self.upconv1(bottleneck)
        decoding1 = torch.cat((decoding1, encoding4), dim=1)
        decoding1 = self.dec1(decoding1)

        decoding2 = self.upconv2(decoding1)
        decoding2 = torch.cat((decoding2, encoding3), dim=1)
        decoding2 = self.dec2(decoding2)

        decoding3 = self.upconv3(decoding2)
        decoding3 = torch.cat((decoding3, encoding2), dim=1)
        decoding3 = self.dec3(decoding3)

        decoding4 = self.upconv4(decoding3)
        decoding4 = torch.cat((decoding4, encoding1), dim=1)
        decoding4 = self.dec4(decoding4)

        ans = torch.sigmoid(self.final_conv(decoding4))
        return ans


    @staticmethod
    def encoder_decoder_block(input_channels,output_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels=input_channels,out_channels=output_channels,kernel_size=3,padding=1),
            nn.BatchNorm2d(num_features=output_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=output_channels,out_channels=output_channels,kernel_size=3,padding=1),
            nn.BatchNorm2d(num_features=output_channels),
            nn.ReLU(inplace=True),
        )

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5],
                         std=[0.225, 0.225, 0.225])
])

def segment(PATH,extension=None):
    model = UNet()
    model.load_state_dict(torch.load('/home/dragon/medical_project/Medical_Suite/models/unet_model2.pt',map_location=torch.device('cpu')))

    image = Image.open(PATH).convert('RGB')
    required_size = image.size[0]
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