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
    def menuWL(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        question = 'Menu Waiting List:'
        button = [
            InlineKeyboardButton('Ambil Waiting List', callback_data='f_ambil_waiting_list'),
            InlineKeyboardButton('Merge Waiting List', callback_data='f_merge_waiting_list')
        ]
        reply_markup = InlineKeyboardMarkup([button])
        query.edit_message_text(question, reply_markup=reply_markup) # kenapa beda dengan update.message.reply_text di method asalKendaraan?
        # update.callback_query.message.reply_text('Pilih sumber data:', reply_markup=reply_markup) # kenapa beda dengan update.message.reply_text di method asalKendaraan?

    def listFileWL(self, update: Update, context: CallbackContext):
        query = update.callback_query
        question = 'Silakan pilih file 1 (dari folder Waiting List):'
        button = [
            [
            InlineKeyboardButton(
                os.path.basename(file), 
                callback_data=f'f-ambilwl_{idx}'
                )
            ]
            for idx, file in enumerate(file_manager.latest_files, start=1)
        ]
        reply_markup = InlineKeyboardMarkup(button)
        query.edit_message_text(question, reply_markup=reply_markup)

    def listFileAmbilResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        question = 'Silakan pilih file 2 (dari folder Resi):'
        button = [
            [
            InlineKeyboardButton(
                os.path.basename(file), 
                callback_data=f'f-ambilresi_{idx}'
                )
            ]
            for idx, file in enumerate(file_manager_lanjutan.latest_files_lanjutan, start=1)
        ]
        reply_markup = InlineKeyboardMarkup(button)
        query.edit_message_text(question, reply_markup=reply_markup)

class Response:
    def menuWL(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        choice_menuWL = "Ambil Waiting List" if query.data == 'f_ambil_waiting_list' else "Merge Waiting List"

        print(f'User {update.effective_user.id} memilih sumber data: {choice_menuWL} ')

        query.edit_message_text(f'Pilihan menu: {choice_menuWL}') 

        if query.data == 'f_ambil_waiting_list':
            call(["python", r"resiextractor\tambah wl\f_ambil_wl.py"])
        if query.data == 'f_merge_waiting_list':
            file_manager.get_last_created_folder()
            file_manager.get_latest_files()
            pertanyaan.listFileWL(update, context)

    def listFileWL(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        file_idx = int(query.data.split('_')[1])-1
        file_manager.set_referensi_file(file_idx)

        with open(r'resiextractor\tambah wl\file_1_ambilwl.json', 'w') as f:
            json.dump(file_manager.referensi_file)
        print(f"User {update.effective_user.id} memilih file: {file_manager.referensi_file}")
        
        context.bot.send_message(chat_id=query.message.chat_id, text=f"File 1 (dari folder Waiting List): {os.path.basename(file_manager.referensi_file)}")

        file_manager_lanjutan.get_last_created_folder_lanjutan()
        file_manager_lanjutan.get_latest_files_lanjutan()
        pertanyaan.listFileAmbilResi(update, context)

    def listFileAmbilResi(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        file_idx = int(query.data.split('_')[1])-1
        file_manager_lanjutan.set_file_lanjutan(file_idx)

        with open(r'resiextractor\tambah wl\file_2_ambilresi.json', 'w') as f:
            json.dump(file_manager_lanjutan.file_lanjutan, f)

        print(f"User {update.effective_user.id} memilih file: {file_manager_lanjutan.file_lanjutan}")
        
        context.bot.send_message(chat_id=query.message.chat_id, text=f"File 2 (dari folder Resi): {os.path.basename(file_manager_lanjutan.file_lanjutan)}")

        pesan_selesai_merger = "Proses merger file 1 (folder Waiting List) dan file 2 (folder Resi) telah selesai"

        call(["python", r"resiextractor\tambah wl\f_merge_wl.py"])

        print(pesan_selesai_merger)
        context.bot.send_message(chat_id=query.message.chat_id, text=pesan_selesai_merger)

base_path = "C:/Users/Aditya PC/Downloads/Surat Jalan/Waiting List"
base_path_lanjutan = "C:/Users/Aditya PC/Downloads/Surat Jalan/Resi"

file_manager = FileManager(base_path, base_path_lanjutan)
file_manager_lanjutan = FileManager(base_path, base_path_lanjutan)

pertanyaan = Pertanyaan()
response = Response()

f_pertanyaan_menuWL = pertanyaan.menuWL
f_pertanyaan_listFileWL = pertanyaan.listFileWL
f_pertanyaan_listFileAmbilResi = pertanyaan.listFileAmbilResi

f_response_menuWL = response.menuWL
f_response_listFileWL = response.listFileWL
f_response_listFileAmbilResi = response.listFileAmbilResi
