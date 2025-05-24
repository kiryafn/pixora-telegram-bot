import logging
import threading
import queue
import tkinter as tk

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.services import user_service

logger = logging.getLogger('pixora')

# Очередь для передачи сообщений в GUI
message_queue: queue.Queue[str] = queue.Queue()

def _start_gui():
    root = tk.Tk()
    root.title("Pixora Logs")
    text_widget = tk.Text(root, wrap='word', state='disabled')
    text_widget.pack(expand=True, fill='both')

    def _poll_queue():
        try:
            while True:
                msg = message_queue.get_nowait()
                text_widget.configure(state='normal')
                text_widget.insert('end', msg + "\n")
                text_widget.configure(state='disabled')
                text_widget.see('end')
        except queue.Empty:
            pass
        root.after(100, _poll_queue)

    root.after(100, _poll_queue)
    root.mainloop()

# Запускаем GUI в отдельном демоническом потоке
threading.Thread(target=_start_gui, daemon=True).start()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            user = event.message.from_user
            text = event.message.text or "<non-text message>"
            lang = await user_service.get_user_lang(user.id)
            log_msg = (
                f"📥 Message from {user.full_name} "
                f"(@{user.username}) [LANG: {lang}] [ID: {user.id}]: {text}"
            )
            logger.info(log_msg)
            # выводим тоже в tkinter-окошко
            message_queue.put(log_msg)
        return await handler(event, data)