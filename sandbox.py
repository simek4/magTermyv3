from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, update, insert, text
from sqlalchemy.sql import or_
import time
import multiprocessing

hostname="localhost"
dbname="magTermyv3"
uname="root"
pwd="testtest"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))
metadata = MetaData(engine)

PZ = Table('PZ', metadata,
        Column('Lp.', Integer, primary_key=True),
        Column('Nazwa', String),
        Column('Jedn.', String),
        Column('Ilosc', Float),
        Column('Cena', String)
)

BO = Table('BO', metadata,
        Column('ID', Integer, primary_key=True),
        Column('Nazwa', String),
        Column('Ilosc', Float),
        Column('Jedn.', String)
)

RW = Table('RW', metadata,
        Column('Lp.', Integer),
        Column('Nazwa', String),
        Column('Ilosc', Float),
        Column('Jedn.', String)
)

RA = Table('RA', metadata,
        Column('Nazwa asortymentu', String),
        Column('Ilosc', Float),
)

komplety = Table('komplety', metadata,
        Column('Ilosc', Float),
        Column('idasortymentu', Float),
        Column('idkompletu', Float),
)

asortyment = Table('asortyment', metadata,
        Column('idasortymentu', Float),
        Column('Nazwa', String),
        Column('iloscZkompletu', Float),
)

metadata.create_all(engine)
connection = engine.connect()

desired_width = 320
def progressValue(x,y):
    progress = (x/y) * 100
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(round(progress,4), ' %')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')

starttime = time.time()

def selectFrom(table):
    s = select([table])
    result = connection.execute(s)
    a = list(result)
    return a
def updateBO(name,totalQuantity):
    update_statement = BO.update() \
        .where(BO.c.Nazwa == name) \
        .values(Ilosc=BO.c.Ilosc - totalQuantity)
    connection.execute(update_statement)

