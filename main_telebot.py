# kode callback query data 'a_' atau 'a-' adalah untuk file bot tele a_bottele_ambilresi

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from a_bottele_ambilresi import a_pertanyaan_asalKendaraan, a_response_asalKendaraan, a_response_sumberData, a_response_listFileReferensi
from b_bottele_inputresi import b_pertanyaan_asalKendaraan, b_response_listFileReferensi, b_response_asalKendaraan, b_response_sumberData, b_response_listFileLanjutan
from c_bottele_skeluar import c_pertanyaan_tujuanKendaraan, c_response_tujuanKendaraan, c_response_sumberData, c_response_listFileReferensi
from d_bottele_kalomzet import d_pertanyaan_tujuanKendaraan, d_pertanyaan_listFileReferensi, d_pertanyaan_listFileLanjutan, d_response_tujuanKendaraan, d_response_listFileLanjutan, d_response_listFileReferensi
from e_bottele_visualisasi import e_pertanyaan_tujuanKendaraan, e_response_tujuanKendaraan, e_response_sumberData, e_response_listFileDetailResi, e_response_listFileKalkulasiOmzet
from f_bottele_ambilwl import f_pertanyaan_menuWL, f_response_listFileAmbilResi, f_response_menuWL, f_response_listFileWL
from g_bottele_mergesopir_resi import g_pertanyaan_listFileAmbilResi, g_pertanyaan_listFileDetailResi, g_response_listFileDetailResi,g_response_listFileAmbilResi

class Pertanyaan:
    def menu(self, update: Update, context: CallbackContext):
        question = 'Pilih menu gan! 🧑‍💻:'
        button = [
            [
                InlineKeyboardButton('Ekstrak Resi 🗳️', callback_data='menu_ekstrak_resi'),
                InlineKeyboardButton('Detailer Resi 🔎', callback_data='menu_detailer_resi')
            ],
            [
                InlineKeyboardButton('Tambahkan WL ⏳', callback_data='menu_tambahkan_wl'),
                InlineKeyboardButton('Ekstrak SKeluar 📤', callback_data='menu_ekstrak_skeluar')
            ],
            [
                InlineKeyboardButton('Kalkulasi Omzet 🔢', callback_data='menu_kalomzet'),
                InlineKeyboardButton('Visualisasi Data 📊', callback_data='menu_visualisasi')
            ],
            [
                InlineKeyboardButton('Merge Sopir-Detail Resi', callback_data='menu_mergesopir')
            ]
        ]

        reply_markup = InlineKeyboardMarkup(button)
        update.message.reply_text(question, reply_markup=reply_markup)

