from math import sin, cos

import matplotlib.pyplot as plt

def load_data(wl, wp):
    """
    Funkcja wczytuje z pliku do przekazanych list wartości prędkości kątowych w danej próbce czasu
    """

    file = open("Profile_prędkości_V2.txt", "r")
    lines_raw = file.readlines()
    file.close()

    for line in lines_raw:
        tmp = line.split(" ")
        wl.append(float(tmp[1]))
        wp.append(float(tmp[2]))


def position_by_v_w(start_position_fi, start_position_x, start_position_y, w_v, Tp, start_position_x_k_l, start_position_y_k_l, start_position_x_k_p, start_position_y_k_p):
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

    d = 0.073
    # x lokalne
    a1 = 0
    # y lokalne
    b1 = (d/2)

    x_l_tmp, y_l_tmp = calculate_P_coordinates(x_tmp, y_tmp, a1, b1, fi_tmp)

    # x lokalne
    a2 = 0
    # y lokalne
    b2 = (d/2) * (-1)

    x_p_tmp, y_p_tmp = calculate_P_coordinates(x_tmp, y_tmp, a2, b2, fi_tmp)


    start_position_x.append(x_tmp)
    start_position_y.append(y_tmp)

    start_position_x_k_l.append(x_l_tmp)
    start_position_y_k_l.append(y_l_tmp)

    start_position_x_k_p.append(x_p_tmp)
    start_position_y_k_p.append(y_p_tmp)


def w_v_by_wp_wl(wp, wl, R, d):
    """
    Funkcja wyznacza wartość prędkości kątowej oraza liniowej na podstawie
    prędkości kątowej lewgo kółka, prawego kółka, prominia kółek oraz odległości pomiędzy nimi
    """

    w_tmp = ((wp*R)/d) - ((wl*R)/d)
    v_tmp = ((wp*R)/2) + ((wl*R)/2)

    w_v = []
    w_v.append(w_tmp)
    w_v.append(v_tmp)

    return w_v


def calculate_P_coordinates(x, y, a, b, fi):
    """
    Na podstawie zadanych wartości x, y, fi środka platformy, wyznacza jakie będą współżędne
    x, y w globalnym ukłądzie punktów przesuniętych o wektor [a, b] w lokalnym układzie
    """

    x_tmp = x + (a*cos(fi) - b*sin(fi))
    y_tmp = y + (a*sin(fi) + b*cos(fi))

    return x_tmp, y_tmp


def main():
    # punkty startowe dla robota
    start_position_fi = [0.4]
    start_position_x = [0.25]
    start_position_y = [0.3]

    # koło lewe
    start_position_x_k_l = []
    start_position_y_k_l = []

    # koło prawe
    start_position_x_k_p = []
    start_position_y_k_p = []

    d = 0.073
    R = 0.021

    wl = []
    wp = []
    load_data(wl, wp)

  # x lokalne
    a1 = 0
    # y lokalne
    b1 = (d/2)

    # koło lewe
    start_position_x_k_l = []
    start_position_y_k_l = []

    # koło prawe
    start_position_x_k_p = []
    start_position_y_k_p = []

    x_l_tmp, y_l_tmp = calculate_P_coordinates(start_position_x[0], start_position_y[0], a1, b1, start_position_fi[0])

    # x lokalne
    a2 = 0
    # y lokalne
    b2 = (d/2) * (-1)

    x_p_tmp, y_p_tmp = calculate_P_coordinates(start_position_x[0], start_position_y[0], a2, b2, start_position_fi[0])

    start_position_x_k_l.append(x_l_tmp)
    start_position_y_k_l.append(y_l_tmp)

    start_position_x_k_p.append(x_p_tmp)
    start_position_y_k_p.append(y_p_tmp)


    # określenie ile ms trwa symulacja
    for i in range(12220):
        # okres próbkowania w [s]
        Tp = 0.01
        w_v = w_v_by_wp_wl(wp[i], wl[i], R, d)

        # przeliczenie na sekundy
        # wektor wartości w i v
        # w_v = [0.5, 1]
        # w_v = [cos(i*Tp), sin(i*Tp)]
        position_by_v_w(start_position_fi, start_position_x, start_position_y, w_v, Tp, start_position_x_k_l, start_position_y_k_l, start_position_x_k_p, start_position_y_k_p)


    # kreślenie wykresów
    plot_x = [x for x in range(len(start_position_fi))]

    fig, ax = plt.subplots()
    ax.plot(start_position_x, start_position_y, "g.", label="trasa środka robota")
    ax.plot(start_position_x_k_l, start_position_y_k_l, "b.", label="trasa lewego koła")
    ax.plot(start_position_x_k_p, start_position_y_k_p, "r.", label="trasa prawego koła")
    ax.set_xlabel("x - w globalnym układzie współrzędnych")
    ax.set_ylabel("y - w globalnym układzie współrzędnych")
    ax.set_title("trasa dla wartości wl i wp z pliku")
    ax.legend()
    plt.show()

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