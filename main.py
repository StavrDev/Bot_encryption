from utils import TgBot
from keyboards import kb_start

app = TgBot('6392188988:AAGEksJrweYY1AhoL1bgNdcAcqGBmrIaDKc', kb_start)

if __name__ == "__main__":
    app.start()