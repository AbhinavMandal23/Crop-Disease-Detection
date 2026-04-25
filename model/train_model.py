import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os

# -------------------------
# CONFIG
# -------------------------
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15

DATASET_PATH = "dataset/train"   # 👈 change if needed
MODEL_SAVE_PATH = "model/crop_model.h5"
CLASS_NAMES_PATH = "model/class_names.json"

# -------------------------
# DATA GENERATOR
# -------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# -------------------------
# SAVE CLASS NAMES
# -------------------------
class_names = list(train_gen.class_indices.keys())

with open(CLASS_NAMES_PATH, "w") as f:
    json.dump(class_names, f)

print("✅ Class names saved")

# -------------------------
# MODEL
# -------------------------
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -------------------------
# CALLBACKS
# -------------------------
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint("model/best_model.h5", save_best_only=True)
]

# -------------------------
# TRAIN
# -------------------------
model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen,
    callbacks=callbacks
)

# -------------------------
# SAVE MODEL
# -------------------------
model.save(MODEL_SAVE_PATH)

print("✅ Model saved at:", MODEL_SAVE_PATH)