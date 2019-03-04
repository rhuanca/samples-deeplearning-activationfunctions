import keras

from keras.models import Sequential
from keras.layers import Dense, Dropout

from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
from numpy.random import seed

def get_model(activation_function=None):

    model = Sequential()
    model.add(Dense(512, activation=activation_function, input_shape=(784,)))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

    return model

def print_model_details(model):
    model.summary()

