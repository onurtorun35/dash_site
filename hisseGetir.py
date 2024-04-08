# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 20:58:17 2024

@author: onur
"""
from matplotlib import pyplot as plt

import pandas as pd
import seaborn as sbn
import numpy as np


    
    

    


class finansalVeriBasliklari:  #onemli finansal verileri tutacagimiz sinif
    def __init__(self,hisseDf):
        self.donenVarliklar          = hisseDf.loc["Dönen Varlıklar"]   # hepsi indexi donemler olan series
        self.duranVarliklar          = hisseDf.loc["Duran Varlıklar"]
        self.ticariBorclar           = hisseDf.loc["Ticari Borçlar"]
        self.kisaVadeliYukumlulukler = hisseDf.loc["Kısa Vadeli Yükümlülükler"]
        self.uzunVadeliYukumlulukler = hisseDf.loc["Uzun Vadeli Yükümlülükler"]
        self.brutKar                 = hisseDf.loc["BRÜT KAR (ZARAR)"]
        self.satisGelirleri          = hisseDf.loc["Satış Gelirleri"]
        self.satislarinMaliyeti      = hisseDf.loc["Satışların Maliyeti (-)"]
        self.faaliyetGiderleri       = hisseDf.loc["Pazarlama, Satış ve Dağıtım Giderleri (-)"] + hisseDf.loc["Genel Yönetim Giderleri (-)"] + hisseDf.loc["Araştırma ve Geliştirme Giderleri (-)"]
        self.amortismanGideri        = hisseDf.loc["Amortisman & İtfa Payları"]
        self.finansmanGideri         = hisseDf.loc["Finansman Giderleri"]
        self.faaliyetKari            = hisseDf.loc["FAALİYET KARI (ZARARI)"]
        self.netDonemKari            = hisseDf.loc["Dönem Net Kar/Zararı"]
        self.ticariAlacaklar         = hisseDf.loc["Ticari Alacaklar"]
        self.Stoklar                 = hisseDf.loc["Stoklar"]
        self.ozKaynaklar             = hisseDf.loc["Özkaynaklar"]
        self.nakitveBenzerleri       = hisseDf.loc["Nakit ve Nakit Benzerleri"]
        self.bilancoDonemleri        = pd.DataFrame(self.donenVarliklar.index)
        self.finansalYatirimlar      = hisseDf.loc["Finansal Yatırımlar"]
        self.LotSayisi               = hisseDf.loc["Ödenmiş Sermaye"]
        self.FCF                     = hisseDf.loc["Serbest Nakit Akım"]

    def SatMalKarOz(self):
        satisGelirleri = pd.DataFrame(self.satisGelirleri)
        satisGelirleri.reset_index(inplace=True)
        satisGelirleri.columns = ["Dönemler","Satışlar"]
        maliyet        = pd.DataFrame(-self.satislarinMaliyeti)
        maliyet.reset_index(inplace=True)
        maliyet.columns=["Dönemler","Satışların Maliyeti"]
        netKar         = pd.DataFrame(self.netDonemKari)
        netKar.reset_index(inplace=True)
        netKar.columns = ["Donemler","Net Kar"]
        ozKaynak       = pd.DataFrame(self.ozKaynaklar)
        ozKaynak.reset_index(inplace=True)
        ozKaynak.columns = ["Dönemler","Öz Kaynaklar"]
        topluHali      = {"Satışlar" : satisGelirleri,"Satışların Maliyeti": maliyet,"Net Kar":netKar,"Öz Kaynaklar":ozKaynak}
        return topluHali

 

# NAKİT ORANLAR

    def cariOran(self):
        donenVarliklar          = pd.Series(self.donenVarliklar.values,dtype=float)
        kisaVadeliYukumlulukler = pd.Series(self.kisaVadeliYukumlulukler.values,dtype=float)
        bilancoDonemleri        = pd.DataFrame(self.donenVarliklar.index)
        cariOran                = pd.DataFrame(donenVarliklar/kisaVadeliYukumlulukler)
        cariOran                = round(cariOran,2)
        cariOran                = pd.concat([bilancoDonemleri,cariOran],axis=1)
        cariOran.columns        = ["Donemler","Cari Oran"] 
        return cariOran
        
    def asitTestOrani(self):

        Stoklar                 = pd.Series(self.Stoklar.values[0,:],dtype=float)  # bilancoda iki tane stoklar oldugu icin
        donenVarliklar          = pd.Series(self.donenVarliklar.values,dtype=float)
        kisaVadeliYukumlulukler = pd.Series(self.kisaVadeliYukumlulukler.values,dtype=float)
        bilancoDonemleri        = pd.DataFrame(self.donenVarliklar.index)
        asitTestOrani           = pd.DataFrame((donenVarliklar-Stoklar)/kisaVadeliYukumlulukler)
        asitTestOrani           = round(asitTestOrani,2)
        asitTestOrani           = pd.concat([bilancoDonemleri,asitTestOrani],axis=1)
        asitTestOrani.columns   = ["Donemler","Asit Test Oranı"] 
        return asitTestOrani
        
    def nakitOran(self):

        nakitler                = pd.Series(self.nakitveBenzerleri.values,dtype=float)
        finansalYatirimlar      =  pd.Series(self.finansalYatirimlar.values[0,:],dtype=float)
        nakitTotal              = nakitler + finansalYatirimlar
        kisaVadeliYukumlulukler = pd.Series(self.kisaVadeliYukumlulukler.values, dtype=float)
        nakitOran_              = pd.DataFrame(nakitTotal/ kisaVadeliYukumlulukler)
        nakitOran_              = round(nakitOran_,2)
        nakitOran_              = pd.concat([self.bilancoDonemleri, nakitOran_], axis=1)
        nakitOran_.columns      = ["Donemler","Nakit Oran"]
        return nakitOran_


       
 # FAALİYET ETKİNLİK ORANLARİ
    def aktifDevirHizi(self):
        satislar                     = self.satislar_Quad()
        yilliklandirilmisSatislar    = self.sumLastForValue(satislar)

        donenVarliklar = pd.DataFrame(self.donenVarliklar)
        donenVarliklar.reset_index(inplace = True)
        donenVarliklar.columns = ["Donemler","Donen"]
        donenVarliklar.set_index("Donemler",inplace = True)
        donenVarliklar         = self.ortalamaOzkaynak(donenVarliklar)
        
        duranVarliklar               = pd.DataFrame(self.duranVarliklar)
        duranVarliklar.reset_index(inplace = True)
        duranVarliklar.columns       = ["Donemler","Duran"]
        duranVarliklar.set_index("Donemler",inplace = True)
        duranVarliklar               = self.ortalamaOzkaynak(duranVarliklar)
        toplamVarliklar              = duranVarliklar["Ortalama"] + donenVarliklar["Ortalama"]
        Donemler                     = duranVarliklar["Donemler"] 

        toplamOrtalamaVarliklarDf = pd.concat([Donemler,toplamVarliklar],axis=1)
        mergedDf                  = pd.merge(yilliklandirilmisSatislar,toplamOrtalamaVarliklarDf,on="Donemler")     
            
        aktifDevirHizi            = pd.Series(np.round(mergedDf["Degerler"].values/mergedDf["Ortalama"].values,2))
        aktifDevirHiziDf          = pd.concat([mergedDf["Donemler"],aktifDevirHizi],axis=1)
        aktifDevirHiziDf.columns = ["Donemler","Aktif Devir Hızı"]
        
        return aktifDevirHiziDf

    def stokDevirHizi(self): 
        satislarinMaliyeti                               = self.satislarinMaliyeti_Quad()
        yilliklandirilmisSatislarinMaliyeti              = self.sumLastForValue(satislarinMaliyeti)
        yilliklandirilmisSatislarinMaliyeti["Degerler"]  = -1*yilliklandirilmisSatislarinMaliyeti["Degerler"] #maliyet eksi oldugu icin
 
        Stoklar               = pd.Series(self.Stoklar.values[0,:],dtype=float)
        StoklarDf= pd.concat([self.bilancoDonemleri,Stoklar],axis=1)

        StoklarDf.columns       = ["Donemler","Stoklar"]
        StoklarDf.set_index("Donemler",inplace = True)
        
        StoklarDf               = self.ortalamaOzkaynak(StoklarDf)
        StoklarDeger          = StoklarDf["Ortalama"]
        Donemler              = StoklarDf["Donemler"] 
        StoklarDf            = pd.concat([Donemler,StoklarDeger],axis=1)
        mergedDf             = pd.merge(yilliklandirilmisSatislarinMaliyeti,StoklarDf,on="Donemler")     
       
        StokDevirHizi            = pd.Series(np.round(mergedDf["Degerler"].values/mergedDf["Ortalama"].values,2))
        StokDevirHizi          = pd.concat([mergedDf["Donemler"],StokDevirHizi],axis=1)
        StokDevirHizi.columns  = ["Donemler","Stok Devir Hızı"]
        
        return StokDevirHizi

    def ozKaynakDevirHizi(self):
        ceyreklikSatislar                                = self.satislar_Quad()
        yilliklandirilmisSatislar                        = self.sumLastForValue(ceyreklikSatislar)
        ozKaynaklar                                      = pd.DataFrame(self.ozKaynaklar)
        ortalamaOzKaynaklar                              = self.ortalamaOzkaynak(ozKaynaklar)
        mergedDf                    = pd.merge(ortalamaOzKaynaklar,yilliklandirilmisSatislar,on="Donemler")
        ozKaynakDevirHizi           = pd.Series((mergedDf["Degerler"].values/mergedDf["Ortalama"].values))
        ozKaynakDevirHizi           = np.round(ozKaynakDevirHizi,2)
        ozKaynakDevirHiziDf         = pd.concat([mergedDf["Donemler"],ozKaynakDevirHizi],axis=1)
        ozKaynakDevirHiziDf.columns = ["Donemler","Öz Kaynak Devir Hızı"]
        return ozKaynakDevirHiziDf

    def alacakDevirHizi (self):
        ceyreklikSatislar                                = self.satislar_Quad()
        yilliklandirilmisSatislar                        = self.sumLastForValue(ceyreklikSatislar)
        _ticariAlacaklar                                  = pd.DataFrame(self.ticariAlacaklar.iloc[0]+ self.ticariAlacaklar.iloc[1])  # bilancoda iki tane varsa ilkini almak icin bunu kullan
        ortalamaTicariAlacaklar                          = self.ortalamaOzkaynak(_ticariAlacaklar) 
        mergedDf                    = pd.merge(ortalamaTicariAlacaklar,yilliklandirilmisSatislar,on="Donemler")
        _alacakDevirHizi            = pd.Series((mergedDf["Degerler"].values/mergedDf["Ortalama"].values))
        _alacakDevirHizi            = np.round(_alacakDevirHizi,2)
        alacakDevirHiziDf           = pd.concat([mergedDf["Donemler"],_alacakDevirHizi],axis=1)
        alacakDevirHiziDf.columns = ["Donemler","Alacak Devir Hızı"]  
        return alacakDevirHiziDf 





    def netIsletmeSermayesi(self):
        donenVarliklar              = pd.Series(self.donenVarliklar.values,dtype=float)   
        kisaVadeliYukumlulukler     = pd.Series(self.kisaVadeliYukumlulukler.values,dtype=float)
        bilancoDonemleri            = pd.DataFrame(self.donenVarliklar.index)
        netIsletmeSermayesi         = pd.DataFrame(donenVarliklar -kisaVadeliYukumlulukler)
        netIsletmeSermayesi         = pd.concat([bilancoDonemleri,netIsletmeSermayesi],axis=1)
        netIsletmeSermayesi.columns = ["Donemler","Net İşletme Sermayesi"]
        return netIsletmeSermayesi
        
    def netIStoSatislar(self):
        netIsletmeSermayesi     = pd.Series(self.netIsletmeSermayesi()["Net İşletme Sermayesi"].values,dtype=float)
        satisGelirleri          = pd.Series(self.satisGelirleri.values,dtype=float)
        netIStoSatislar         = pd.DataFrame(netIsletmeSermayesi/satisGelirleri)
        netIStoSatislar         = round(netIStoSatislar,2)
        bilancoDonemleri        = pd.DataFrame(self.satisGelirleri.index)
        netIStoSatislar         = pd.concat([bilancoDonemleri,netIStoSatislar],axis=1)
        netIStoSatislar.columns = ["Donemler","NİS/Satislar"]
        return netIStoSatislar
        
    def borclanmaKatsayisi(self):  #borcluluk orani (borc/ozkaynak)
        toplamYukumlulukler        = pd.Series(self.kisaVadeliYukumlulukler.values + self.uzunaVadeliYukumlulukler.values,dtype=float)
        borclanmaKatsayisi         = pd.DataFrame(self.ozKaynaklar/toplamYukumlulukler)
        borclanmaKatsayisi         = pd.concat([self.bilancoDonemleri,borclanmaKatsayisi],axis=1)
        borclanmaKatsayisi.columns = ["Donemler","borçlanma Katsayisi"]
        return borclanmaKatsayisi

    def PDDD(self):
        lotSayisi    = self.LotSayisi[-1]
        piyasaDegeri = self.kapanisFiyati()*lotSayisi
        ozKaynak     = self.ozKaynaklar[-1]
        PDDD         = piyasaDegeri/ozKaynak
        return round(PDDD,2)

    def firmaDegeri(self):
        finansalYatirimlar = self.finansalYatirimlar.values[0,-1] + self.finansalYatirimlar.values[1,-1]
        netBorc            = self.uzunVadeliYukumlulukler[-1] + self.kisaVadeliYukumlulukler[-1] - self.nakitveBenzerleri[-1] - finansalYatirimlar
        lotSayisi          = self.LotSayisi[-1]
        dolasimOrani       = 50.5 #float(input("Hissenin Dolasim Orani(%) : "))
        piyasaDegeri       = self.kapanisFiyati()*lotSayisi*dolasimOrani/100
        firmaDegeri        = piyasaDegeri + netBorc
        return firmaDegeri

    def FDFAVOK(self):
        firmaDegeri = self.firmaDegeri()
        favok       = self.sumLastForValue(self.FAVOK_Quad())
        favokLast   = favok["Degerler"].iloc[-1]
        FDFAVOK     = firmaDegeri/favokLast
        return round(FDFAVOK,2)

    def FKOrani(self):
        FK = self.kapanisFiyati()/self.HBK()
        return round(FK,2)

    def PEG(self):
        netKarQuad                = self.netKar_Quad()
        calculatedKar             = self.sumLastForValue(netKarQuad)
        sonYilliklandirilmisKar   = calculatedKar["Degerler"].iloc[-1]
        sonYilliklandirilmisKar_2 = calculatedKar["Degerler"].iloc[-2]
        KarDegisimi               = ((sonYilliklandirilmisKar - sonYilliklandirilmisKar_2)/sonYilliklandirilmisKar_2)*100
        PEG                       = (self.FKOrani()/KarDegisimi)
        return round(PEG,2)

    def kaynakveBorclar(self):
        Ozkaynak = self.ozKaynaklar[-1]
        KVB      = self.kisaVadeliYukumlulukler[-1]
        UVB      = self.uzunVadeliYukumlulukler[-1]
        data     = {"Basliklar":["Öz Kaynak","Kısa Vadeli Borclar","Uzun Vadeli Borçlar"],"Degerler":[Ozkaynak,KVB,UVB]}
        df       = pd.DataFrame(data)
        return df

        #DIGER

    def FAVOK_CUM(self):
        FAVOK_         = pd.Series(self.brutKar.values + self.faaliyetGiderleri.values + self.amortismanGideri.values,dtype=float)
        FAVOK_         = pd.concat([self.bilancoDonemleri, FAVOK_], axis=1)
        FAVOK_.columns = ["Donemler","FAVOK"]
        return FAVOK_

    def FAVOK_Quad(self):
        FAVOK_CUM           = self.FAVOK_CUM()
        FAVOK_CUM.set_index(FAVOK_CUM.columns[0],inplace=True)
        FAVOK_Quad_         = self.makeQuarter(FAVOK_CUM)
        FAVOK_Quad_         = pd.Series(FAVOK_Quad_["Ceyreklik"].values)
        FAVOK_Quad_         = pd.concat([self.bilancoDonemleri, FAVOK_Quad_],axis=1)
        FAVOK_Quad_.columns = ["Donemler","FAVOK (Ceyreklik)"]
        return FAVOK_Quad_

    def netKar_Quad(self):
        donemselKar          = pd.DataFrame(self.netDonemKari)
        donemselKarDf        = self.makeQuarter(donemselKar)
        _netKar_Quad         = pd.Series(donemselKarDf["Ceyreklik"].values)
        _netKar_Quad         = pd.concat([self.bilancoDonemleri, _netKar_Quad], axis=1)
        _netKar_Quad.columns = ["Donemler", "Net Kar (Ceyreklik)"]
        return _netKar_Quad

    def satislar_Quad(self):
        donemselSatislar               = pd.DataFrame(self.satisGelirleri)
        donemselSatislarDf             = self.makeQuarter(donemselSatislar)
        _Satislar_Quad                 = pd.Series(donemselSatislarDf["Ceyreklik"].values)
        _Satislar_Quad                 = pd.concat([self.bilancoDonemleri, _Satislar_Quad], axis=1)
        _Satislar_Quad.columns = ["Donemler", "Satislar (Ceyreklik)"]
        return _Satislar_Quad       

    def satislarinMaliyeti_Quad(self):
        donemselSatislarinMaliyeti            = pd.DataFrame(self.satislarinMaliyeti)
        donemselSatislarDf                    = self.makeQuarter(donemselSatislarinMaliyeti)
        _SatislarinMaliyeti_Quad              = pd.Series(donemselSatislarDf["Ceyreklik"].values)
        _SatislarinMaliyeti_Quad              = pd.concat([self.bilancoDonemleri, _SatislarinMaliyeti_Quad], axis=1)
        _SatislarinMaliyeti_Quad.columns = ["Donemler", "Satislarin Maliyeti (Ceyreklik)"]
        return _SatislarinMaliyeti_Quad  


    def kapanisFiyati(self):
        fiyatDf      = pd.read_excel("database/THYAO_fiyat.xlsx")
        fiyatGecmisi = fiyatDf["CLOSING_TL"]
        sonFiyat     = fiyatGecmisi.iloc[-1]
        return sonFiyat


        #FREE CASH FLOW 

    def FreeCashFlow(self):
        FCF              = pd.Series(self.FCF.values,dtype=float)
        bilancoDonemleri = pd.DataFrame(self.FCF.index)
        FCFDf           = pd.concat([bilancoDonemleri,FCF],axis=1)
        FCFDf.columns = ["Donemler","FCF"] 
        return FCFDf

    def FreeCashFlow_Quad(self):
        FCF_QuadDf                   = self.makeQuarter(pd.DataFrame(self.FCF))
        FCF_QuadDf.reset_index(inplace=True)
        FCF_QuadDf.columns         = ["Donemler","FCF (Ceyreklik)"] 
        return FCF_QuadDf

    def FCF_Yilliklanidirlmis(self):  # BİR HATA VAR BULAMADIM
        FCF_Quad   = self.FreeCashFlow_Quad()
        FCF_Yillik = self.sumLastForValue(FCF_Quad)
        return FCF_Yillik
        
  

        #FONSIYONLAR

    def sumLastForValue(self,df):

        df       = df.iloc[::-1].reset_index(drop=True)
        Values   = df[[df.columns[1]]].values   # ikinci sutunda bulunan degerleri alıyor
        donemler = df[df.columns[0]]     # series
        length   = len(donemler)
        i = 0
        calculatedDict = {}
        while i < length - 3:
            fourValue = Values[i]  + Values[i+1] + Values[i+2] + Values[i+3]
            donem = donemler[i]
            calculatedDict[donem] = fourValue
            i+=1

        calculatedDict = pd.DataFrame(calculatedDict).transpose()
        calculatedDict.reset_index(inplace=True)
        calculatedDict.columns=["Donemler","Degerler"]
        calculatedDict = calculatedDict.iloc[::-1].reset_index(drop=True)
        return calculatedDict

    def FinansalOranlar(self):
        print(f"F/K : {self.FKOrani()}\nPD/DD : {self.PDDD()}\nFD/FAVOK : {self.FDFAVOK()}\nHBK : {self.HBK()}\nPEG : {self.PEG()}")

    def ortalamaOzkaynak(self,df):   #ortalama hesaplar(bir sonraki yılla)
        ortalama        = []
        donemlerListesi = []
        df = df[::-1]  # reversing dataframe
        try:
            for i in df.index:
                donem = i.split("/")[1]
                sene = i.split("/")[0]
                firstValue = df.loc[i][0]
                j = str(int(sene)-1)
                index = j+"/"+donem
                secondValue = df.loc[index][0]
                meanValue = (firstValue + secondValue)*0.5
                ortalama.append(meanValue)
                donemlerListesi.append(i)
        except (KeyError,ValueError):
            pass

        ortalamDf         = pd.DataFrame([ortalama])
        ortalamDf.columns = donemlerListesi
        ortalamDf         = ortalamDf.transpose()
        ortalamDf.reset_index(inplace=True)
        ortalamDf.columns = ["Donemler","Ortalama"]
        ortalamDf         = ortalamDf[::-1].reset_index(drop=True)
        return  ortalamDf

    def makeQuarter(self,cumulativeDf):  # bu fonksiyona gelecek DF index kesinlikle Donemler olarak gelmelidir

        ceyreklik = {}
        for i in cumulativeDf.index:
            donem = i.split("/")[1]
            if donem =="3":
                sonUcluk_1 = cumulativeDf.loc[i][0]
                ceyreklik.update({f"{i}":sonUcluk_1})  
                
            if donem=="6":
                sonUcluk_2 = cumulativeDf.loc[i][0]- sonUcluk_1
                ceyreklik.update({f"{i}":sonUcluk_2})
                
            if donem =="9":
                sonUcluk_3 = cumulativeDf.loc[i][0]- sonUcluk_2 - sonUcluk_1
                ceyreklik.update({f"{i}":sonUcluk_3})
                
            if donem == "12":
                sonUcluk_4 = cumulativeDf.loc[i][0]- sonUcluk_1 - sonUcluk_2 - sonUcluk_3
                ceyreklik.update({f"{i}":sonUcluk_4})

        ceyreklikDf = pd.DataFrame([ceyreklik],index=[0]).transpose()
        ceyreklikDf.columns = ["Ceyreklik"]
        return ceyreklikDf   # cikti formatinin okunmasi ile ilgili bilgi FAVOK_Quad fonksiyonunda var


        #KARLILIK

    def aktifKarlilik(self):
        donenVarliklar = pd.DataFrame(self.donenVarliklar)
        duranVarlıklar = pd.DataFrame(self.duranVarliklar)

        donenVarliklar.reset_index(inplace = True)
        donenVarliklar.columns = ["Donemler","Donen"]
        donenVarliklar.set_index("Donemler",inplace = True)
        donenVarliklar         = self.ortalamaOzkaynak(donenVarliklar)

        duranVarlıklar.reset_index(inplace = True)
        duranVarlıklar.columns = ["Donemler","Duran"]
        duranVarlıklar.set_index("Donemler",inplace = True)
        duranVarliklar         = self.ortalamaOzkaynak(duranVarlıklar)

        netKarQuad    = self.netKar_Quad()
        calculatedKar = self.sumLastForValue(netKarQuad)

        toplamOrtalamaVarliklar = duranVarliklar["Ortalama"] + donenVarliklar["Ortalama"]
        Donemler                = duranVarliklar["Donemler"]

        toplamOrtalamaVarliklarDf = pd.concat([Donemler,toplamOrtalamaVarliklar],axis=1)
        mergedDf                  = pd.merge(calculatedKar,toplamOrtalamaVarliklarDf,on="Donemler")

        artifKarlilik           = pd.Series((mergedDf["Degerler"].values/mergedDf["Ortalama"].values)*100)
        artifKarlilikDf         = pd.concat([mergedDf["Donemler"],artifKarlilik],axis=1)
        artifKarlilikDf.columns = ["Donemler","Aktif Karlılık"]

        return artifKarlilikDf

    def ozSermayeKarliligi(self):
        netKarQuad    = self.netKar_Quad()
        calculatedKar = self.sumLastForValue(netKarQuad)


        ozSermaye         = pd.DataFrame(self.ozKaynaklar)
        ozSermaye.reset_index(inplace = True)
        ozSermaye.columns = ["Donemler","Oz Sermaye"]
        ozSermaye.set_index("Donemler",inplace = True)
        _ortalamaOzkaynak = self.ortalamaOzkaynak(ozSermaye)

        mergedDf                     = pd.merge(calculatedKar,_ortalamaOzkaynak,on="Donemler")   # this is a good method
        ozSermayeKarliligi           = pd.Series((mergedDf["Degerler"].values/mergedDf["Ortalama"].values)*100)
        ozSermayeKarliligi           = round(ozSermayeKarliligi,2)
        ozSermayeKarliligiDf         = pd.concat([mergedDf["Donemler"],ozSermayeKarliligi],axis=1)
        ozSermayeKarliligiDf.columns = ["Donemler","Öz Sermaye Karlılığı"]

        return ozSermayeKarliligiDf

    def brutKarMarji(self):
        brutKar          = pd.Series(self.brutKar.values,dtype=float)
        satislar         = pd.Series(self.satisGelirleri.values,dtype=float)
        bilancoDonemleri = pd.DataFrame(self.brutKar.index)
        brutKarMarji     = pd.DataFrame((brutKar/satislar)*100)
        brutKarMarji     = round(brutKarMarji,2)
        brutKarMarjiDf   = pd.concat([bilancoDonemleri,brutKarMarji],axis=1)
        brutKarMarjiDf.columns = ["Donemler","Brüt Kar Marji"] 
        return brutKarMarjiDf

    def brutKarMarji_Quad(self):
        brutKarQuad        = self.makeQuarter(pd.DataFrame(self.brutKar))       # excelden cektiklerini dataframe e cevirip makeQuad a gonder
        satisGelirleriQuad = self.makeQuarter(pd.DataFrame(self.satisGelirleri))
        _brutKarMarji_Quad = ((brutKarQuad/satisGelirleriQuad)*100)
        _brutKarMarji_Quad = round(_brutKarMarji_Quad,2)
        _brutKarMarji_Quad.reset_index(inplace=True)
        _brutKarMarji_Quad.columns = ["Donemler","Brüt Kar Marji (Ceyreklik)"]
        return _brutKarMarji_Quad

    def netKarMarji_Quad(self):
        netKarQuad         = self.makeQuarter(pd.DataFrame(self.netDonemKari))       # excelden cektiklerini dataframe e cevirip makeQuad a gonder
        satisGelirleriQuad = self.makeQuarter(pd.DataFrame(self.satisGelirleri))
        netKarQuad         = ((netKarQuad/satisGelirleriQuad)*100)
        netKarQuad         = round(netKarQuad,2)
        netKarQuad.reset_index(inplace=True)
        netKarQuad.columns = ["Donemler","Net Kar Marjı (Ceyreklik)"]
        return netKarQuad

    def HBK(self):
        netKarQuad              = self.netKar_Quad()
        calculatedKar           = self.sumLastForValue(netKarQuad)
        sonYilliklandirilmisKar = calculatedKar["Degerler"].iloc[-1]
        lotSayisi               = self.LotSayisi[-1]
        HBK                     = sonYilliklandirilmisKar / lotSayisi
        return round(HBK,2)

    def FAVOKMarji_Quad(self):
        FAVOKQuad          = self.FAVOK_Quad()
        satisGelirleriQuad = self.makeQuarter(pd.DataFrame(self.satisGelirleri))
        satisGelirleriQuad.reset_index(inplace=True)
        FAVOKMarjiQuad     = (FAVOKQuad["FAVOK (Ceyreklik)"]/satisGelirleriQuad["Ceyreklik"])*100
        FAVOKMarjiQuad     = round(FAVOKMarjiQuad,2)
        FAVOKMarji_QuadDf  = pd.concat([self.bilancoDonemleri, FAVOKMarjiQuad], axis=1)
        FAVOKMarji_QuadDf.columns = ["Donemler","FAVÖK Marjı (Ceyreklik)"]
        return FAVOKMarji_QuadDf





