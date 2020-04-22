#####################################################
#                  Liam Floyd
#                    CS461
#                   Program 4
#####################################################
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import review
import count


def main():
    # Get a list of all brands appearing more than once
    brand_list = get_major_brand()
    # Get a list of the top 100 varieties
    var_list = get_top_var()
    # Get a list of all the styles and origins
    style_list, origin_list = get_sty_ori()
    # Load all the data with the processing, all values will be encoded to the index of previous lists
    ratings_list = load_data(brand_list, var_list, style_list, origin_list)

    column_names = ["Brand", "Variety", "Style", "Origin", "Stars"]
    data_to_set = {"Brand": [], "Variety": [], "Style": [], "Origin": [], "Stars": []}

    for item in ratings_list:
        data_to_set["Brand"].append(item.brand)
        data_to_set["Variety"].append(item.variety)
        data_to_set["Style"].append(item.style)
        data_to_set["Origin"].append(item.origin)
        data_to_set["Stars"].append(item.stars)

    dataset = pd.DataFrame(data_to_set, columns=column_names)
    print(dataset)

    # Split data for training and testing
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats = train_stats.transpose()
    print(train_stats)
    print(dataset)

    # Split target from data
    train_labels = train_dataset.pop('Stars')
    test_labels = test_dataset.pop('Stars')

    normed_train_data = norm(train_dataset, train_stats)
    normed_test_data = norm(test_dataset, train_stats)

    model = build_model(train_dataset)

    print(model.summary())

    example_batch = normed_train_data[:10]
    example_result = model.predict(example_batch)
    print(example_result)

    EPOCHS = 1000

    history = model.fit(
        normed_train_data, train_labels,
        epochs=EPOCHS, validation_split=0.2, verbose=0,
        callbacks=[tfdocs.modeling.EpochDots()])


def load_data(major_brands, top_vars, styles, origins):
    ratings = []
    # major_brands = get_major_brand()
    # top_vars = get_top_var()

    ratings_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    for line in ratings_file:
        val = line.split(',')
        # Keep clean of Title row
        if val[0] == "Review #":
            continue
        # Keep clean of dirty input rows
        if len(val) < 3:
            continue
        # Discard unrated data
        try:
            star = val[5]
        except:
            continue

        # Check if the brand is a main brand or "Other"
        # Encode as index (or 1 outside of index for Other) to make numeric Brand values
        if val[1] not in major_brands:
            brand_name = len(major_brands)
        else:
            brand_name = major_brands.index(val[1])
        # Count only the top 100 varieties
        vars_list = val[2].split()
        valid_vars = []
        for item in vars_list:
            if item in top_vars:
                valid_vars.append(top_vars.index(item))

        for var in valid_vars:
            temp_review = review.Review(val[0], brand_name, var, styles.index(val[3]), origins.index(val[4]), star)
            ratings.append(temp_review)

    ratings_file.close()
    return ratings


def get_major_brand():
    """Count each instance of a brand and return a list of major brands"""
    in_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    brand_count = []
    for line in in_file:
        val = line.split(',')
        # Handle invalid lines
        if len(val) < 3:
            continue

        # Add the first value if the list is empty
        if len(brand_count) == 0:
            temp_brand = count.Count(val[1])
            brand_count.append(temp_brand)
        else:
            for item in brand_count:
                # If the brand is already present, increase the count by 1
                if val[1] == item.name:
                    item.add_count()
                    break

            # If brand hasn't been accounted for, add it
            temp_brand = count.Count(val[1])
            brand_count.append(temp_brand)

    # Create list of Brands with more than 1 occurrence
    major_brands = []
    for brand_object in brand_count:
        if brand_object.count > 1:
            major_brands.append(str(brand_object))

    in_file.close()
    return major_brands


def get_top_var():
    """Find the top 100 variety keywords and return a list of strings"""
    in_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    raw_vars = []
    for line in in_file:
        val = line.split(',')
        if len(val) < 3:
            continue

        varieties = val[2].split()

        for var in varieties:
            if len(raw_vars) == 0:
                temp_brand = count.Count(var)
                raw_vars.append(temp_brand)
            else:
                for item in raw_vars:
                    # If the var is already present, increase the count by 1
                    if var == item.name:
                        item.add_count()
                        break
                # If var hasn't been accounted for, add it
                temp_brand = count.Count(var)
                raw_vars.append(temp_brand)

    var_list = []
    for cnt in range(100):
        # Take the top 100 varieties and add them to the list
        temp_var = cnt_max(raw_vars)
        raw_vars.remove(temp_var)
        var_list.append(str(temp_var))

    in_file.close()
    return var_list


def get_sty_ori():
    """Return lists for both Style and Origin for encoding"""
    in_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    style_list = []
    origin_list = []

    for line in in_file:
        val = line.split(',')
        if len(val) < 3:
            continue

        if len(style_list) == 0:
            style_list.append(val[3])
        else:
            if val[3] not in style_list:
                style_list.append(val[3])

        if len(origin_list) == 0:
            origin_list.append(val[4])
        else:
            if val[4] not in origin_list:
                origin_list.append(val[4])

    in_file.close()
    return style_list, origin_list


def build_model(dataset):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(dataset.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
    return model


def cnt_max(in_list):
    """Returns a max from a list of count objects"""
    temp_max = count.Count("benchmark")
    for item in in_list:
        if item.count > temp_max.count:
            temp_max = item
    return temp_max


def norm(x, stats):
    return (x - stats['mean']) / stats['std']


if __name__ == "__main__":
    main()
