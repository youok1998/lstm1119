from pandas import read_csv
from PIL import Image
import numpy as np
import csv
import time


def get_dealer(dealer_type=2, filename="output/character.csv"):
    cols = ['id', 'main_signal']
    dealer_list = read_csv(filename, usecols=cols)
    dealer_list = dealer_list.values
    dealer_chosen = list()
    for dealer in dealer_list:
        if dealer[1] == dealer_type:
            dealer_chosen.append(dealer[0])
    return dealer_chosen


def timestamp_to_str(timestamp=None, format='%H:%M:%S'):
    if timestamp:
        return time.strftime(format, time.localtime(timestamp))

    else:
        return time.strftime(format, time.localtime())


def read_day_info(date):
    dealer_list = get_dealer()
    filename = 'output/' + date + '.csv'
    info = read_csv(filename, usecols=['time', 'agent', 'offset', 'volume'], encoding='GBK')
    info = info.values
    buy_tick = dict()
    sell_tick = dict()
    for temp in info:
        if int(temp[1]) in dealer_list:
            if temp[3] > 0:
                if buy_tick.get(timestamp_to_str(temp[0])) is None:
                    buy_tick[timestamp_to_str(temp[0])] = temp[3]
                else:
                    buy_tick[timestamp_to_str(temp[0])] = buy_tick[timestamp_to_str(temp[0])] + temp[3]
            else:
                if sell_tick.get(timestamp_to_str(temp[0])) is None:
                    sell_tick[timestamp_to_str(temp[0])] = -temp[3]
                else:
                    sell_tick[timestamp_to_str(temp[0])] = sell_tick[timestamp_to_str(temp[0])] - temp[3]
    return buy_tick, sell_tick


def generate_new_csv(date):
    buy_tick, sell_tick = read_day_info(date=date)
    read_filename = 'quote/' + date + '/sc1809.csv'
    reader = read_csv(read_filename, iterator=True)
    time = read_csv(read_filename, usecols=['UpdateTime']).values
    bid_list = list()
    ask_list = list()
    for temp in time:
        if buy_tick.get(temp[0]) is None:
            bid_list.append(0)
        else:
            bid_list.append(buy_tick.get(temp[0]))
        if sell_tick.get(temp[0]) is None:
            ask_list.append(0)
        else:
            ask_list.append(sell_tick.get(temp[0]))

    header = True

    try:
        df = reader.get_chunk(50000)
        df['Bid'] = bid_list
        df['Ask'] = ask_list
        new_filename = 'new_quote/' + date + '.csv'
        df.to_csv(new_filename, mode='a', index=False, header=header, encoding='GBK')
        header = False
    except StopIteration:
        pass


def addone(path, columns, data):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for row in data:
            writer.writerow(row)


def picture_to_black_white(date):
    filename = 'picture/' + date + '.png'
    img = Image.open(filename)
    img = img.convert("L")
    img.save('bw_picture/' + date + '.png')


def picture_to_array(date):
    filename = 'bw_picture/' + date + '.png'
    im = Image.open(filename)
    im2 = np.array(im)
    return im2


def array_to_picture(array, date):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] < 200:
                array[i][j] = 0
            else:
                array[i][j] = 255
    image = Image.fromarray(array)
    image.save('new_picture/' + date + '.png')


def transfer_picture_to_black_white_picture(date):
    picture_to_black_white(date)
    temp_array = picture_to_array(date)
    array_to_picture(temp_array, date)


def new_picture_to_array(date):
    filename = 'new_picture/' + date + '.png'
    im = Image.open(filename)
    im2 = np.array(im)
    return im2


if __name__ == '__main__':
    # transfer_picture_to_black_white_picture('20181003')
    generate_new_csv('20180412')
    # print(timestamp_to_str(1522026342, format='%H:%M:%S'))
    # print(read_day_info('20180326'))
