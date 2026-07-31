import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Load images and labels
    print("Loading data...")
    images, labels = load_data(sys.argv[1])

    # Convert labels to one-hot encoding
    print("Preparing training and testing data...")
    labels = tf.keras.utils.to_categorical(labels)

    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images),
        np.array(labels),
        test_size=TEST_SIZE,
        random_state=42
    )

    # Build model
    print("Building model...")
    model = get_model()

    # Train model
    print("Training model...")
    model.fit(
        x_train,
        y_train,
        epochs=EPOCHS,
        batch_size=32,
        validation_data=(x_test, y_test)
    )

    # Evaluate model
    print("Evaluating model...")
    model.evaluate(x_test, y_test, verbose=2)

    # Save model if filename provided
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.") 


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Return (images, labels).
    """

    images = []
    labels = []

    # Loop through every category (0 - 42)
    for category in range(NUM_CATEGORIES):

        print(f"Loading category {category}")

        category_path = os.path.join(data_dir, str(category))

        # Skip if folder doesn't exist
        if not os.path.isdir(category_path):
            print(f"Folder not found: {category_path}")
            continue

        # Get all files in this category
        files = os.listdir(category_path)
        print(f"Category {category}: {len(files)} images")

        # Read every image
        for i, filename in enumerate(files):

            if i % 200 == 0:
                print(f"  Processed {i}/{len(files)}")

            image_path = os.path.join(category_path, filename)

            image = cv2.imread(image_path)
            if image is None:
                continue

            # Resize image
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            # Normalize pixel values
            image = image.astype("float32") / 255.0

            images.append(image)
            labels.append(category)

    print(f"Loaded {len(images)} images.")
    return images, labels



def get_model():
    """
   Returns a compiled convolutional neural network model.
    """

    model = tf.keras.models.Sequential([

        tf.keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        tf.keras.layers.Conv2D(
            32,
            (3, 3),
            activation="relu"
        ),

        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(
            64,
            (3, 3),
            activation="relu"
        ),

        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(
            128,
            activation="relu"
        ),

        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(
            NUM_CATEGORIES,
            activation="softmax"
        )
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
