# Bot ini mengajukan pertanyaan kepada user tentang tujuan barang/tujuan kendaraan yang digunakan untuk menentukan prefix filename. Jawaban disimpan di #* resiextractor\visualisasi 2\tujuan_kendaraan.json

# Pertanyaan selanjutnya adalah file mana yang akan divisualisasikan (dari Folder Detail Resi, nama file 'Truk_Detail_Resi', jadi visualisasi dilakukan setelah merge sopir dan resi). Jawaban disimpan di #* resiextractor\visualisasi 2\sumber_data_visualisasi.json

# Bot ini juga berfungsi mengirimkan visualisasi per truk kepada user bot. Sumber visualisasi tersebut dari #* resiextractor\visualisasi 2\sumber_data_visualisasi.json

import os
import glob
from subprocess import call
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import json


class FileManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.referensi_file = None  # initialize the attribute here

    def get_last_created_folder(self):
        folders = glob.glob(f"{self.base_path}/*/")
        folders.sort(key=os.path.getctime, reverse=True)
        self.last_created_folder = folders[0]

    def get_latest_files(self, count=3):
        files = glob.glob(f"{self.last_created_folder}/*")
        files.sort(key=os.path.getmtime, reverse=True)
        self.latest_files = files[:count]

    @staticmethod
    def format_path(path):
        return path.replace('/', '\\')
    
    def set_referensi_file(self, file_idx):
        self.referensi_file = self.format_path(self.latest_files[file_idx])


class Pertanyaan:
    def tujuanKendaraan(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        question = 'Pilih tujuan barang/kendaraan 📥:'
        button = [
            InlineKeyboardButton('Lokalan', callback_data='h_tujuan_lokalan'),
            InlineKeyboardButton('Pool Lain', callback_data='h_tujuan_pool_lain')
        ]
        reply_markup = InlineKeyboardMarkup([button])
        query.edit_message_text(question, reply_markup=reply_markup)
        # query.message.reply_text(question, reply_markup=reply_markup)

    # def sumberData(self, update: Update, context: CallbackContext) -> None:
    #     query = update.callback_query
    #     button = [
    #         InlineKeyboardButton('Mulai dari awal 0️⃣', callback_data='a_sumber_mulai_awal'),
    #         InlineKeyboardButton('Pilih referensi file 🔁', callback_data='a_sumber_ref_file')
    #     ]
    #     reply_markup = InlineKeyboardMarkup([button])
    #     query.edit_message_text('Pilih sumber data:', reply_markup=reply_markup)
    #     # query.message.reply_text('Pilih sumber data:', reply_markup=reply_markup)

    def listFileDetailResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        button = [
            [
            InlineKeyboardButton(
                os.path.basename(file), 
                callback_data=f'h-file_{idx}'
                )
            ]
            for idx, file in enumerate(file_manager.latest_files, start=1)
        ]
        reply_markup = InlineKeyboardMarkup(button)
        query.edit_message_text('Silakan pilih file sumber data visualisasi (dari Folder Detail Resi):', reply_markup=reply_markup)

class Response:
    def tujuanKendaraan(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        choice_tujuanKendaraan = "Lokalan" if query.data == "h_tujuan_lokalan" else "Pool Lain"

        print(f'User {update.effective_user.id} memilih asal kendaraan: {choice_tujuanKendaraan}')

        with open('resiextractor\visualisasi 2\tujuan_kendaraan.json', 'w') as f:
            json.dump(query.data, f)
        
        # query.edit_message_text(f"Pilihan asal barang: {choice_tujuanKendaraan}") # -> gunakan ini jika ingin menampilkan pilihan user berupa MERUBAH CHAT SEBELUMNYA

        context.bot.send_message(chat_id=query.message.chat_id, text=f"Pilihan asal barang: {choice_tujuanKendaraan}")# -> gunakan ini jika ingin menampilkan pilihan user berupa CHAT TAMBAHAN

        file_manager.get_last_created_folder()
        file_manager.get_latest_files()
        pertanyaan.listFileDetailResi(update, context)

    def listFileDetailResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        a_idx = int(query.data.split('_')[1])-1
        if a_idx < len(file_manager.latest_files):
            file_manager.set_referensi_file(a_idx)
            with open(r'resiextractor\visualisasi 2\sumber_data_visualisasi.json', 'w') as f:
                json.dump(file_manager.referensi_file, f)

            print(f"User {update.effective_user.id} memilih file: {file_manager.referensi_file}")
            context.bot.send_message(chat_id=query.message.chat_id, text=f"File sumber data visualisasi (dari Folder Detail Resi): {os.path.basename(file_manager.referensi_file)}")
        else:
            context.bot.send_message(chat_id=query.message.chat_id, text="Indeks file tidak valid. Silakan coba lagi.")

        pesan_mulai_visualisasi = "Visualisasi data omzet per truk dimulai"
        pesan_selesai_visualisasi = "Visualisasi data omzet per truk selesai"
        print(pesan_mulai_visualisasi)
        context.bot.send_message(chat_id=query.message.chat_id, text=pesan_mulai_visualisasi)

        call(["python", "resiextractor\visualisasi 2\h_vis_pertruk.py"])

        print(pesan_selesai_visualisasi)
        context.bot.send_message(chat_id=query.message.chat_id, text=pesan_selesai_visualisasi)
        # ! Pengiriman visualisasi ke user bot diinisasi dengan command di bawah
        visualisasi.sendVisualisasi(update,context)


class Visualisasi:
    def sendVisualisasi(self, update: Update, context:CallbackContext):
        with open (r'resiextractor\visualisasi 2\saved_visualisasi.json', 'r') as f:
            img_visualisasi = json.load(f)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img_visualisasi, 'rb'))

base_path = "C:/Users/Aditya PC/Downloads/Surat Jalan/Detail Resi"
file_manager = FileManager(base_path)
pertanyaan = Pertanyaan()
response = Response()
visualisasi = Visualisasi()

h_pertanyaan_tujuanKendaraan = pertanyaan.tujuanKendaraan
h_pertanyaan_listFileDetailResi = pertanyaan.listFileDetailResi

h_response_tujuanKendaraan = response.tujuanKendaraan
h_response_listFileDetailResi = response.listFileDetailResi
