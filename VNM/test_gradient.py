import numpy as np
import matplotlib.pyplot as plt

def main():

    x = [1., 2., 3., 4., 5., 6., 7., 8.]
    y = [1., 2., 3., 4., 5., 5.5, 7., 9.]
    dy = np.gradient(y)                 # yの勾配を計算
    print(dy)
    # 結果を表示
    plt.plot(x, y, "r-o", label="y")
    plt.plot(x, dy, "g-o", label="dy")
    plt.xlim([0, 10])
    plt.ylim([0, 10])
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
