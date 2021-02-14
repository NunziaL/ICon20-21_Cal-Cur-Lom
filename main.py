#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
import sys
import pandas as pd
import os
import warnings
warnings.filterwarnings(action='ignore')

#moduli privati
from byesian import classificatore_bayesiano
from spotify import canzoneDaSpotify
from supervised import previsione
from cluster import suggerimenti

#Espressione regolare che apre i file della cartella con tutte le canzoni per ogni decade salvando le informazioni in un dataframe
dfs = [pd.read_csv(f'archive/dataset-of-{decade}0s.csv') for decade in ['6', '7', '8', '9', '0', '1']]

#Aggiunta della colonna decade al dataset
for i, decade in enumerate([1960, 1970, 1980, 1990, 2000, 2010]):
    dfs[i]['decade'] = pd.Series(decade, index=dfs[i].index)

data = pd.concat(dfs, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui",self)
        self.pushButton.clicked.connect(self.buttonPress)

    def buttonPress(self):
        self.textEdit.clear()
        input = self.lineEdit.text()
        if not self.radioButton.isChecked() and not self.radioButton_2.isChecked() and not self.radioButton_3.isChecked():
            self.textEdit.insertPlainText("Seleziona un'opzione.")
            return
        if input == "":
            return
        song = canzoneDaSpotify(input)
        if song is None :
            self.textEdit.insertPlainText("Prova a cercare qualcos'altro.")
            return
        elif song is -1:
            self.textEdit.insertPlainText("Prova a cercare qualcos'altro.")
            return
        self.pushButton.setEnabled(False) 
        
        #Prepara la canzone alla predizione eliminando gli attributi non necessari
        songPredic=song.drop(['track', 'artist', 'uri'], axis=1)

        #Classificazione canzone nella decade con classificatore Bayesiano
        songPredic['decade']= classificatore_bayesiano(songPredic)
        
        if self.radioButton.isChecked():
            self.textEdit.insertPlainText("La canzone è stata classificata nel seguente decennio:" + "  " + str(songPredic.iloc[0]['decade']))
        
        elif self.radioButton_2.isChecked():

            #Previsione per ogni tipo di modello
            result=previsione(data,songPredic)
            #Aggiunge valore alla colonna target in base al valore preponderante nelle predizioni
            count1 = 0
            count0 = 0
            for model in result.values():
                if model == 1:
                    count1 = count1 + 1
                else:
                    count0 = count0 + 1
            if count1 > count0:
                song['target'] = 1
                self.textEdit.insertPlainText("La canzone è una HIT!\n")
            else:
                song['target'] = 0
                self.textEdit.insertPlainText("La canzone è un FLOP.\n")
            self.textEdit.insertPlainText("Le previsioni sono:\n")
            for key in result:
                self.textEdit.insertPlainText(key + ":   " + str(result[key]) + "\n")
            
        else:
            #verifica dell'esistenza di cluster su file
            if(not os.path.exists('data/Cluster.sav')):
                self.textEdit.insertPlainText("Attenzione! E' in corso la creazione dei cluster. Ci vorrà un pò di tempo...")
            #Stampa delle canzoni simili a quella inserita dall'utente
            a = songPredic['decade']
            songPredic = songPredic.drop('decade', axis=1)
            if 'target' in song:
                songPredic['target'] = song['target']
            else:
                songPredic['target'] = 0
            songPredic['decade'] = a
            songSugg = suggerimenti(songPredic, data)
            #self.textEdit.clear()
            for i in range(0, len(songSugg)):
                counter = i+1
                if song.iloc[0]['track'] == songSugg[i]['track'] and song.iloc[0]['artist'] == songSugg[i]['artist']:
                    counter = counter - 1
                    continue
                self.textEdit.insertPlainText(str(counter) + ". " + str(songSugg[i]['track']) + " - " + str(songSugg[i]['artist'])+ "\n")
        self.pushButton.setEnabled(True)
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())