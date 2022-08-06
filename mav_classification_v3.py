# -*- coding: utf-8 -*-
"""MAV Classification v3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AnQ-bl1rmaWnTw2AFTuR5QKL98OG2ros

# **Machine Learning models for Classification (Tensorflow + Keras)**
*Artificial Neural Networks to analyze 3-Year prognostication for patients with brain arteriovenous malformation (AVM) after stereotactic radiosurgery: a study for a small and heterogeneous group in Peru.*
> *Developed by*: **Mirko J. Rodríguez** (https://www.linkedin.com/in/mirkorodriguez/)

---

## **Setup Environment**
---

Tensorflow 2 (include Keras)
"""

import tensorflow as tf
print('Tensorflow: ',tf.__version__)

from tensorflow import keras
print('TF Keras: ',keras.__version__)

import platform
print('Python:',platform.python_version())

import sklearn 
print('sklearn: {}'. format(sklearn. __version__))

# Commented out IPython magic to ensure Python compatibility.
# %%bash 
# # Install external librearies
# python -m pip uninstall matplotlib
# pip install matplotlib==3.1.3
# pip install autoviz # EDA
# pip install keras-visualizer # Visualizer for ANN

"""## **Dataset Loading**
---

**Mount Google Drive:**
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

"""**Read dataset:**"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# # Read folders in google drive
# MYPROJECT="/content/drive/MyDrive/UNI/DSc/Ciclo 5/Taller de Machine Learning/Session Final - 06 Agosto/Final/3. Code"
# ls -l "$MYPROJECT"
# echo "$MYPROJECT" > config.txt

# Import Dataset
import pandas as pd
project_folder = open('config.txt').readline().rstrip('\n')
csv_file = project_folder + "/dataset/dataset-mav-msalas.v6.csv"
dataset = pd.read_csv(csv_file)

# Show info
dataset.info()

"""## **Exploratory Data Analysis (EDA)**
---

"""

""" First observations (10) """
dataset.head(10)

""" Describe dataset """
dataset.describe()

# Commented out IPython magic to ensure Python compatibility.
from autoviz.AutoViz_Class import AutoViz_Class

# EDA using autoviz
# %matplotlib inline
autoviz = AutoViz_Class().AutoViz(csv_file)

"""## **Data Preprocessing**
---
"""

# Dataset copy
dataset_final = dataset.copy()

# Reduced dataset
COLUMNS_TO_REMOVE = ['id','residence','education_level','health_insurance','mri_examination','ct_examination','das_examination']
dataset_final.drop(COLUMNS_TO_REMOVE, inplace=True, axis=1)

dataset_final.head(10)

"""**Split dataset (Train / Test):**"""

from sklearn.model_selection import train_test_split

# Train / Test (30% test size)
dataset_train, dataset_test = train_test_split(dataset_final, test_size = 0.3, random_state = 1)

"""**Validate Imbalanced dataset:**"""

target_count = dataset_train['curation'].value_counts()
target_count.plot(kind='bar', title='Dataset');
print(dataset_train.shape)

"""**Balanceo (SMOTE + Tomek)**"""

import numpy as np
from imblearn.combine import SMOTETomek

num_columns = dataset_train.shape[1]
dataset_columns = dataset_train.columns

# Obteniendo valores a procesar
X = dataset_train.iloc[:, 0:num_columns - 1].values
y = dataset_train.iloc[:, num_columns - 1].values

# SMOTE Tomek
smt = SMOTETomek(sampling_strategy='not majority')
X_sm, y_sm = smt.fit_resample(X, y)

balanced_dataset = np.column_stack((X_sm, y_sm))

# Dataset final normalizado
dataset_train = pd.DataFrame(balanced_dataset,columns=dataset_columns, dtype=np.float64)

# Print Balanceo por clase
target_count = dataset_train['curation'].value_counts()
target_count.plot(kind='bar', title='Dataset');
print(dataset_train.shape)

"""**Getting X and Y:**"""

# Features name
var_dependent = ['curation']
var_independent = list(dataset_train.columns)
var_independent.remove('curation');

"""**A) Training dataset**"""

# Train dataset
X_train = dataset_train[var_independent]
Y_train = dataset_train[var_dependent]

print("X_train size is %s" % str(X_train.shape))
X_train.head(5)

