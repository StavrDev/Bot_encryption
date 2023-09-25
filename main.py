from utils import TgBot
from keyboards import kb_start

app = TgBot(TOKEN_BOT, kb_start)

if __name__ == "__main__":
    app.start()
