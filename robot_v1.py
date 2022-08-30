from math import sin, cos

import matplotlib.pyplot as plt


def position_by_v_w(start_position_fi, start_position_x, start_position_y, w_v, Tp):
    """
    Funkcja wyznaczające nowe położenie na podstawie wcześniszego położenia x, y, wylicza nową
    wartość kąta fi na odstawie wektora w_v, zawierającego jaka w danej próbce była prędkość 
    kątowa i liniowa, Tp to okres próbkowania 
    """


    fi_tmp = start_position_fi[-1] + Tp * w_v[0]
    # dodanie od razu fi do tablicy, by wkorzystać wyliczoną wartość w obliczeniach
    start_position_fi.append(fi_tmp)

    x_tmp = start_position_x[-1] + Tp * cos(start_position_fi[-1]) * w_v[1]
    y_tmp = start_position_y[-1] + Tp * sin(start_position_fi[-1]) * w_v[1]

    start_position_x.append(x_tmp)
    start_position_y.append(y_tmp)


def main():
    # punkty startowe dla robota
    #start_position_fi = [0.4]
    #start_position_x = [0.25]
    #start_position_y = [0.3]

    start_position_fi = [0]
    start_position_x = [0]
    start_position_y = [0]

    # określenie ile ms trwa symulacja
    for i in range(300):
        # okres próbkowania w jednej [s]
        Tp = 0.01

        # przeliczenie na sekundy
        # wektor wartości w i v
        # w_v = [0.5, 1]
        w_v = [cos(i*Tp), sin(i*Tp)]
        position_by_v_w(start_position_fi, start_position_x, start_position_y, w_v, Tp)


    # kreślenie wykresów
    plot_x = [x for x in range(len(start_position_fi))]

    fig, ax = plt.subplots()
    ax.plot(start_position_x, start_position_y, "g.", label="trasa")
    ax.set_xlabel("x - w globalnym układzie współrzędnych")
    ax.set_ylabel("y - w globalnym układzie współrzędnych")
    ax.set_title("trasa w=cos(t) v=sin(t)")
    ax.legend()
    plt.show()
    # trasa w=cos(t) v=sin(t)

    fig, ax = plt.subplots()
    ax.plot(plot_x, start_position_x, "g.", label="przebieg X")
    ax.set_xlabel("1/100 s")
    ax.set_ylabel("wartość X")
    ax.set_title("przebieg wartości X w czasie")
    ax.legend()
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(plot_x, start_position_y, "g.", label="przebieg Y")
    ax.set_xlabel("1/100 s")
    ax.set_ylabel("wartość Y")
    ax.set_title("przebieg wartości Y w czasie")
    ax.legend()
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(plot_x, start_position_fi, "g.", label="przebieg fi")
    ax.set_xlabel("1/100 s")
    ax.set_ylabel("wartość fi")
    ax.set_title("przebieg wartości fi w czasie")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()