print("Y_train size is %s" % str(Y_train.shape))
Y_train.head(5)

"""**B) Testing dataset**"""

# Test dataset
X_test = dataset_test[var_independent]
Y_test = dataset_test[var_dependent]

print("X_test size is %s" % str(X_test.shape))
X_test.head(5)

print("Y_test size is %s" % str(Y_test.shape))
Y_test.head(5)

"""## **Training dataset Preprocessing**
---

**Training data Scaling:**
"""

from sklearn.preprocessing import StandardScaler

# Scaling
scaler = StandardScaler()
X_train[var_independent] = scaler.fit_transform(X_train[var_independent])

print ("\nTraining dataset:")
X_train.head(10)

"""---
## **Artificial Neural Network (find function)**
---

**Architecture of Artificial Neural Network:**
"""

# Importando Keras y Tensorflow
from keras.models import Sequential
from keras.layers import Dense

num_neuronas_entrada = X_train.shape[1]

def crear_red_neuronal(kernel_init, func_activation, optimizer):
    # Inicializando la Red Neuronal
    neural_network = Sequential()

    # Agregado la Capa de entrada y la primera capa oculta
    neural_network.add(Dense(units = 20, kernel_initializer = kernel_init, activation = func_activation, input_dim = num_neuronas_entrada))

    # Agregando capa oculta
    neural_network.add(Dense(units = 20, kernel_initializer = kernel_init, activation = func_activation))

    # Agregando capa oculta
    neural_network.add(Dense(units = 10, kernel_initializer = kernel_init, activation = func_activation))

    # Agregando capa oculta
    neural_network.add(Dense(units = 5, kernel_initializer = kernel_init, activation = func_activation))

    # Agregando capa de salida
    neural_network.add(Dense(units = 1, kernel_initializer = kernel_init, activation = 'sigmoid'))

    neural_network.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    return neural_network

from keras.wrappers.scikit_learn import KerasClassifier

# Obteniendo la red plantilla
red_neuronal_obtenida = KerasClassifier(build_fn = crear_red_neuronal)

"""**Definiendo valores posibles para los Hiper-parámetros:**"""

# Posibles valores de los Hiper-parámetros de Arquitectura
kernel_init = ['uniform', 'normal']    # ['uniform', 'lecun_uniform', 'normal', 'zero', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform']
func_activation = ['relu','tanh']   # ['relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']

# Posibles valores de los Hiper-parámetros de compilación
optimizer = [ 'SGD', 'Adam']

# Otros
batch_size = [8, 16, 32]
nb_epoch = [40, 50, 100]

# Diccionario de valores
param_values = dict(kernel_init=kernel_init, 
                    func_activation=func_activation,
                    optimizer=optimizer,
                    batch_size=batch_size,
                    nb_epoch=nb_epoch)

print(param_values)

"""**Entrenando la Red:**"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# from sklearn.model_selection import GridSearchCV
# 
# SCORING = 'balanced_accuracy' # Se busca optimizar esta métrica
# 
# # Entrenamiento
# grid_model = GridSearchCV(estimator = red_neuronal_obtenida, param_grid = param_values, scoring = SCORING)
# grid_model.fit(X_train, Y_train)

"""**Obteniendo resultados:**"""

print("Mejor score: %f usando params: %s \n" % (grid_model.best_score_, grid_model.best_params_))

means = grid_model.cv_results_['mean_test_score']
stds = grid_model.cv_results_['std_test_score']
params = grid_model.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

"""**Architecture for Artificial Neural Network: Visualization**"""

# Mejor score: 0.435027 usando params: {'batch_size': 16, 'func_activation': 'tanh', 'kernel_init': 'normal', 'nb_epoch': 40, 'optimizer': 'Adam'} 

neural_network = crear_red_neuronal('normal', 'tanh', 'Adam');

# ANN architecture
neural_network.summary()

"""**Train Artificial Neural Network:**"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# BATCH_SIZE = 16
# EPOCHS = 40
# 
# iterations = neural_network.fit(X_train, Y_train, batch_size = BATCH_SIZE, epochs = EPOCHS)

