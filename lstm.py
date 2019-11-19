from dataloader import DataLoader
from optimize_features import handle_lastprice_bidprice_askprice
import numpy as np
import keras


def lstm_model():
    model = keras.Sequential()

    model.add(keras.layers.CuDNNLSTM(
        input_shape=(features.shape[1], features.shape[2]),
        units=lstm_unit1,
        return_sequences=True
    ))
    # model.add(keras.layers.Dropout(0.5))

    model.add(keras.layers.CuDNNLSTM(
        units=lstm_unit2,
        return_sequences=False
    ))
    # model.add(keras.layers.Dropout(0.5))

    model.add(keras.layers.Dense(
        1, activation='linear'
    ))
    model.compile(
        loss='mse',
        optimizer='adam'
    )
    return model


if __name__ == '__main__':
    # filename = '20190104'
    filename_set = [
        '20180326', '20180327', '20180328', '20180329', '20180402',
        '20180403', '20180404', '20180409', '20180410', '20180411'
    ]
    # filename_set = [
    #     '20190103'
    # ]
    loader = DataLoader(is_ask=False)

    lstm_unit1 = 32
    lstm_unit2 = 32
    timesteps = 16
    learning_rate = 0.001
    epochs = 2000
    batch_size = 1024

    # features, labels = loader.get_features(date=filename, mode=mode, num_history=timesteps)
    # features = handle_lastprice_bidprice_askprice(features=features)

    features, labels = loader.get_features(date=filename_set[0], num_history=timesteps)
    features = list(handle_lastprice_bidprice_askprice(features=features))
    labels = list(labels)

    for i in range(1, len(filename_set)):
        temp_features, temp_labels = loader.get_features(date=filename_set[i], num_history=timesteps)
        temp_features = handle_lastprice_bidprice_askprice(features=temp_features)
        features.extend(temp_features)
        labels.extend(temp_labels)

    features = np.array(features)
    labels = np.array(labels)

    model = lstm_model()
    model.fit(
        x=features,
        y=labels,
        batch_size=batch_size,
        epochs=epochs,
    )

    model.save('model/lstm_ask_model_3.h5')
    predict = model.predict(x=features, batch_size=batch_size)