def getAssortmentFromID(a):
    i = text(
        "SELECT * "
        "FROM asortyment "
        "WHERE idasortymentu LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result

pz = selectFrom(PZ)
sm = selectFrom(BO)
rw = selectFrom(RW)
ra = selectFrom(RA)
# komplet = selectFrom(komplety)
# asort = selectFrom(asortyment)
# const = selectFrom(asortyment)
# const2 = selectFrom(asortyment)
#
# komplet2 = selectFrom(komplety)





# ##Dodanie na magazyn
# for a in pz:
#     print(a)
#
#     if a[4]==0:
#
#         # print(a)
#         # print('Pozycja na PZ 0zł traktuję jako RW')
#
#         ifExist = False
#         sm = selectFrom(BO)
#
#         for b in sm:
#             if a[1]==b[1]:
#
#                 ifExist = True
#
#                 update_statement = BO.update() \
#                     .where(BO.c.ID==b[0] ) \
#                     .values(Ilosc=BO.c.Ilosc - a[3]) #traktuje pozycje jako rw   czy minus robi pluss
#
#                 connection.execute(update_statement)
#
#         if ifExist == False: # jeśli nie istnieje asortyment na magazynie to dodaje pozycje
#
#             stanGast = selectFrom(BO)
#
#             i = insert(BO)
#             i = i.values({'ID': len(sm)+1, 'Nazwa': a[1], 'Ilosc': a[3], 'Jedn.': a[2]}) #dodanie z pz asortymentu którego nie było na magazynie ID + 1
#             connection.execute(i)
#
#     else:
#
#         ifExist = False
#         sm = selectFrom(BO)
#
#         for b in sm:
#             if a[1]==b[1]:
#
#                 ifExist = True
#
#                 update_statement = BO.update() \
#                     .where(BO.c.ID==b[0] ) \
#                     .values(Ilosc=BO.c.Ilosc + a[3]) #dodanie ilosci z pz do stanu
#
#                 connection.execute(update_statement)
#
#         if ifExist == False: # jeśli nie istnieje asortyment na magazynie to dodaje pozycje
#
#             sm = selectFrom(BO)
#
#             i = insert(BO)
#             i = i.values({'ID': len(sm)+1, 'Nazwa': a[1], 'Ilosc': a[3], 'Jedn.': a[2]}) #dodanie z pz asortymentu którego nie było na magazynie ID + 1
#             connection.execute(i)
#
# sm = selectFrom(BO)


# for a in rw:
#
#     ifExist = False
#     sm = selectFrom(BO)
#
#     for b in sm:
#
#         if a[1]==b[1]:
#
#             ifExist = True
#
#             update_statement = BO.update() \
#                 .where(BO.c.ID==b[0] ) \
#                 .values(Ilosc=BO.c.Ilosc + a[2]) #rw do stanu
#
#             connection.execute(update_statement)
#
#     if ifExist == False:
#         print(a)
#         # print('BRAK POZYCJI NA MAGAZYNIE Z DOKUMENT RW KUCHNIA')
#
#         # s = select([StanGastro])
#         # result = connection.execute(s)
#         # stanGast = list(result)  # pobranie nowego stanu magazynu po dodaniu asortymentu w celu nadania poprawnego id
#         # i = insert(StanGastro)
#         # i = i.values({'ID': len(stanGast) + 1, 'Nazwa': a[1], 'Ilosc': a[3], 'Jedn.': a[2]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
#         # connection.execute(i)
#
# sm = selectFrom(BO)
#
# count=0
# allRA = len(ra)
#
#
#
#




for a in ra:
    print("")
    print("Pozycja na paragonie ",a[0]," sprzedany ",a[1],"x")

    s = text(
        "SELECT * "
        "FROM asortyment "
        "WHERE Nazwa LIKE :x"
    )

    result = connection.execute(s, {"x":a[0]}).fetchall() #pozycja z asortymentu wyciągnięta z pozycji na paragonie
    idasortymentu = [r[0] for r in result]
    iloscZkompletu = [r[4] for r in result]

    s = text(
        "SELECT * "
        "FROM komplety "
        "WHERE idkompletu LIKE :y"
    )
    result = connection.execute(s, {"y":idasortymentu[0]}).fetchall()
    kompot = [p for p in result]

    for f in kompot:
        # print("ID asortymentu z kompletu ",f[1]," w ilości ",f[0])
        # u = text(
        #     "SELECT * "
        #     "FROM asortyment "
        #     "WHERE idasortymentu LIKE :z"
        # )
        #
        # def getAssortmentFromID(a):
        #     i = text(
        #         "SELECT * "
        #         "FROM asortyment "
        #         "WHERE idasortymentu LIKE :y"
        #     )
        #     result = connection.execute(i, {"y":a}).fetchall()
        #     return result
        #
        # wynik = connection.execute(u, {"z":f[1]}).fetchall()
        wynik = getAssortmentFromID(f[1])
        assortmentID = [q[0] for q in wynik]
        assortmentName = [q[1] for q in wynik]
        assortmentQuantity = [q[4] for q in wynik]
        total = (f[0]/iloscZkompletu[0])*a[1]
        # print(total)
        qq = text(
            "SELECT * "
            "FROM BO "
            "WHERE Nazwa LIKE :w"
        )
        wynik3 = connection.execute(qq, {"w":assortmentName[0]}).fetchall()
        pozycjaZmagazynu = [e[1] for e in wynik3]

        if not pozycjaZmagazynu: #Brak asortymentu do ściągnięcia w magazynie (receptura w recepturze)

            n = text(
                "SELECT * "
                "FROM komplety "
                "WHERE idkompletu LIKE :p"
            )
            chojco = connection.execute(n, {"p":assortmentID[0]}).fetchall()
            chojcoByleCo = [v for v in chojco]

            for l in chojcoByleCo:
                print("ID asortymentu z kompletu ", l[1], " w ilości ", l[0])
                # u = text(
                #     "SELECT * "
                #     "FROM asortyment "
                #     "WHERE idasortymentu LIKE :z"
                # )
                # wynik5 = connection.execute(u, {"z": l[1]}).fetchall()
                wynik5 = getAssortmentFromID(l[1])
                assortmentID = [q[0] for q in wynik5]
                assortmentName1 = [q[1] for q in wynik5]
                print(assortmentID[0])
                print(assortmentName1[0])

                total = (((l[0]/assortmentQuantity[0])*f[0])/iloscZkompletu[0])*a[1]
                print(total)
                updateBO(assortmentName1[0],total)


        else: #Asortyment do ściągnięcia w magazynie
            updateBO(assortmentName[0],total)




# ifExist = False
#
# ##RA
# for a in ra:
#     count += 1
#     progressValue(count,allRA)
#
#     for b in asort:
#
#         if a[0] == b[1]: #Nazwa asortymentu z paragonu ma się zgodzić z nazwą z tabeli asortymentu
#
#             for c in komplet:
#
#                 if b[0] == c[2]: #ID asortymentu z ID kompletu
#
#                     for e in const:
#
#                         if c[1] == e[0]: #Składniki z asortymentu są w stanie magazynu
#
#                             total = c[0]/b[2] #Ilość składnika podzielona przez ilość z kompletu
#                             total = total*a[1] #Pomnożona przez ilośc sprzedanych pozycji z paragonu
#
#                             for f in sm:
#
#                                 if e[1] == f[1]: #Sciągniecie towaru z stanu magazynowego
#                                     update_statement = BO.update() \
#                                         .where(BO.c.ID == f[0]) \
#                                         .values(Ilosc=BO.c.Ilosc - total)
#
#                                     connection.execute(update_statement)
#                                     # print('Paragon nr: ', count , file=open('output.txt', 'a'))
#                                     # print('Sprzedane ', a[0], ' ', a[1], 'x', file=open('output.txt', 'a'))
#                                     # print('Sciagam z magazynu ', e[1], ' w ilości ', total, file=open('output.txt', 'a'))
#                                     ifExist = True
#                                     print('Paragon nr: ', count)
#                                     print('Sprzedane ', a[0], ' ', a[1], 'x')
#                                     print('Sciagam z magazynu ', e[1], ' w ilości ', total)
#                                     sm = selectFrom(BO)
#                                     break;
#
#                                 else:
#                                     if ifExist == True:
#
#                                         for g in komplet2: #Sciągnięcie towaru który jest recepturą w recepturze
#
#                                             if e[0] == g[2]:
#                                                 print('Sciągam recepture z receptury tj. ', e[1])
#                                                 for h in const2:
#                                                     if g[1] == h[0]:
#
#                                                         total = ((g[0]/e[2])*c[0])/b[2] #Ilość składnika w recepturze podzielona przez ilość kompletu w recepturze pomnożone przez ilość użytej receptury w recepturze podzielone przez ilość kompletu pierwszej receptury
#
#                                                         for f in sm:
#
#                                                             if h[1] == f[1]:  # Towar
#                                                                 update_statement = BO.update() \
#                                                                     .where(BO.c.ID == f[0]) \
#                                                                     .values(Ilosc=BO.c.Ilosc - total)  #
#
#                                                                 connection.execute(update_statement)
#
#                                                                 ifExist = False
#                                                                 print('Paragon nr: ', count)
#                                                                 print('Sprzedane ', a[0], ' ', a[1], 'x')
#                                                                 print('Sciagam z magazynu ', h[1], ' w ilości ', total)
#                                                                 sm = selectFrom(BO)
#                                                                 break;
#
#
#
#
#




                                                # for h in const2:
                                                #     if g[1] == h[0]:
                                                        # print(h)
                                                        # print('Ilość receptury w recepturze ',e[0]) # użyta ilość receptury np 2 budynie JEST OK
                                                        #
                                                        # print('Nazwa składników z receptury do ściągnięcia ',h[1])
                                                        #
                                                        # print('Ilość składnika w recepturze ', )
                                                        #
                                                        # print(h)
                                                        # print(h[2])

                                                        # wynik = g[0] / h[2]
                                                        # wynik = wynik * a[1]
                                                        #
                                                        # for z in sm:
                                                        #
                                                        #     if h[1] == z[1]:
                                                        #         update_statement = BO.update() \
                                                        #             .where(BO.c.ID == z[0]) \
                                                        #             .values(Ilosc=BO.c.Ilosc - wynik)  #
                                                        #
                                                        #         connection.execute(update_statement)
                                                        #         # print('Paragon nr: ', count , file=open('output.txt', 'a'))
                                                        #         # print('Sprzedane ', a[0], ' ', a[1], 'x', file=open('output.txt', 'a'))
                                                        #         # print('Sciagam z magazynu ', e[1], ' w ilości ', total, file=open('output.txt', 'a'))
                                                        #         print('Paragon nr: ', count)
                                                        #         print('Sprzedane ', a[0], ' ', a[1], 'x')
                                                        #         print('Sciagam z magazynu ', h[1], ' w ilości ', wynik)
                                                        #         sm = selectFrom(BO)






                            # for z in const2:
                            #     if c[1] == z[0]:
                            #         print(z)





                            # for g in komplet2:
                            #
                            #     if c[1] == g[2]:
                            #         print('Sciągam recepture z receptury tj. ', c[1])
                            #
                            #
                            #         for h in const2:
                            #             if g[1] == h[0]:
                            #                 print(h)
                            #                 print('Ilość receptury w recepturze ',c[0]) # użyta ilość receptury np 2 budynie JEST OK
                            #
                            #                 print('Nazwa składników z receptury do ściągnięcia ',h[1])
                            #
                            #                 print('Ilość składnika w recepturze ', )
                            #
                            #                 print('telo receptury np budyn 6szt')
                            #                 print(h)
                            #                 print(h[2])
                            #
                            #                 wynik = g[0] / h[2]
                            #                 wynik = wynik * a[1]
                            #
                            #                 for z in sm:
                            #
                            #                     if h[1] == z[1]:
                            #                         update_statement = BO.update() \
                            #                             .where(BO.c.ID == z[0]) \
                            #                             .values(Ilosc=BO.c.Ilosc - wynik)  #
                            #
                            #                         connection.execute(update_statement)
                            #                         # print('Paragon nr: ', count , file=open('output.txt', 'a'))
                            #                         # print('Sprzedane ', a[0], ' ', a[1], 'x', file=open('output.txt', 'a'))
                            #                         # print('Sciagam z magazynu ', e[1], ' w ilości ', total, file=open('output.txt', 'a'))
                            #                         print('Paragon nr: ', count)
                            #                         print('Sprzedane ', a[0], ' ', a[1], 'x')
                            #                         print('Sciagam z magazynu ', h[1], ' w ilości ', wynik)
                            #                         sm = selectFrom(BO)



















#
# for x in ra:
#     count = 0
#
#     for y in asort:
#         if a[0] == b[1]:
#             count+=1

#
# ifExist = False
#
# for a in ra:
#
#     for b in asort:
#
#         if a[0] == b[1]:
#
#                 # ifExist = True
#
#                 s = select([komplety]).where(komplety.c.idkompletu == b[0])
#                 result = connection.execute(s)
#                 idasort = list(result)
#                 #
#                 for id in idasort:
#
#                     print(id[1])
#                     s = select([asortyment]).where(asortyment.c.idasortymentu == id[1])
#                     result = connection.execute(s)
#                     towar = list(result)
#                     print(towar)
#
#


sm = selectFrom(BO)
#
# for a in ra:
#     s = select([asortyment.r.Nazwa == a[0]])
#     result = connection.execute(s)
#     b = list(result)
#
#     print(b)
# #
#
# for a in ra:
#
#         for b in receptura:
#
#                 if a[0] == b[0]:
#
#                         i = a[1]*b[1]
#
#                         for c in sm:
#
#                                 if b[2] == c[1]:
#
#                                   update_statement = BO.update() \
#                                            .where(BO.c.ID==c[0] ) \
#                                            .values(Ilosc=BO.c.Ilosc - i) #dodanie ilosci z pz do stanu
#
#                                   connection.execute(update_statement)
#                                   sm = selectFrom(BO)
#
#                                 else:
#                                         print("cos nie tak")
#
#
#
print('Ukończono w {} sekund'.format(time.time() - starttime))