# Ploting results
import matplotlib.pyplot as plt
plt.title('Training')
plt.plot(iterations.history['loss'], color='blue')
plt.plot(iterations.history['accuracy'], color='orange')
plt.legend(['loss', 'accuracy'])
plt.show()

"""**Saving function (model):**"""

# Keras format
function_name = "avm_function.h5"
neural_network.save(project_folder + "/model/" + function_name, save_format='h5')

"""**Prediction**

**Load function (model):**
"""

# Load function/model (h5) from disk
from tensorflow.keras.models import load_model

project_folder = open('config.txt').readline().rstrip('\n')
function_name = "avm_function.h5"
loaded_function = load_model(project_folder + "/model/" + function_name)

# ANN Architecture
loaded_function.summary()

# ANN Graph
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from keras_visualizer import visualizer
visualizer(neural_network, format='jpg')
fig = plt.figure(figsize=(10, 10))
plt.grid(False)
plt.axis('off')
plt.imshow(image.load_img('graph.jpg'))
plt.show()

"""**PREDICTION:**"""

X_test = dataset_test[var_independent]
X_test.head(5)

# Scaling
X_test[var_independent] = scaler.transform(X_test[var_independent])
X_test.head(5)

# Prediction for X_test
Y_pred = loaded_function.predict(X_test)
dataset_test['Prediction'] = Y_pred

# Show new dataset
dataset_test.head(15)

THREASHOLD = 0.5 
Y_pred_final = (Y_pred > THREASHOLD).astype(int)

dataset_test['PredictionFinal'] = Y_pred_final

# Show new dataset
dataset_test.head(15)

"""**Confusion Matrix (aka Error Matrix):**"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

cm = confusion_matrix(Y_test, Y_pred_final)
print ("\nConfusion Matrix: \n", cm)

import seaborn as sns
import matplotlib.pyplot as plt     
ax=plt.subplot()
sns.heatmap(cm, annot=True, fmt='g', ax=ax, cbar=False, cmap="Blues");
ax.set_xlabel('Predicted');
ax.set_ylabel('True'); 
ax.set_title('Confusion Matrix');

"""**Metrics:**"""

TN, FP, FN, TP = cm.ravel()

# Accuracy
accuracy = (TP+TN)/(TP+TN+FP+FN)
# Sensitivity/Recall
sensitivity = TP/(TP+FN)
# Specificity
specificity = TN/(TN+FP)
# Positive Predictive Value (PPV)/ Precision
PPV = TP/(TP + FP)
# Negative Predictive Value (NPV)
NPV = TN/(TN + FN)

print("Accuracy: ","({:.2%})".format(accuracy))
print("Sensitivity:","({:.2%})".format(sensitivity))
print("Specificity:","({:.2%})".format(specificity))
print("PPV:","({:.2%})".format(PPV))
print("NPV:","({:.2%})".format(NPV))

print("Accuracy Balanceado:","({:.2%})".format((sensitivity + specificity)/2))

"""---
## **Support Vector Machines (find function)**
---

**KERNEL: linear**
"""

from sklearn.svm import SVC 

model = SVC(C=0.1, break_ties=False, cache_size=200, class_weight=None, coef0=0.0,
                decision_function_shape='ovr', degree=3, gamma=1, kernel='linear',
                max_iter=-1, probability=True, random_state=None, shrinking=True, tol=0.001,
                verbose=False)

model.fit(X_train, Y_train)

# Predicciones
Y_pred = model.predict(X_test)
# print("Y_pred:", Y_pred)

Y_pred_final = (Y_pred > THREASHOLD).astype(int)

"""**Confusion Matrix (aka Error Matrix):**"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

cm = confusion_matrix(Y_test, Y_pred_final)
print ("\nConfusion Matrix: \n", cm)

import seaborn as sns
import matplotlib.pyplot as plt     
ax=plt.subplot()
sns.heatmap(cm, annot=True, fmt='g', ax=ax, cbar=False, cmap="Blues");
ax.set_xlabel('Predicted');
ax.set_ylabel('True'); 
ax.set_title('Confusion Matrix');

"""**Metrics:**"""

TN, FP, FN, TP = cm.ravel()

# Accuracy
accuracy = (TP+TN)/(TP+TN+FP+FN)
# Sensitivity/Recall
sensitivity = TP/(TP+FN)
# Specificity
specificity = TN/(TN+FP)
# Positive Predictive Value (PPV)/ Precision
PPV = TP/(TP + FP)
# Negative Predictive Value (NPV)
NPV = TN/(TN + FN)

