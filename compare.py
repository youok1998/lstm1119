import os
from dataloader import DataLoader
from util import addone
from numpy import array
from keras.models import load_model
from numpy import load


date = '20180413'
loader = DataLoader(is_ask=True)
features = load('npys/features_' + date + '.npy')
labels = load('npys/labels_' + date + '.npy')
model = load_model('model/lstm_ask_model_2.h5')
predict = model.predict(features, 1024)
predict = array(predict).reshape(-1)

if not os.path.exists('out'):
    os.mkdir('out')

addone(
        'out/' + date + '_predict_test.csv',
        ['TrueLabels', 'PredictLabels'],
        zip(labels, predict)
)