class Response:
    def response_menu(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        if query.data == 'menu_ekstrak_resi':
            choice_menu = 'Ekstrak Resi 🗳️'
        elif query.data == 'menu_detailer_resi':
            choice_menu = 'Detailer Resi 🔎'
        elif query.data == 'menu_tambahkan_wl':
            choice_menu = 'Tambahkan Waiting List ⏳'
        elif query.data == 'menu_ekstrak_skeluar':
            choice_menu = 'Ekstrak Surat Keluar 📤'
        elif query.data == 'menu_kalomzet':
            choice_menu = 'Kalkulasi Omzet 🔢'
        elif query.data == 'menu_visualisasi':
            choice_menu = 'Visualisasi Data 📊'
        elif query.data == 'menu_mergesopir':
            choice_menu = 'Merge Sopir-Detail Resi'
        # query.edit_message_text(text=f"Menu: {query.data} dipilih")
        context.bot.send_message(chat_id=query.message.chat_id, text=f'Menu dipilih: {choice_menu}')

        if query.data == 'menu_ekstrak_resi':
            a_pertanyaan_asalKendaraan(update, context)
        elif query.data == 'menu_detailer_resi':
            b_pertanyaan_asalKendaraan(update, context)
        elif query.data == 'menu_tambahkan_wl':
            f_pertanyaan_menuWL(update, context)
        elif query.data == 'menu_ekstrak_skeluar':
            c_pertanyaan_tujuanKendaraan(update, context)
        elif query.data == 'menu_kalomzet':
            d_pertanyaan_tujuanKendaraan(update, context)
        elif query.data == 'menu_visualisasi':
            e_pertanyaan_tujuanKendaraan(update,context)
        elif query.data == 'menu_mergesopir':
            g_pertanyaan_listFileAmbilResi(update,context)

    def response_ekstrakResi(self, update: Update, context: CallbackContext):
        if update.callback_query.data in ['a_asal_lokalan', 'a_asal_pool_lain']:
            a_response_asalKendaraan(update, context)
        elif update.callback_query.data in ['a_sumber_mulai_awal','a_sumber_ref_file']:
            a_response_sumberData(update, context)
        elif update.callback_query.data.startswith('a-file_'):
            if update.callback_query.data == 'a-file_':
                context.bot.send_message(chat_id=update.effective_chat.id, text="Silakan pilih file:")
            else:
                a_response_listFileReferensi(update, context)

    def response_inputResi(self, update: Update, context: CallbackContext): # Detailer Resi
        if update.callback_query.data in ['b_asal_lokalan', 'b_asal_pool_lain']:
            b_response_asalKendaraan(update, context)
        elif update.callback_query.data in ['b_sumber_mulai_awal','b_sumber_ref_file']:
            b_response_sumberData(update, context)
        elif update.callback_query.data.startswith('b-file_'):
            if update.callback_query.data == 'b-file_':
                context.bot.send_message(chat_id=update.effective_chat.id, text="Silakan pilih file:")
            else:
                b_response_listFileReferensi(update, context)
        elif update.callback_query.data.startswith('b-lanjutan_'):
            if update.callback_query.data == 'b-lanjutan_':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file yang akan dilanjutkan:')
            else:
                b_response_listFileLanjutan(update, context)

    def response_skeluar(self, update: Update, context:CallbackContext):
        if update.callback_query.data in ['c_tujuan_lokalan','c_tujuan_pool_lain']:
            c_response_tujuanKendaraan(update, context)
        elif update.callback_query.data in ['c_sumber_mulai_awal','c_sumber_ref_file']:
            c_response_sumberData(update, context)
        elif update.callback_query.data.startswith('c-file_'):
            if update.callback_query.data == 'c-file_':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file:')
            else:
                c_response_listFileReferensi(update,context)

    def response_kalomzet(self, update: Update, context:CallbackContext):
        if update.callback_query.data in ['d_tujuan_lokalan', 'd_tujuan_pool_lain']:
            d_response_tujuanKendaraan(update, context)
        elif update.callback_query.data.startswith ('d-file_'):
            if update.callback_query.data == 'd-file_':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file sumber (file detail resi):')
            else:
                d_response_listFileReferensi(update, context)
        elif update.callback_query.data.startswith ('d-lanjutan_'):
            if update.callback_query.data == 'd-lanjutan_':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file pengurang (file surat keluar):')
            else:
                d_response_listFileLanjutan(update, context)

    def response_visualisasi(self, update: Update, context:CallbackContext):
        if update.callback_query.data in ['e_tujuan_lokalan', 'e_tujuan_pool_lain']:
            e_response_tujuanKendaraan(update, context)
        if update.callback_query.data in ['e_visualisasi_pertama', 'e_visualisasi_pengurangan']:
            e_response_sumberData(update, context)
        elif update.callback_query.data.startswith('e-detailresi_'):
            if update.callback_query.data == 'e-detailresi_':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file sumber data di Folder Detail Resi:')
            else:
                e_response_listFileDetailResi(update, context)
        elif update.callback_query.data.startswith('e-lanjutan'):
            if update.callback_query.data == 'e-lanjutan':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file sumber data di Folder Kalkulasi Omzte')
            else:
                e_response_listFileKalkulasiOmzet(update, context)

    def response_ambilWL(self, update: Update, context:CallbackContext):
        if update.callback_query.data in ['f_ambil_waiting_list','f_merge_waiting_list']:
            f_response_menuWL(update, context)
        elif update.callback_query.data.startswith('f-ambilwl'):
            if update.callback_query.data == 'f-ambilwl':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file 1 (dari Folder Waiting List):')
            else:
                f_response_listFileWL(update, context)
        elif update.callback_query.data.startswith('f-ambilresi'):
            if update.callback_query.data == 'f-ambilresi':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file 2 (dari Folder Resi)')
            else:
                f_response_listFileAmbilResi(update, context)

    def response_mergesopir(self, update: Update, context:CallbackContext):
        if update.callback_query.data.startswith('g-ambilresi'):
            if update.callback_query.data == 'g-ambilresi':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih file 1 (dari folder Resi)')
            else:
                g_response_listFileAmbilResi(update,context)
        elif update.callback_query.data.startswith('g-detailresi_'):
            if update.callback_query.data == 'g-detailresi':
                context.bot.send_message(chat_id=update.effective_chat.id,text='Silakan pilih file 2 (dari folder Detail Resi)')
            else:
                g_response_listFileDetailResi(update,context)


    # def response_visualisasi(self, update: Update, context: CallbackContext):
    #     e_visualisasi_send(update, context)

def main():
    pertanyaan = Pertanyaan()
    response = Response()

    updater = Updater("6329646403:AAHKItvXUHuDGXP3MbjKE6b4r7y-6Ty7n3U", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('m', pertanyaan.menu))
    dispatcher.add_handler(CallbackQueryHandler(response.response_menu, pattern='^menu'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_ekstrakResi, pattern='^a_asal'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_ekstrakResi, pattern='^a_sumber'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_ekstrakResi, pattern='^a-file_.*'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_inputResi, pattern='^b_asal'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_inputResi, pattern='^b_sumber'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_inputResi, pattern='^b-file_.*'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_inputResi, pattern='^b-lanjutan_.*'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_skeluar, pattern='^c_tujuan'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_skeluar, pattern='^c_sumber'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_skeluar, pattern='^c-file_.*'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_kalomzet, pattern='^d_tujuan'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_kalomzet, pattern='^d-file_.*'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_kalomzet, pattern='^d-lanjutan_.*'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_visualisasi, pattern='^e_tujuan'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_visualisasi, pattern='^e_visualisasi'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_visualisasi, pattern='^e-detailresi_.*'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_visualisasi, pattern='^e-lanjutan_.*'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_ambilWL, pattern='^f_'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_ambilWL, pattern='^f-ambilwl_.*'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_ambilWL, pattern='^f-ambilresi_.*'))

    dispatcher.add_handler(CallbackQueryHandler(response.response_mergesopir, pattern='^g-ambilresi_.*'))
    dispatcher.add_handler(CallbackQueryHandler(response.response_mergesopir, pattern='^g-detailresi_.*'))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
