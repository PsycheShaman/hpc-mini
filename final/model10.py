import numpy as np
import matplotlib.pyplot as plt

tracks = np.load("/scratch/vljchr004/6_tracklets_large_calib_train/0_tracks.npy")

infosets = np.load("/scratch/vljchr004/6_tracklets_large_calib_train/0_info_set.npy")

train = tracks.reshape((-1, 17, 24, 1))

labels = np.repeat(infosets[:, 0], 6)

train = (train-np.max(train))/np.max(train)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(train, labels, test_size=0.33, random_state=42)

import tensorflow as tf

model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(filters=16,kernel_size=(3,3),strides=1, padding='valid',activation="relu"))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128,activation="sigmoid"))
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1,activation="sigmoid"))

adam = tf.train.AdamOptimizer(learning_rate=0.00001)

model.compile(loss='binary_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])

batch_size=32

epochs=50

history=model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_split=0.2,
              shuffle=True)

#unit = model.get_weights()[0]
#
#unit = model.get_weights()[0][:,:,0,0]
#
#plt.imshow(unit)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('/home/vljchr004/hpc-mini/final/model10_history1.png', bbox_inches='tight')
plt.close()


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('/home/vljchr004/hpc-mini/final/model10_history2.png', bbox_inches='tight')

plt.close()

model.probs = model.predict_proba(x_test)

import numpy as np
np.savetxt("/home/vljchr004/hpc-mini/final/model10_results.csv", np.array(model.probs), fmt="%s")

np.savetxt("/home/vljchr004/hpc-mini/final/model10_y_test.csv", np.array(y_test), fmt="%s")

model.save('/home/vljchr004/hpc-mini/final/model10_.h5')  # creates a HDF5 file 'my_model.h5'
del model

print("<-----------------------------done------------------------------------------>")
