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
excelfile = os.path.join(userhome, 'Desktop/GastroMag/Kuchnia', 'PZ_KUCH.xls')

def dataFrameFromSQL(path):
    df = pd.read_excel(path, skiprows=4, usecols=['Lp.', 'Nazwa', 'Jedn.', 'Ilość', 'Cena','Dokument'])
    open(path, "r")
    df.rename(columns={'Ilość': 'Ilosc'}, inplace=True)
    df.dropna(subset=["Lp."], inplace=True)  # Jeśli kolumna Nazwa zawiera Nan -> wyjeboj
    a = df[df['Lp.'].astype(str).str.isdigit()]
    a['Ilosc'] = a['Ilosc'].str.replace(' ', '')
    a['Ilosc'] = a['Ilosc'].str.replace(',', '.').astype(float)
    a['Jedn.'] = a['Jedn.'].str.replace('Szt.', 'Szt')
    a['Nazwa'] = a['Nazwa'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')
    return a

i = dataFrameFromSQL(excelfile)
i.to_sql('PZKuchnia', engine, index=False)




