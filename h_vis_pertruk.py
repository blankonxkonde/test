# Digunakan untuk mevisualisasikan omzet per mobil

# Sumber data visualisasi (sumber_data_visualisai.json) ada 2, jika pertama kali maka sumber adalah dari detail resi (folder Detail Resi)

# Namun jika visualisasi dari sisa omzet, maka sumber_data_visualisasi.json berasal dari kalkulasi omzet (folder Kalkukasi Omzet)

import matplotlib.pyplot as plt
import pandas as pd
import locale
from datetime import datetime
import time
import os
import json

class FileManager:
    def __init__(self):
        self.download_directory = 'C:\\Users\\Aditya PC\\Downloads\\Surat Jalan'

        # Buat folder baru untuk setiap hari
        self.date_now = datetime.now().strftime('%d-%m-%Y')
        self.new_folder_path = os.path.join(self.download_directory, "Chart Per Truk", self.date_now)
        os.makedirs(self.new_folder_path, exist_ok=True)

        self.prefix_filename = ""
        self.filename = ""

        # List tujuan barang
        self.list_lokalan = ['YGY','BTL','PWJ','KBM','CLP', 'PWT','PBG','BNR','WSB','BMA','BNR','WSB','CRB','BRB','TGL','PML','PKL','BTG']
        self.list_pool_lain = ['LGD','POMDN','KND','CPY','BDG','TKL','POBGR','POTGR','POCKR','POLPG']

        with open (r"resiextractor\visualisasi 2\tujuan_kendaraan.json", "r") as f:
            self.user_choice_grup = json.load(f)

        with open (r"resiextractor\visualisasi 2\sumber_data_visualisasi.json", "r") as f:
            self.user_choice_data = json.load(f)

        self.data = pd.read_csv(self.user_choice_data)
        # data = pd.read_csv("C:\\Users\\Aditya PC\\Downloads\\Surat Jalan\\Detail Resi\\28-07-2023\\L_Detail_Resi_2023-07-28_17-24-31.csv")

    def buatFile(self):
        with open(r"resiextractor\visualisasi 2\tujuan_kendaraan.json", 'r') as f:
            user_choice = json.load(f)
        # Update filename prefix based on user's choice
        if user_choice == 'e_tujuan_lokalan':
            self.prefix_filename = "L_"
        elif user_choice == 'e_tujuan_pool_lain':
            self.prefix_filename = "P_"
        else:
            print("Invalid choice."), 
            return
        
        file_manager.filename = os.path.join(file_manager.new_folder_path, f"{self.prefix_filename}Visualisasi_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")

class Visualisasi:
    def visualisasi(self):
        self.e = 0
        nopol_unique = file_manager.data['Nopol'].unique()
        for nopol in nopol_unique:
            sopir = file_manager.data['Sopir'].iloc[0+self.e]
            subset = file_manager.data[file_manager.data['Nopol'] == nopol]

            data_gabung = {}
            for i, row in subset.iterrows():
                tujuan = row['Pool Tujuan']
                berat = row['Berat']
                ongkir = row['Ongkir']
                if tujuan not in data_gabung:
                    data_gabung[tujuan] = (berat, ongkir)
                else:
                    data_gabung[tujuan] = (data_gabung[tujuan][0] + berat, data_gabung[tujuan][1] + ongkir)

            sorted_data = sorted(data_gabung.items(), key=lambda x: x[0], reverse=True)
            tujuan_sorted = [item[0] for item in sorted_data]
            berat_sorted = [item[1][0] for item in sorted_data]

            plt.barh(tujuan_sorted, berat_sorted)

            locale.setlocale(locale.LC_ALL, '')
            for i, v in enumerate(sorted_data):
                ongkir_str = locale.format_string("%d", v[1][1], grouping=True)
                ongkir_str = ongkir_str.replace(",", ".")
                berat_str = locale.format_string("%.1f", v[1][0], grouping=True)
                if berat_str.endswith(".0"):
                    berat_str = berat_str[:-2]
                berat_str = berat_str.replace(",", ".")
                plt.text(v[1][0]+1, i, f"Rp{ongkir_str} ({berat_str} Kg)", ha='left', va='center', fontsize=8)

            plt.xlabel('Berat')
            plt.ylabel('Tujuan')

            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)

            plt.title(f'Chart Omzet {nopol} ({sopir})')

            visualisasi.saveVisualisasi()
            self.e += 1
    def saveVisualisasi(self):
        # Save the plot into a .png file with the current date and time in its name
        plt.savefig(file_manager.filename, dpi=300, bbox_inches='tight')
        print(f"File berhasil disimpan di {file_manager.filename}")
        # plt.show()
        with open (r'resiextractor\visualisasi 2\saved_visualisasi.json', 'w') as f:
            json.dump(file_manager.filename, f)

def main():
    global file_manager
    file_manager = FileManager()
    global visualisasi
    visualisasi = Visualisasi()
    file_manager.buatFile()
    visualisasi.visualisasi()

if __name__ == '__main__':
    main()
