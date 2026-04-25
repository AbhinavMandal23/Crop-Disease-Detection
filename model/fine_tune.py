import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# -------------------------
# CONFIG
# -------------------------
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 2   # keep small

DATASET_PATH = "dataset/train"
MODEL_PATH = "model/crop_model.h5"

# -------------------------
# DATA
# -------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
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
# LOAD MODEL
# -------------------------
model = tf.keras.models.load_model(MODEL_PATH)

# -------------------------
# UNFREEZE LAST LAYERS
# -------------------------
base_model = model.layers[0]  # MobileNetV2

base_model.trainable = True

# Freeze most layers, unfreeze last 30
for layer in base_model.layers[:-30]:
    layer.trainable = False

# -------------------------
# COMPILE AGAIN
# -------------------------
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),  # very low LR
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("🔧 Fine-tuning started...")

# -------------------------
# TRAIN
# -------------------------
model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen
)

# -------------------------
# SAVE UPDATED MODEL
# -------------------------
model.save(MODEL_PATH)

print("✅ Fine-tuned model saved!")