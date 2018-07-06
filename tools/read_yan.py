# import pickle
#
# with open('data.pkl', 'rb') as f:
#     data_x = pickle.load(f)
#     data_y = pickle.load(f)
#     return standardize(data_x), data_y
#
# train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size=0.4, random_state=40)
# dev_x, test_x, dev_y, test_y, = train_test_split(test_x, test_y, test_size=0.5, random_state=40)