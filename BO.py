class importStanMagazynu(object):

	import pandas as pd
	import numpy as np
	import os.path
	from sqlalchemy import create_engine

	hostname="localhost"
	dbname="magTermyv3"
	uname="root"
	pwd="testtest"

	engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
					.format(host=hostname, db=dbname, user=uname, pw=pwd))

	desired_width = 320

	pd.options.mode.chained_assignment = None
	pd.set_option('display.width', desired_width)
	np.set_printoptions(linewidth=desired_width)
	pd.set_option('display.max_columns',10)

	userhome = os.path.expanduser('~')
	excelfile = os.path.join(userhome, 'Desktop/magTermyv3', 'BO_GASTRO.xls')

# df = pd.read_excel(excelfile, skiprows=4, usecols=['Lp.','Nazwa','Grupa','Cena','Unnamed: 5','Ilość'])
	df = pd.read_excel(excelfile, usecols=['ID','Nazwa','Stan rzeczywisty','JM','WartoscNetto','CenaZakupu'])
	open(excelfile, "r")

# df.rename( columns={'Unnamed: 5': 'Jedn.'}, inplace=True)
	df.rename( columns={'Stan rzeczywisty': 'Ilosc'}, inplace=True)
	df.rename( columns={'JM': 'Jedn.'}, inplace=True)
# df.rename( columns={'Lp.': 'ID'}, inplace=True)

# df.rename( columns={'Lp.': 'ID'}, inplace=True)

	a = df[df.Nazwa != 'Nazwa'] # Jeśli kolumna Nazwa ma wartość Nazwa -> zmien na Nan

	a.dropna(subset = ["Nazwa"], inplace=True) #Jeśli kolumna Nazwa zawiera Nan -> wyjeboj

# a.astype({"Cena": float, "Ilość": int})  #zamiana typu danych
# 	a['Ilosc'] = a['Ilosc'].str.replace(',', '.').astype(float)

# a['Ilosc'] = a['Ilosc'].str.split(",",1).str[0]
# a['Ilosc'] = a['Ilosc'].str.replace(' ', '').astype(int)



# a['Cena'] = a['Cena'].str.replace(',', '.').astype(float)
	a['Jedn.'] = a['Jedn.'].str.replace('szt.', 'Szt')
	a['Jedn.'] = a['Jedn.'].str.replace('kg.', 'KG')
	a['Jedn.'] = a['Jedn.'].str.replace('l.', 'L')
	a['Jedn.'] = a['Jedn.'].str.replace('opak.', 'Szt')  #w tt soft jest to jako sztuka

	a.to_sql('BO', engine, index=False)
	engine.execute('ALTER TABLE BO ADD PRIMARY KEY (`ID`);')



