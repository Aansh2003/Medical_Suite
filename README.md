# Medical Suite
 
## Project Description
This is a ML/DL project to create a medical metastack which is able to detect various diseases based on scans and other data. Currently brain tumor detection and segmentation as well as retinal disease detection is fully operational and deployed.

## Analytics
Brain Tumor classification - Test accuracy: 93%\
Brain Tumor segmentation - Test Loss: 0.32%
\


Retinal classification - Test accuracy: 91%

## Setting up
clone the repositor onto your local system
```
git clone https://github.com/Aansh2003/Medical_Suite.git
```

Install all dependencies by running the following code
```
pip3 install -r requirements.txt
```
Create a throwaway Gmail account which will be used by the application to send Emails to the users.
The account will need 2FA and app password generation. Go to settings and type app passwords on the search bar.\
\
![oie_lQsTN7ndL1Aa](https://github.com/Aansh2003/Medical_Suite/assets/96300383/2e8cdea1-2ae9-4612-8e46-f32851cf5f91)

Generate a 16 character long password, for example:
> email: example@gmail.com\
> password: abcd abcd abcd abcd

Go to the functionality folder and create a file called login_credentials.txt
```
nano medical_suite/deployment/functionality/login_credentials.txt
```
Type in the email ID on the first line and password on the second line, for example\
\
![oie_dYqrmfdtL1FR](https://github.com/Aansh2003/Medical_Suite/assets/96300383/9f7ded89-6f0c-4b73-b10d-7f6b85c70265)\
The application can now connect to this email and send emails containing the attached files and the output of the model.

## Running the server
Go to the deployment folder
```
cd
cd medical_suite/deployment
```
Type the following command to run the server
```
python3 main_server.py
```
Type in any one of the links shown on the terminal to open the website, for example:
> Running on http://127.0.0.1:5000

Type this on the web browser
http://127.0.0.1:5000/brain_tumor
The website should look like this:\
\
![oie_lrkpxvodDbGd](https://github.com/Aansh2003/Medical_Suite/assets/96300383/a2ea67ec-a8bd-4ced-8139-4d6410d71da1)

## Output
After submitting basic details the following email will be sent.\
\
![oie_ZiBgAlS5juOy](https://github.com/Aansh2003/Medical_Suite/assets/96300383/60324775-52b6-40ad-aace-3dd7ff4e199a)
\

### Brain Tumor
This classifies between 4 classes ie- meningioma, glioma and pituitary tumor and also normal scans.
If a tumor is detected, the image will be passed through a segmentation model and the following output will be generated.\
![oie_UDo75R8A6goB](https://github.com/Aansh2003/Medical_Suite/assets/96300383/f8629ede-f5bb-4fa7-b3dd-1b429184d975)
\
A similar attachment will be sent in the email with the image containing the segmentation mask.

### Retinal diseases detection
This classifies between 4 classes ie- cataract, diabetic retinopathy and glaucoma and also normal retinal images.

## Further work
Creating a fully functional website with a proper home page.
Creating more models to detect other diseases.
Improving the email distribution system

## References
[ResNet](https://arxiv.org/abs/1512.03385)\
[UNet](https://arxiv.org/abs/1505.04597)\
[DenseNet](https://arxiv.org/abs/1608.06993)
