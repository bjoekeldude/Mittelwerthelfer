import argparse
import pandas as pd

def generate_analysis_json(sonden_df):
    #zeit: Anfang und Ende
    #Wassermelder: wieviel Prozent 1
    #Fehlercode: alle unique von 0 verschiedenen falls nur null, dann none
    #Logger: Logger-ID
    #Serial: Serienummer
    #Strömung X und Y: Strömung Durchschnitt + Std-Dev
    #Temperatur: Mittelwert + Std-Dev
    #Druck: Mittelwert + Std-Dev
    #Leitfähigkeit: Mittelwert + Std-Dev
    #Kappa25: Mittelwert + Std-Dev
    #Ges. Strömung: Mittelwert + Std-Dev
    #Strömungsrichtung: Mittelwert + Std-Dev

    #Alles in ein JSON
    return 0

parser = argparse.ArgumentParser(description="Durchschnittsbestimmung Sensordatenfile")
parser.add_argument("-i", dest="filename", required=True,
                    help="input file", metavar="FILE")
args = parser.parse_args()

raw_data = pd.read_excel(args.filename, index_col=0) #hier muss die erste Zeile weggeschmissen werden
sonden_data = []
sonden_data[0] = raw_data #aber nur spalten 1-14
sonden_data[1] = raw_data #aber nur spalten 15-28
sonden_data[2] = raw_data #aber nur spalten 29-42
sonden_data[3] = raw_data #aber nur spalten 43-56

analysis_json = []
for n in range(0,3):
    analysis_json[n] = generate_analysis_json(sonden_data[n])

#print to file