print("Accuracy: ","({:.2%})".format(accuracy))
print("Sensitivity:","({:.2%})".format(sensitivity))
print("Specificity:","({:.2%})".format(specificity))
print("PPV:","({:.2%})".format(PPV))
print("NPV:","({:.2%})".format(NPV))

print("Accuracy Balanceado:","({:.2%})".format((sensitivity + specificity)/2))

"""**KERNEL: poly**"""

from sklearn.svm import SVC 

model = SVC(C=0.1, break_ties=False, cache_size=200, class_weight=None, coef0=0.0,
                decision_function_shape='ovr', degree=3, gamma=1, kernel='poly',
                max_iter=-1, probability=True, random_state=None, shrinking=True, tol=0.001,
                verbose=False)

model.fit(X_train, Y_train)

# Predicciones
Y_pred = model.predict(X_test)
# print("Y_pred:", Y_pred)

Y_pred_final = (Y_pred > THREASHOLD).astype(int)

"""**Confusion Matrix (aka Error Matrix):**"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

cm = confusion_matrix(Y_test, Y_pred_final)
print ("\nConfusion Matrix: \n", cm)

import seaborn as sns
import matplotlib.pyplot as plt     
ax=plt.subplot()
sns.heatmap(cm, annot=True, fmt='g', ax=ax, cbar=False, cmap="Blues");
ax.set_xlabel('Predicted');
ax.set_ylabel('True'); 
ax.set_title('Confusion Matrix');

"""**Metrics:**"""

TN, FP, FN, TP = cm.ravel()

# Accuracy
accuracy = (TP+TN)/(TP+TN+FP+FN)
# Sensitivity/Recall
sensitivity = TP/(TP+FN)
# Specificity
specificity = TN/(TN+FP)
# Positive Predictive Value (PPV)/ Precision
PPV = TP/(TP + FP)
# Negative Predictive Value (NPV)
NPV = TN/(TN + FN)

print("Accuracy: ","({:.2%})".format(accuracy))
print("Sensitivity:","({:.2%})".format(sensitivity))
print("Specificity:","({:.2%})".format(specificity))
print("PPV:","({:.2%})".format(PPV))
print("NPV:","({:.2%})".format(NPV))

print("Accuracy Balanceado:","({:.2%})".format((sensitivity + specificity)/2))

"""---
## **Decision Trees (find function)**
---

**DT:**
"""

from sklearn.tree import DecisionTreeClassifier

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)

# Train Decision Tree Classifer
clf = clf.fit(X_train,Y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

Y_pred_final_tree = (Y_pred > THREASHOLD).astype(int)

"""**Confusion Matrix (aka Error Matrix):**"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

cm = confusion_matrix(Y_test, Y_pred_final_tree)
print ("\nConfusion Matrix: \n", cm)

import seaborn as sns
import matplotlib.pyplot as plt     
ax=plt.subplot()
sns.heatmap(cm, annot=True, fmt='g', ax=ax, cbar=False, cmap="Blues");
ax.set_xlabel('Predicted');
ax.set_ylabel('True'); 
ax.set_title('Confusion Matrix');

"""**Metrics:**"""

TN, FP, FN, TP = cm.ravel()

# Accuracy
accuracy = (TP+TN)/(TP+TN+FP+FN)
# Sensitivity/Recall
sensitivity = TP/(TP+FN)
# Specificity
specificity = TN/(TN+FP)
# Positive Predictive Value (PPV)/ Precision
PPV = TP/(TP + FP)
# Negative Predictive Value (NPV)
NPV = TN/(TN + FN)

print("Accuracy: ","({:.2%})".format(accuracy))
print("Sensitivity:","({:.2%})".format(sensitivity))
print("Specificity:","({:.2%})".format(specificity))
print("PPV:","({:.2%})".format(PPV))
print("NPV:","({:.2%})".format(NPV))

print("Accuracy Balanceado:","({:.2%})".format((sensitivity + specificity)/2))

"""Visualizing DT:"""

from six import StringIO
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True, feature_names = var_independent, class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('diabetes.png')
Image(graph.create_png())