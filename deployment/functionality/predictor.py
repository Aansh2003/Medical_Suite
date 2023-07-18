def predict(type,prediction):
    database = {'brain_tumor':['Glioma','Meningioma','No Tumor','Pituitary'],'retinal':['cataract','diabetic retinopathy','glaucoma','normal']}
    return database[type][prediction]

if __name__ == "__main__":
    print(predict('brain_tumor',0))