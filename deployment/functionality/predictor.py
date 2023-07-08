def predict(type,prediction):
    database = {'brain_tumor':['Glioma','Meningioma','No Tumor','Pituitary']}
    return database[type][prediction]

if __name__ == "__main__":
    print(predict('brain_tumor',0))