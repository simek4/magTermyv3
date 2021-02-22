from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, update, insert, text
from sqlalchemy.sql import or_
import time
import multiprocessing

hostname = "localhost"
dbname = "magTermyv3"
uname = "root"
pwd = "testtest"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=hostname, db=dbname, user=uname, pw=pwd))
metadata = MetaData(engine)

PZBar = Table('PZBar', metadata,
              Column('Lp.', Integer),
              Column('Nazwa', String),
              Column('Jedn.', String),
              Column('Ilosc', Float),
              Column('Cena', Float)
              )

PZKuchnia = Table('PZKuchnia', metadata,
                  Column('Lp.', Integer),
                  Column('Nazwa', String),
                  Column('Jedn.', String),
                  Column('Ilosc', Float),
                  Column('Cena', Float)
                  )

PZSklepReg = Table('PZSklepReg', metadata,
                   Column('Lp.', Integer),
                   Column('Nazwa', String),
                   Column('Jedn.', String),
                   Column('Ilosc', Float),
                   Column('Cena', Float)
                   )

BO = Table('BO', metadata,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jedn.', String),
           Column('WartoscNetto',Float),
           Column('CenaZakupu',Float)

           )

StanMagazynu = Table('StanMagazynu', metadata,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jedn.', String),
           Column('WartoscNetto',Float),
           Column('CenaZakupu',Float)

           )

RWBar = Table('RWBar', metadata,
              Column('Lp.', Integer),
              Column('Nazwa', String),
              Column('Ilosc', Float),
              Column('Jedn.', String)
              )

RWKuchnia = Table('RWKuchnia', metadata,
                  Column('Lp.', Integer),
                  Column('Nazwa', String),
                  Column('Ilosc', Float),
                  Column('Jedn.', String)
                  )

RA = Table('RA', metadata,
           Column('Nazwa asortymentu', String),
           Column('Ilosc', Float),
           Column('Netto',Float)
           )

ZWSklepReg = Table('ZWSR', metadata,
                   Column('Lp.', Integer),
                   Column('Nazwa', String),
                   Column('Ilosc', Float),
                   Column('Jedn.', String)
                   )

ZDKuchnia = Table('ZDKuchnia', metadata,
                  Column('Lp.', Integer),
                  Column('Nazwa', String),
                  Column('Ilosc', Float),
                  Column('Jedn.', String)
                  )

ZDBar = Table('ZDBar', metadata,
              Column('Lp.', Integer),
              Column('Nazwa', String),
              Column('Ilosc', Float),
              Column('Jedn.', String)
              )

metadata.create_all(engine)
connection = engine.connect()


def progressValue(x, y):
    progress = (x / y) * 100
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(round(progress, 4), ' %')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')


def selectFrom(table):
    s = select([table])
    result = connection.execute(s)
    a = list(result)
    return a


def updateBO(name, totalQuantity):
    update_statement = BO.update() \
        .where(BO.c.Nazwa == name) \
        .values(Ilosc=BO.c.Ilosc - totalQuantity,
                WartoscNetto=BO.c.Ilosc * BO.c.CenaZakupu)
    connection.execute(update_statement)


