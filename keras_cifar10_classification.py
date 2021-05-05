# -*- coding: utf-8 -*-
"""Keras CIFAR10 Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14XyoWRos2zX8Ez0RySl4Je_ut5r2jFw4
"""

from numpy.random import seed
seed(888)
from tensorflow.random import set_seed
set_seed(404)

import os
import numpy as np
import tensorflow as tf
import keras
import seaborn as sns
from keras.datasets import cifar10
from IPython.display import display
from keras.preprocessing.image import array_to_img
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import itertools
from keras.callbacks import TensorBoard
from time import strftime
from sklearn.metrics import confusion_matrix

"""#Constants"""

LABEL_NAME=['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
IMAGE_WIDTH=32
LOG_DIR='/tensorboard_cifar_logs/'
IMAGE_HEIGHT=32
IMAGE_PIXEL=IMAGE_WIDTH*IMAGE_HEIGHT
COLOR_CHANNELS=3
TOTAL_INPUTS=IMAGE_PIXEL*COLOR_CHANNELS
VALIDATION_SIZE=10000
SMALL_TRAIN_SIZE=1000

(x_train,y_train),(x_test,y_test)=cifar10.load_data()

"""#Explore the data"""

x_train[0]

pic=array_to_img(x_train[7])
display(pic)

y_train.shape

LABEL_NAME[y_train[7][0]]

plt.imshow(x_train[4])
plt.xlabel(LABEL_NAME[y_train[4][0]])
plt.show()

for i in range(100):
  plt.imshow(x_train[i])  
  plt.xlabel(LABEL_NAME[y_train[i][0]])
  plt.show()

x_train,x_test=x_train/255,x_test/255

x_train=x_train.reshape(x_train.shape[0],TOTAL_INPUTS)
x_test=x_test.reshape(len(x_test),TOTAL_INPUTS)

x_val=x_train[:VALIDATION_SIZE]
y_val=y_train[:VALIDATION_SIZE]
x_train=x_train[VALIDATION_SIZE:]
y_train=y_train[VALIDATION_SIZE:]
y_train.shape

"""#Create a small dataset"""

x_train_xs=x_train[:SMALL_TRAIN_SIZE]
y_train_xs=y_train[:SMALL_TRAIN_SIZE]

"""#Define neural networks"""

model_l=Sequential([
                     Dense(units=128,input_dim=TOTAL_INPUTS,activation='relu',name='m1_hidden1'),
                     Dense(units=64,activation='relu',name='m1_hidden2'),
                     Dense(16,activation='relu',name='m1_hidden3'),
                     Dense(10,activation='softmax',name='m1_hidden4')
 ])

 model_l.compile(optimizer='adam',loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])

model_l.summary()

"""#Tensorboard"""

def get_tensorboard(model_name):
  folder_name=f'{model_name} at model_l at {strftime("%H %M")}'
  dir_paths=os.path.join(LOG_DIR,folder_name)
  try:
    os.makedirs(dir_paths)
  except OSError as err:
    print(err.strerror)
  else:
    print('Successfully created directory')
  return TensorBoard(log_dir=dir_paths)

"""#Fit the model"""

samples_per_batch=1000

nr_epochs=300
model_l.fit(x_train_xs,y_train_xs,batch_size=samples_per_batch,epochs=nr_epochs,callbacks=[get_tensorboard('Model 1')],validation_data=(x_v al,y_val))

"""#Include Dropout method"""

model_2=Sequential()
#Add dropout layer
model_2.add(Dropout(0.2,seed=42,input_shape=(TOTAL_INPUTS,)))
model_2.add(Dense(128,activation='relu',name='m2_hidden1'))
model_2.add(Dense(64,activation='relu',name='m2_hidden2'))
model_2.add(Dense(16,activation='relu',name='m2_hidden3'))
model_2.add(Dense(10,activation='softmax',name='m2_output'))

model_2.compile(optimizer='adam',loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])

nr_epochs=100
model_2.fit(x_train,y_train,batch_size=samples_per_batch,epochs=nr_epochs,callbacks=[get_tensorboard('Model 2')],validation_data=(x_val,y_val))

model_3=Sequential()
#Add dropout layer
model_3.add(Dropout(0.2,seed=42,input_shape=(TOTAL_INPUTS,)))
model_3.add(Dense(128,activation='relu',name='m3_hidden1'))
model_3.add(Dropout(0.25,seed=42))
model_3.add(Dense(64,activation='relu',name='m3_hidden2'))
model_3.add(Dense(16,activation='relu',name='m3_hidden3'))
model_3.add(Dense(10,activation='softmax',name='m3_output'))

model_3.compile(optimizer='adam',loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])

nr_epochs=100
model_3.fit(x_train_xs,y_train_xs,batch_size=samples_per_batch,epochs=nr_epochs,callbacks=[get_tensorboard('Model 3')],validation_data=(x_val,y_val))

"""#Prediction on Individual Images"""

x_val[0].shape

test=np.expand_dims(x_val[0],axis=0)
test.shape

model_2.predict(test)

for i in range(10):
  test=np.expand_dims(x_val[i],axis=0)
  print(f'actual value is {y_val[i]}')
  print(f'The predicted value is {model_2.predict_classes(test)}')

test_loss,test_accuracy=model_2.evaluate(x_test,y_test)  
print(f'Test loss is {test_loss} and accuracy is {test_accuracy}')

"""#Confusion matrix"""

predictions=model_2.predict_classes(x_test)
conf_matrix=confusion_matrix(y_test,predictions)

nr_rows=conf_matrix.shape[0]
nr_cols=conf_matrix.shape[1]
sns.set()
plt.figure(figsize=(10,10))
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('Actual Labels')
tick_marks=np.arange(10)
plt.yticks(tick_marks,LABEL_NAME)
plt.xticks(tick_marks,LABEL_NAME)
plt.imshow(conf_matrix)
plt.colorbar()
for i,j in itertools.product(range(10),range(10)):
  plt.text(j,i,conf_matrix[i][j])
plt.show()

