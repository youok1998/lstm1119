
# 作用：
# 将features中的前三个属性：
# lastprice, bidprice, askprice进行差值处理
def handle_lastprice_bidprice_askprice(features):
    for first_layer in range(len(features)):
        num_history = len(features[0])
        for second_layer in range(num_history):
            if second_layer != 15:
                features[first_layer][num_history - second_layer - 1][0] -=\
                    features[first_layer][num_history - second_layer - 2][0]
                features[first_layer][num_history - second_layer - 1][1] -= \
                    features[first_layer][num_history - second_layer - 2][1]
                features[first_layer][num_history - second_layer - 1][3] -= \
                    features[first_layer][num_history - second_layer - 2][3]
                features[first_layer][num_history - second_layer - 1][0] = \
                    round(features[first_layer][num_history - second_layer - 1][0], 1)
                features[first_layer][num_history - second_layer - 1][1] = \
                    round(features[first_layer][num_history - second_layer - 1][1], 1)
                features[first_layer][num_history - second_layer - 1][3] = \
                    round(features[first_layer][num_history - second_layer - 1][3], 1)
            else:
                features[first_layer][0][0] = 0
                features[first_layer][0][1] = 0
                features[first_layer][0][3] = 0
    return features


def handle_k_features(features):
    for first_layer in range(len(features)):
        temp = features[first_layer][-1]
        for second_layer in range(len(features[0])):
            if second_layer != 15:
                if features[first_layer][second_layer] != 0:
                    features[first_layer][second_layer] = features[first_layer][second_layer] - temp
                else:
                    features[first_layer][second_layer] = 0
            else:
                features[first_layer][second_layer] = 0
    return features
