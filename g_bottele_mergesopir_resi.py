import os
import glob
from subprocess import call
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import json


class FileManager:
    def __init__(self, base_path, base_path_lanjutan):
        self.base_path = base_path
        self.referensi_file = None  # initialize the attribute here
        self.base_path_lanjutan = base_path_lanjutan
        self.referensi_file_lanjutan = None

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

        # File lanjutan
    def get_last_created_folder_lanjutan(self):
        folders_lanjutan = glob.glob(f"{self.base_path_lanjutan}/*/")
        folders_lanjutan.sort(key=os.path.getctime, reverse=True)
        self.last_created_folder_lanjutan = folders_lanjutan[0]

    def get_latest_files_lanjutan(self, count=3):
        files_lanjutan = glob.glob(f"{self.last_created_folder_lanjutan}/*")
        files_lanjutan.sort(key=os.path.getmtime, reverse=True)
        self.latest_files_lanjutan = files_lanjutan[:count]

    def set_file_lanjutan(self, file_idx):
        self.file_lanjutan = self.format_path(self.latest_files_lanjutan[file_idx])

class Pertanyaan:
    def listFileAmbilResi(self, update: Update, context: CallbackContext):
        file_manager.get_last_created_folder()
        file_manager.get_latest_files()
        query = update.callback_query
        question = 'Silakan pilih file 1 (dari folder Ambil Resi):'
        button = [
            [
            InlineKeyboardButton(
                os.path.basename(file), 
                callback_data=f'g-ambilresi_{idx}'
                )
            ]
            for idx, file in enumerate(file_manager.latest_files, start=1)
        ]
        reply_markup = InlineKeyboardMarkup(button)
        query.edit_message_text(question, reply_markup=reply_markup)

    def listFileDetailResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        question = 'Silakan pilih file 2 (dari folder Detail Resi):'
        button = [
            [
            InlineKeyboardButton(
                os.path.basename(file), 
                callback_data=f'g-detailresi_{idx}'
                )
            ]
            for idx, file in enumerate(file_manager_lanjutan.latest_files_lanjutan, start=1)
        ]
        reply_markup = InlineKeyboardMarkup(button)
        query.edit_message_text(question, reply_markup=reply_markup)

class Response:
    def listFileAmbilResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        # file_manager.get_last_created_folder()
        # file_manager.get_latest_files()
        file_idx = int(query.data.split('_')[1])-1
        file_manager.set_referensi_file(file_idx)

        with open(r'resiextractor\merge sopir\file_1_ambilresi.json', 'w') as f:
            json.dump(file_manager.referensi_file, f)

        print(f"User {update.effective_user.id} memilih file: {file_manager.referensi_file}")
        
        context.bot.send_message(chat_id=query.message.chat_id, text=f"File 1 (dari folder Waiting List): {os.path.basename(file_manager.referensi_file)}")

        file_manager_lanjutan.get_last_created_folder_lanjutan()
        file_manager_lanjutan.get_latest_files_lanjutan()
        pertanyaan.listFileAmbilResi(update, context)

    def listFileDetailResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        file_idx = int(query.data.split('_')[1])-1
        file_manager_lanjutan.set_file_lanjutan(file_idx)

        with open(r'resiextractor\merge sopir\file_2_inputresi.json', 'w') as f:
            json.dump(file_manager_lanjutan.file_lanjutan, f)

        print(f"User {update.effective_user.id} memilih file: {file_manager_lanjutan.file_lanjutan}")
        
        context.bot.send_message(chat_id=query.message.chat_id, text=f"File 2 (dari folder Resi): {os.path.basename(file_manager_lanjutan.file_lanjutan)}")

        pesan_selesai_merger = "Proses merger file 1 (folder Resi) dan file 2 (folder Detail Resi) telah selesai"

        call(["python", r"resiextractor\tambah wl\f_merge_wl.py"])

        print(pesan_selesai_merger)
        context.bot.send_message(chat_id=query.message.chat_id, text=pesan_selesai_merger)

base_path = "C:/Users/Aditya PC/Downloads/Surat Jalan/Resi"
base_path_lanjutan = "C:/Users/Aditya PC/Downloads/Surat Jalan/Detail Resi"

file_manager = FileManager(base_path, base_path_lanjutan)
file_manager_lanjutan = FileManager(base_path, base_path_lanjutan)

pertanyaan = Pertanyaan()
response = Response()

g_pertanyaan_listFileAmbilResi = pertanyaan.listFileAmbilResi
g_pertanyaan_listFileDetailResi = pertanyaan.listFileDetailResi

g_response_listFileAmbilResi = response.listFileAmbilResi
g_response_listFileDetailResi = response.listFileDetailResi
