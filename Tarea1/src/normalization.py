from pathlib import Path
import numpy as np
import json


def getData(properties):
    """
    Given the paths in properties, load the dataset and proces it
    to return an array with parsed data, also applies 1-hot codding
    codification for the class
    """
    data = Path.cwd() / properties["dataset"]
    mapping = Path.cwd() / properties["classes"]
    print('loading file {}'.format(mapping))
    with open(mapping) as json_file:
        classes = json.load(json_file)[0]

    print('reading file {}'.format(data))
    parsed_data = [[], [], [], [], []]
    try:
        with open(data) as reader:
            for line in reader:
                ldata = line.strip().split(',')
                data_class=[]
                for i in range(properties["number_of_classes"]):
                    if i==classes[ldata[4]]:
                        data_class.append(1)
                    else:
                        data_class.append(0)

                parsed_data[0].append(float(ldata[0]))  # sepal_length
                parsed_data[1].append(float(ldata[1]))  # sepal_width
                parsed_data[2].append(float(ldata[2]))  # petal_length
                parsed_data[3].append(float(ldata[3]))  # petal_width
                parsed_data[4].append(data_class)       # one hot encoded class
    except:
        pass
    return parsed_data


def normalize_data(data, min_num, max_num):
    """
    Normalices the given data using the given parameters
    """
    ndata = np.array(data)
    nmin = ndata.min()
    nmax = ndata.max()
    normaliced_data = []
    for num in data:
        norm = (((num - nmin) * (max_num - min_num)) / (nmax - nmin)) + min_num
        normaliced_data.append(norm)
    return normaliced_data


def prepare_data(data):
    """
    It takes the data, normalices it nad returns it
    """
    sepal_length = normalize_data(data[0], 0, 1)
    sepal_width = normalize_data(data[1], 0, 1)
    petal_length = normalize_data(data[2], 0, 1)
    petal_width = normalize_data(data[3], 0, 1)
    real_class = data[4]

    ndata = []
    for i in range(len(sepal_length)):
        ndata.append([np.array([
            sepal_length[i],
            sepal_width[i],
            petal_length[i],
            petal_width[i]]),
            np.array(real_class[i])
        ])

    return ndata


def normalize(properties):
    """
    Given the paths in properties, prepares the dataset and
    saves it in a npy file
    """
    print("Getting data")
    data = getData(properties)
    print("Data obtained")
    print("Normalizing data")
    ndata = np.array(prepare_data(data))
    print("Data normalized")

    data_path = Path.cwd() / properties["data"]
    np.save(data_path, ndata)
