import numpy as np

array = np.random.random((200,150, 50))

np.save("test_array.npy", array)