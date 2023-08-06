while True:
    def dodawanie():
        d1 = float(input("Podaj pierwsza liczbe: "))
        d2 = float(input("Podaj druga liczbe: "))
        suma = d1 + d2
        print("Twoj wynik to: ", suma)


    def odejmowanie():
        o1 = float(input("Podaj pierwsza liczbe: "))
        o2 = float(input("Podaj druga liczbe: "))
        roznica = o1 - o2
        print("Twoj wynik to: ", roznica)


    def mnozenie():
        mm = str(input("Przez ile liczb chcesz mnozyc? [2] lub [3]: "))
        if mm == ("2"):
            m1 = float(input("Podaj pierwsza liczbe: "))
            m2 = float(input("Podaj druga liczbe: " ))
            iloczyn = m1 * m2
            print("Twoj wynik to: ", iloczyn)
        if mm == ("3"):
            m1 = float(input("Podaj pierwsza liczbe: "))
            m2 = float(input("Podaj druga liczbe: "))
            m3 = float(input("Podaj trzecia liczbe: "))
            iloczyn = m1 * m2 * m3
            print("Twoj wynik to: ", iloczyn)


    def dzielenie():
        dz1 = float(input("Podaj pierwsza liczbe: "))
        dz2 = float(input("Podaj druga liczbe: "))
        iloraz = dz1 / dz2
        print("Twoj wynik to: ", iloraz)


    x = input("Dodawanie, odejmowanie, mnozenie czy dzielenie? ")
    if x == ("dodawanie"):
        dodawanie()
    if x == ("odejmowanie"):
        odejmowanie()
    if x == ("mnozenie"):
        mnozenie()
    if x == ("dzielenie"):
        dzielenie()

    decyzja = input("Czy chcesz kontynuować? tak/nie ")
    if decyzja == "nie":
        print("Dziękujemy za obliczenia")
        break