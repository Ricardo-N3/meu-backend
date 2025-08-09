animal1 = input("")
animal2 = input("")
animal3 = input("")

if animal1 == "vertebrado":
    if animal2 == "ave":
        if animal3 == "carnivoro":
            print("aguia")
        else:
            print("pomba")

    else:
        if animal3 == "onivoro":
            print("homem")
        else:
            print("vaca")

else:
    if animal2 == "inseto":
        if animal3 == "hematofago":
            print("pulga")
        else:
            print("lagarta")
    
    else:
        if animal3 == "hematofago":
            print("sanguessuga")
        else:
            print("minhoca")