def getAssortmentFromID(a):
    i = text(
        "SELECT * "
        "FROM asortyment "
        "WHERE idasortymentu LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def getAssortmentByName(a):
    i = text(
        "SELECT * "
        "FROM asortyment "
        "WHERE Nazwa LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def getSetByID(a):
    i = text(
        "SELECT * "
        "FROM komplety "
        "WHERE idkompletu LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def getStockByName(a):
    i = text(
        "SELECT * "
        "FROM BO "
        "WHERE Nazwa LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


starttime = time.time()

pzBar = selectFrom(PZBar)
pzKuchnia = selectFrom(PZKuchnia)
pzSklepReg = selectFrom(PZSklepReg)
sm = selectFrom(BO)

rwBar = selectFrom(RWBar)
rwKuchnia = selectFrom(RWKuchnia)
ra = selectFrom(RA)
zdKuchnia = selectFrom(ZDKuchnia)
zdBar = selectFrom(ZDBar)
zwSR = selectFrom(ZWSklepReg)


#
# ##PZ
for a in pzBar:

    if a[4] == 0: #PZ z pozycją 0zł traktuję jako RW

        ifExist = False
        sm = selectFrom(BO)

        for b in sm:
            if a[1] == b[1]:
                ifExist = True

                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc - a[3],
                            WartoscNetto=BO.c.WartoscNetto - (a[3]*BO.c.CenaZakupu)
                            )

                connection.execute(update_statement)

        if ifExist == False:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje
            sm = selectFrom(BO)

            i = insert(BO)
            i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                          'Jedn.': a[2], 'WartoscNetto': a[3] * a[4], 'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
            connection.execute(i)

    else:

        ifExist = False
        sm = selectFrom(BO)

        for b in sm:
            if a[1] == b[1]:
                ifExist = True


                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc + a[3], #Dodanie ilości na magazyn z PZ
                            WartoscNetto=BO.c.WartoscNetto + (a[3]*a[4]), #Zwiększenie wartości magazynu
                            CenaZakupu=((b[2]*b[5]) + (a[3]*a[4]))/(b[2]+a[3])
                            )

                connection.execute(update_statement)

        if ifExist == False:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje

            sm = selectFrom(BO)
            i = insert(BO)
            i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                          'Jedn.': a[2], 'WartoscNetto': a[3]*a[4], 'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
            connection.execute(i)

sm = selectFrom(BO)

for a in pzKuchnia:
    if a[4] == 0:

        ifExist = False
        sm = selectFrom(BO)

        for b in sm:
            if a[1] == b[1]:
                ifExist = True

                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc - a[3],
                            WartoscNetto=BO.c.WartoscNetto - (a[3] * BO.c.CenaZakupu)
                            )  # traktuje pozycje jako rw   czy minus robi pluss

                connection.execute(update_statement)

        if ifExist == False:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje

            sm = selectFrom(BO)

            i = insert(BO)
            i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                          'Jedn.': a[2], 'WartoscNetto': a[3] * a[4],
                          'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
            connection.execute(i)

    else:

        ifExist = False
        sm = selectFrom(BO)

        for b in sm:
            if a[1] == b[1]:
                ifExist = True

                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc + a[3],  # Dodanie ilości na magazyn z PZ
                            WartoscNetto=BO.c.WartoscNetto + (a[3] * a[4]),  # Zwiększenie wartości magazynu
                            CenaZakupu=((b[2] * b[5]) + (a[3] * a[4])) / (b[2] + a[3])
                            )

                connection.execute(update_statement)

        if ifExist == False:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje

            sm = selectFrom(BO)
            i = insert(BO)
            i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                          'Jedn.': a[2], 'WartoscNetto': a[3] * a[4],
                          'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
            connection.execute(i)

sm = selectFrom(BO)
#
for a in pzSklepReg:

    if a[4] == 0:

        ifExist = False
        sm = selectFrom(BO)

        for b in sm:
            if a[1] == b[1]:
                ifExist = True

                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc - a[3],
                            WartoscNetto=BO.c.WartoscNetto - (a[3] * BO.c.CenaZakupu)
                            )  # traktuje pozycje jako rw   czy minus robi pluss

                connection.execute(update_statement)

        if ifExist == False:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje

            sm = selectFrom(BO)

            i = insert(BO)
            i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                          'Jedn.': a[2], 'WartoscNetto': a[3] * a[4],
                          'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
            connection.execute(i)

    else:

        ifExist = False
        sm = selectFrom(BO)

        for b in sm:
            if a[1] == b[1]:
                ifExist = True

                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc + a[3],  # Dodanie ilości na magazyn z PZ
                            WartoscNetto=BO.c.WartoscNetto + (a[3] * a[4]),  # Zwiększenie wartości magazynu
                            CenaZakupu=((b[2] * b[5]) + (a[3] * a[4])) / (b[2] + a[3])
                            )

                connection.execute(update_statement)

        if ifExist == False:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje

            sm = selectFrom(BO)

            i = insert(BO)
            i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                          'Jedn.': a[2], 'WartoscNetto': a[3] * a[4],
                          'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
            connection.execute(i)

sm = selectFrom(BO)


##RW
for a in rwBar:

    ifExist = False
    sm = selectFrom(BO)

    for b in sm:

        if a[1] == b[1]:
            ifExist = True

            update_statement = BO.update() \
                .where(BO.c.ID == b[0]) \
                .values(Ilosc=BO.c.Ilosc + a[2],
                        WartoscNetto=BO.c.WartoscNetto + (a[2]*b[5]))  # rw do stanu

            connection.execute(update_statement)

    if ifExist == False:
        print("Brak pozycji ", a, " z dokumentu RW na stanie magazynu")

