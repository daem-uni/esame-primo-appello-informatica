from operator import itemgetter

FILE_INCENDIO = "incendio_1.txt"
FILE_RISERVA = "riserva.txt"
FILE_SERVIZIO = "servizio.txt"

def carica_pompieri(nome_file):
    pompieri = []

    with open(nome_file, 'r') as file_pompieri:
        for riga in file_pompieri:
            matricola, _, grado = riga.strip().split(";")
            pompieri.append({
                "matricola": int(matricola),
                "grado": int(grado)
            })

    return pompieri


def carica_incendio(nome_file):
    incendio_xy = []

    with open(nome_file, "r") as file_incendio:
        for riga in file_incendio:
            incendio_xy.append(riga.strip().split(" "))

    incendio = []

    for y in range(len(incendio_xy)):
        incendio.append([])
        for x in range(len(incendio_xy[y])):
            incendio[y].append(incendio_xy[x][y])

    return incendio

def categorizza_fuochi(incendio):
    fuochi = []

    for x in range(len(incendio)):
        accessi = []
        raggio = 0
        ultimo = ""

        for y in range(len(incendio[x])):
            casella = incendio[x][y]
            
            if casella == "f":
                raggio = raggio + 1
                if ultimo == '.':
                    accessi.append((x, y - 1))
            elif casella == ".":
                if ultimo == 'f':
                    accessi.append((x, y))

                    fuochi.append({
                        "punti_accesso": accessi,
                        "raggio": raggio
                    })

                    accessi = []
                    raggio = 0

            ultimo = casella
        if raggio > 0:
            fuochi.append({
                "punti_accesso": accessi,
                "raggio": raggio
            })

    return fuochi

def scegli_pompieri(fuochi, servizio, riserva):
    pompieri_assegnati = []
    servizio = sorted(servizio, key=itemgetter("grado"))
    riserva = sorted(riserva, key=itemgetter("grado"))

    for fuoco in fuochi:
        while len(fuoco['punti_accesso']) >= 1 and (len(servizio) > 0 or len(riserva) > 0) and fuoco['raggio'] > 0:
            if len(servizio) > 0:
                for i in range(len(servizio)):
                    if fuoco['raggio'] <= servizio[i]['grado']:
                        pompieri_assegnati.append({
                            "pompiere": servizio.pop(i),
                            "posizione": fuoco['punti_accesso'].pop(0)
                            })
                        fuoco['raggio'] = 0
                        break

                if fuoco['raggio'] > 0:
                    p = servizio.pop()
                    pompieri_assegnati.append({
                        "pompiere": p,
                        "posizione": fuoco['punti_accesso'].pop(0)
                        })
                    fuoco['raggio'] -= p['grado']
            else:
                for i in range(len(riserva)):
                    if fuoco['raggio'] <= riserva[i]['grado']:
                        pompieri_assegnati.append({
                            "pompiere": riserva.pop(i),
                            "posizione": fuoco['punti_accesso'].pop(0)
                            })
                        fuoco['raggio'] = 0
                        break

                if fuoco['raggio'] > 0:
                    p = riserva.pop()
                    pompieri_assegnati.append({
                        "pompiere": p,
                        "posizione": fuoco['punti_accesso'].pop(0)
                        })
                    fuoco['raggio'] -= p['grado']

    return pompieri_assegnati

def stampa_incendio(incendio):
    spento = True

    for x in range(len(incendio)):
        for y in range(len(incendio[x])):
            if incendio[y][x] == 'f':
                spento = False

            print("%3s" % (incendio[y][x]), end=" ")
        print()

    if spento:
        print("Incendio sotto controllo")
    else:
        print("Chiamare Canadair")

def main():
    servizio = carica_pompieri(FILE_SERVIZIO)
    riserva = carica_pompieri(FILE_RISERVA)
    incendio = carica_incendio(FILE_INCENDIO)

    fuochi = categorizza_fuochi(incendio)
    pompieri_assegnati = scegli_pompieri(fuochi, servizio, riserva)

    for p in pompieri_assegnati:
        x, y = p['posizione']
        incendio[x][y] = p['pompiere']['matricola']

        if len(incendio[x]) > y + 1 and incendio[x][y + 1] == 'f':
            for i in range(p['pompiere']['grado']):
                incendio[x][y + 1 + i] = "+"
        else:
            for i in range(p['pompiere']['grado']):
                incendio[x][y - 1 - i] = "+"

    stampa_incendio(incendio)

main()