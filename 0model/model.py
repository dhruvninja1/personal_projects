# Hypothesis - To clasify an animal into mammal, bird, etc using other data
# CSV from https://www.kaggle.com/datasets/uciml/zoo-animal-classification/data?select=zoo.csv

# Imports
import matplotlib as mpl
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# uncomment the next line if on google colab
#from google.colab import files; uploaded=files.upload()

# Reading the CSV
# Change the path to the file name
data=pd.read_csv('0model/zooData.csv')

# Selecting which columns to keep
keep = ['hair', 'feathers', 'eggs', 'airborne', 'aquatic', 'backbone', 'fins', 'class_type']
# Dropping the other ones
for item in data.columns: 
    if item not in keep:
        data.drop(item, axis=1, inplace=True)

print(data.head(5))

# Group the selected attributes
selected_Attributes = ['hair', 'feathers', 'eggs', 'airborne', 'aquatic', 'backbone', 'fins']
plots={}
colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink'] 

# Making graphs
for i, item in enumerate(selected_Attributes):
    grouped_data = data.groupby('class_type')[item].sum()

    plt.figure(figsize=(8, 5)) 
    ax = grouped_data.plot.bar(
        title=f'Amount with {item} per Class Type',
        xlabel='Class Type (1-7)', 
        ylabel=f'Count of Animals with {item}',
        rot=0,
        color=colors[i]
    )
    class_labels = {1: "Mammal", 2: "Bird", 3: "Reptile", 4: "Fish",
                     5: "Amphibian", 6: "Bug", 7: "Invertebrate"}
    ax.set_xticklabels([class_labels[int(x.get_text())] for x in ax.get_xticklabels()])

    plots[f"plot{i}"] = ax
    plt.tight_layout() 
    plt.show()
    plt.show()


# Selecting training and testing data

inputs_train, inputs_test, labels_train, labels_test = \
    model_selection.train_test_split(data[['hair', 'feathers', 
                                           'eggs', 'airborne', 'aquatic', 
                                           'backbone', 'fins', ]].values, data['class_type'].values, test_size=0.2)


# Setting up KNN
knn = KNeighborsClassifier(n_neighbors = 5)

# Learning based on inputs and labels from our dataset
knn.fit(inputs_train, labels_train)

# Predicting
predictions = knn.predict(inputs_test)
print(f"Prediction score: {round(accuracy_score(labels_test, predictions)*100, 3)}%")


# Turning the numbers into strings for readability
def predict(input: list) -> str:
    a = knn.predict([input])
    if a==1:
        return "Mammal"
    elif a==2:
        return "Bird"
    elif a==3:
        return "Reptile"
    elif a==4:
        return "Fish"
    elif a==5:
        return "Amphibian"
    elif a==6:
        return "Bug"
    elif a==7:
        return "Invertebrate"
    else:
        return "Idk"
    
# Testing
print(predict([1, 0, 0, 0, 0, 1, 0]))