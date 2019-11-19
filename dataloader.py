import os
import pandas as pd
import numpy as np
from optimize_features import handle_lastprice_bidprice_askprice


class DataLoader:
    def __init__(self, is_ask, data_path='new_quote/'):
        self.is_ask = is_ask
        self.data_path = data_path

    def get_features(self, date, num_prefix=200, num_history=16, num_output=1):
        if not os.path.exists('npys'):
            os.mkdir('npys')
        if os.path.exists('npys/features_' + date + '.npy'):
            return np.load('npys/features_' + date + '.npy'), np.load('npys/labels_' + date + '.npy')
        df_total = pd.read_csv(self.data_path + '/' + date + '.csv', encoding='gbk')
        df = df_total.fillna(0)
        df1 = df.iloc[num_prefix: -1, :]
        data = df1.values
        features, labels = [], []
        num_data = len(data)

        num_steps = num_data - num_history - num_output
        for i in range(num_steps):
            feature, label = self.get_features_each_line(data, i + num_history, num_history)
            features.append(feature)
            labels.append(label)
        features = np.array(features)
        features = handle_lastprice_bidprice_askprice(features)
        labels = np.array(labels)
        np.save('npys/features_' + date + '.npy', features)
        np.save('npys/labels_' + date + '.npy', labels)
        return features, labels

    def get_features_each_line(self, data, lid, num_history):
        cols = data[lid - num_history + 1: lid + 1]
        feature = cols[:, [4, 5, 6, 7, 8]]
        feature_ = []
        for i in feature:
            feature_.append([float(f) for f in i])
        label = cols[-1, -1] if self.is_ask else cols[-1, -2]
        return feature_, label


if __name__ == '__main__':
    loader = DataLoader(is_ask=True)
    feats, labels = loader.get_features('20180412')
    print(feats)
    print(labels)