sm = selectFrom(BO)

for a in rwKuchnia:

    ifExist = False
    sm = selectFrom(BO)

    for b in sm:

        if a[1] == b[1]:
            ifExist = True

            update_statement = BO.update() \
                .where(BO.c.ID == b[0]) \
                .values(Ilosc=BO.c.Ilosc + a[2],
                        WartoscNetto=BO.c.WartoscNetto + (a[2] * b[5]))  # rw do stanu

            connection.execute(update_statement)

    if ifExist == False:
        print("Brak pozycji ", a, " z dokumentu RW na stanie magazynu")

sm = selectFrom(BO)

##ZW
for a in zwSR:

    ifExist = False

    sm = selectFrom(BO)

    for b in sm:

        if a[1] == b[1]:
            ifExist = True

            update_statement = BO.update() \
                .where(BO.c.ID == b[0]) \
                .values(Ilosc=BO.c.Ilosc - a[2],
                        WartoscNetto=BO.c.WartoscNetto - (a[2] * BO.c.CenaZakupu)
                        )  # traktuje pozycje jako rw   czy minus robi pluss

            connection.execute(update_statement)

    if ifExist == False:
        print(a)
        print('Asortyment z dokumentu ZWSR nie istnieje')

sm = selectFrom(BO)

##ZD
for a in zdKuchnia:
    ifExist = False
    sm = selectFrom(BO)

    for b in sm:

        if a[1] == b[1]:
            ifExist = True

            update_statement = BO.update() \
                .where(BO.c.ID == b[0]) \
                .values(Ilosc=BO.c.Ilosc + a[2],
                        WartoscNetto=BO.c.WartoscNetto + (a[2] * b[5]))

            connection.execute(update_statement)

    if ifExist == False:
        print(a)
        print('Asortyment z dokumentu ZDKuchnia nie istnieje')

sm = selectFrom(BO)

for a in zdBar:
    ifExist = False
    sm = selectFrom(BO)

    for b in sm:

        if a[1] == b[1]:
            ifExist = True

            update_statement = BO.update() \
                .where(BO.c.ID == b[0]) \
                .values(Ilosc=BO.c.Ilosc + a[2],
                        WartoscNetto=BO.c.WartoscNetto + (a[2] * b[5]))

            connection.execute(update_statement)

    if ifExist == False:
        print(a)
        print('Asortyment z dokumentu ZDBar nie istnieje')

sm = selectFrom(BO)

count = 0
allRA = len(ra)

##RA
for a in ra:

    count += 1
    progressValue(count, allRA)
    print("Pozycja na paragonie ", a[0], " sprzedany ", a[1], "x za cenę: ",a[2]," zł")

    assortmentID = [b[0] for b in getAssortmentByName(a[0])]
    quantitySet = [b[4] for b in getAssortmentByName(a[0])]

    if not assortmentID:
        print("Asortyment nie do ściągnięcia ", a[0])

    else:
        set = [a for a in getSetByID(assortmentID[0])]

        for f in set:

            assortmentIDFromSet = [q[0] for q in getAssortmentFromID(f[1])]
            assortmentNameFromSet = [q[1] for q in getAssortmentFromID(f[1])]
            assortmentQuantityFromSet = [q[4] for q in getAssortmentFromID(f[1])]

            total = (f[0] / quantitySet[0]) * a[1]

            surowiec = [e[1] for e in getStockByName(assortmentNameFromSet[0])]

            if not surowiec:  # Brak surowca do ściągnięcia z magazynu (receptura w recepturze)

                setInSet = [a for a in getSetByID(assortmentIDFromSet[0])]

                for l in setInSet:
                    assortmentIDFromSetInSet = [a[0] for a in getAssortmentFromID(l[1])]
                    assortmentNameFromSetInSet = [a[1] for a in getAssortmentFromID(l[1])]
                    total = (((l[0] / assortmentQuantityFromSet[0]) * f[0]) / quantitySet[0]) * a[1]
                    print("Sciagam ", assortmentNameFromSetInSet[0], " w ilości ", total)
                    updateBO(assortmentNameFromSetInSet[0], total)

            else:  # Surowiec do ściągnięcia z magazynu
                print("Sciągam ", assortmentNameFromSet[0], " w ilości ", total)
                updateBO(assortmentNameFromSet[0], total)



print('Ukończono w {} sekund'.format(time.time() - starttime))


