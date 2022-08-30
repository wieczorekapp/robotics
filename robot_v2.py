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


def calculate_r(w_v):
    """
    Na podstawie znanej wartości kątowej i liniowej, jeśli są one stałę można wyznaczyć promień koła
    jakie zatoczy robot poruszając się z zadaną prędkością R = v/w
    """

    print(f"prędkość kątowa: {w_v[0]} prędkość liniowa:{w_v[1]}")
    if w_v[0] != 0:
        print(f"R = v/w:  R={round(w_v[1]/w_v[0],2)}")
    else:
        print(f"Robot porusza się po prostej z prędkością liniow {w_v[1]}")


def main():
    # punkty startowe dla robota
    start_position_fi = [0.4]
    start_position_x = [0.25]
    start_position_y = [0.3]

    # wyznaczenie wartości prędkości kątowej i liniowej
    w_v = w_v_by_wp_wl(1,0.5,0.025,0.145)
    calculate_r(w_v)

    # określenie ile ms trwa symulacja
    for i in range(300):
        # okres próbkowania w [s]
        Tp = 0.01

        # przeliczenie na sekundy
        # wektor wartości w i v
        # w_v = [0.5, 1]
        # w_v = [cos(i*Tp), sin(i*Tp)]
        position_by_v_w(start_position_fi, start_position_x, start_position_y, w_v, Tp)


    # kreślenie wykresów
    plot_x = [x for x in range(len(start_position_fi))]

    fig, ax = plt.subplots()
    ax.plot(start_position_x, start_position_y, "g.", label="trasa środka robota")
    ax.set_xlabel("x - w globalnym układzie współrzędnych")
    ax.set_ylabel("y - w globalnym układzie współrzędnych")
    ax.set_title("trasa wp=1 wl=0.5")
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