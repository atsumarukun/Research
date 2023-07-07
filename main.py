import random
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.utils import to_categorical
from keras.layers import Dense, InputLayer

from utils.files import read_files
from config import DATA_PATH

def main():
    labels = ["JOY", "ACC", "FEA", "SUR", "SAD", "DIS", "ANG", "ANT", "NEU", "OTH"]
    files = read_files(DATA_PATH)
    random.shuffle(files)
    nomalize = lambda x: (x - min(x)) / (max(x)  - min(x))
    x_train = np.array([nomalize(f["data"]) for f in files[:int(len(files) * 0.9)]], "int16")
    t_train = to_categorical(np.array([labels.index(f["path"][-8:-5]) for f in files[:int(len(files) * 0.9)]]), len(labels))
    x_test = np.array([nomalize(f["data"]) for f in files[int(len(files) * 0.9):]], "int16")
    t_test = to_categorical(np.array([labels.index(f["path"][-8:-5]) for f in files[int(len(files) * 0.9):]]), len(labels))

    model = Sequential()
    model.add(InputLayer(input_shape=(x_train.shape[1],)))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(len(labels), activation='relu'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.summary()

    history = model.fit(x_train, t_train, epochs=10, batch_size=8)

    plt.plot(np.arange(len(history.history["loss"])), history.history["loss"], label="loss")
    plt.plot(np.arange(len(history.history["accuracy"])), history.history["accuracy"], label="acc")
    plt.legend()
    plt.show()

    loss, acc = model.evaluate(x_test, t_test)
    print(f"loss: {loss}, acc: {acc}")

if __name__ == "__main__":
    main()
