import pyAesCrypt as p
from aiogram import Dispatcher, executor, types, Bot
import time
import os

class TgBot:
    def __init__(
                        self,
                        token,
                        kb_start
                    ):
                    
            
            self.bot = Bot(token=token)
            self.dp = Dispatcher(self.bot)

            async def start_command(message: types.Message):
                await message.answer('Вы попали в бота шифровальщика!\n\nЗдесь вы сможете зашифровать/расшифровать свой txt-файл\n\nПриятного использования!', reply_markup=kb_start)

            async def enc_dec(callback:types.CallbackQuery):
                chat_id = callback.message.chat.id
                btn_data = callback.data
                message_id = callback.message.message_id
                if btn_data == "enc":
                    await self.bot.edit_message_text('Отправьте пароль для шифрования.',chat_id=chat_id, message_id=message_id)
                
                if btn_data == "dec":
                    await self.bot.edit_message_text('Отправьте пароль для расшифрования.',chat_id=chat_id, message_id=message_id)

            async def set_password(message:types.Message):
                password = message.text

                f_pass = open('passw.txt',"w")
                f_pass.write(password)
                f_pass.close()

                chat_id = message.chat.id
                
                await self.bot.send_message(chat_id=chat_id,text='Отправьте файл, который хотите зашифровать/расшифровать(в txt/txt.aes).')

                

            async def process_file(message: types.Message):
                file_extension = message.document.file_name.split('.')[-1].lower()

                if file_extension == "txt":
                    chat_id = message.chat.id
                    file_id = message.document.file_id
                    file_info = await self.bot.get_file(file_id)
                    file_path = file_info.file_path

                    await self.bot.download_file(file_path, 'file.txt')

                    f_pass = open('passw.txt',"r")
                    passw = f_pass.read()
                    f_pass.close()

                    p.encryptFile('file.txt', 'result.txt.aes', passw)
                    
                    await self.bot.send_document(chat_id=chat_id, document=open('result.txt.aes', 'rb'), caption='Вот твой файл')
                    os.remove('passw.txt')
                    os.remove('file.txt')
                    os.remove('result.txt.aes')

                else:
                    chat_id = message.chat.id
                    file_id = message.document.file_id
                    file_info = await self.bot.get_file(file_id)
                    file_path = file_info.file_path

                    await self.bot.download_file(file_path, 'file.txt.aes')

                    try:
                        f_pass = open('passw.txt',"r")
                        passw = f_pass.read()
                        f_pass.close()
                        
                        p.decryptFile('file.txt.aes', 'result.txt', passw)

                        await self.bot.send_document(chat_id=chat_id, document=open('result.txt', 'rb'), caption='Вот твой файл')
                        
                    except:
                        await message.answer("Был введен неверный пароль")

                    os.remove('passw.txt')
                    os.remove('file.txt.aes')
                    os.remove('result.txt')
                    

            self.dp.register_message_handler(start_command, commands=["start"]) 
            self.dp.register_callback_query_handler(enc_dec)
            self.dp.register_message_handler(set_password) 
            self.dp.register_message_handler(process_file,content_types=types.ContentType.DOCUMENT)

    def start(self):
        executor.start_polling(
                                    self.dp,
                                    skip_updates=True
                                    )       