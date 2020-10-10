import sys
import pandas as pd
from datetime import date
f1= "/home/h.mahmoudi/LOGICIMMONEUF/LOGICIMMONEUF/spiders/logicimmoneuf_2020_07_10.csv"
f2= date.today().strftime("LOGICIMMONEUF_%Y_%m_%d.csv") #fichier sortie entrer comme parametre

x=pd.read_csv(f1,sep=';',keep_default_na=False)



def fn_replace_0(i):
    res=str(i).replace(".0","")
    return res

def fn_categorie(i):
    res=i
    if i=="":
        res="Autres"
    else:
        pass 
    return res 

def get_number(chaine):
    mon_number=""
    for i in chaine:
        if i.isdigit():
            mon_number+=i
        else:
            pass
    return mon_number

def get_minsite_id(chaine):
    try:
        res=chaine.split("-")[-1]
    except:
        res=""
    return res

def corrction_cp(chaine):
    
    return str(chaine).zfill(5)



list_m2_total=x['M2_TOTALE'].tolist()

new_m2_total=[get_number(m2) for m2 in list_m2_total]
x['M2_TOTALE']=new_m2_total
#---------------------------

list_prix=x['PRIX'].tolist()

new_prix=[get_number(prix) for prix in list_prix]
x['PRIX']=new_prix
#---------------------- 


list_STOCK_NEUF=x['STOCK_NEUF'].tolist()

new_STOCK_NEUF=[fn_replace_0(STOCK_NEUF) for STOCK_NEUF in list_STOCK_NEUF]
x['STOCK_NEUF']=new_STOCK_NEUF


#-------------------------
list_photo=x['PHOTO'].tolist()
new_photo=[fn_replace_0(photo) for photo in list_photo]
x['PHOTO']=new_photo

#---------------------- 

list_catgorie=x['CATEGORIE'].tolist()
new_categorie=[fn_categorie(categorie) for categorie in list_catgorie]
x['CATEGORIE']=new_categorie
#----------------------------------
liste_misite_url=x['MINI_SITE_URL'].tolist()
#minisite_id=x[''].tolist()
new_minisite_id=[get_minsite_id(minisite_url) for minisite_url in liste_misite_url]
x['MINI_SITE_ID']=new_minisite_id
#---------------------

#---------------------- 

list_cp=x['CP'].tolist()
new_cp=[corrction_cp(cp) for cp in list_cp]
x['CP']=new_cp
#----------------------------------

x.to_csv(f2,sep = ';',doublequote=True,quotechar='"',quoting=1,index=False)

