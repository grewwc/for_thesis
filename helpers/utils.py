import numpy as np

def norm_features(values):
    mean = np.mean(values, axis=0)
    std = np.std(values, axis=0)
    try:
        values = (values - mean) / std
    except Warning as e:
        print(e, std)
    return values