# # bot/dialogs/profile_dialog.py
#
# from aiogram import Dispatcher
# from aiogram.types import Message, CallbackQuery
# from aiogram.filters import Command
# from aiogram.fsm.storage.memory import MemoryStorage
#
# from aiogram_dialog import Dialog, Window, setup_dialogs, DialogManager
# from aiogram_dialog.widgets.text import Const, Format
# from aiogram_dialog.widgets.kbd import Button
# from aiogram_dialog.widgets.input import MessageInput
#
# from aiogram.fsm.state import State, StatesGroup
#
# from data.repositories.user_repository import user_repository
#
# class ProfileSG(StatesGroup):
#     waiting_for_name = State()
#     waiting_for_email = State()
#     waiting_for_phone = State()
#     summary = State()
#
#
# # 3) Handlers для каждого шага
# async def name_handler(m: Message, dialog: DialogManager):
#     dialog.current_context().dialog_data["name"] = m.text
#     await dialog.next()
#
# async def email_handler(m: Message, dialog: DialogManager):
#     dialog.current_context().dialog_data["email"] = m.text
#     await dialog.next()
#
# async def phone_handler(m: Message, dialog: DialogManager):
#     dialog.current_context().dialog_data["phone"] = m.text
#     await dialog.next()
#
#
# # 4) Финальный on_click
# async def finish_handler(c: CallbackQuery, button, dialog: DialogManager):
#     data = dialog.current_context().dialog_data
#     user = await user_repository.get_by_id(c.from_user.id)
#     if user:
#         user.full_name = data["name"]
#         user.email      = data["email"]
#         user.phone      = data["phone"]
#         await user_repository.save(user)
#
#     await c.message.answer(
#         f"✅ Данные сохранены:\n"
#         f"• Имя: {data['name']}\n"
#         f"• E-mail: {data['email']}\n"
#         f"• Телефон: {data['phone']}"
#     )
#     await dialog.done()
#
#
# # 5) Сам Dialog
# profile_dialog = Dialog(
#     Window(
#         Const("👤 Как вас зовут?"),
#         MessageInput(name_handler),
#         state=ProfileSG.waiting_for_name,
#     ),
#     Window(
#         Format("Отлично, {name}! Укажите ваш e-mail:"),
#         MessageInput(email_handler),
#         state=ProfileSG.waiting_for_email,
#     ),
#     Window(
#         Format("Почта: {email}\nТеперь введите телефон:"),
#         MessageInput(phone_handler),
#         state=ProfileSG.waiting_for_phone,
#     ),
#     Window(
#         Format(
#             "Проверьте:\n"
#             "• Имя: {name}\n"
#             "• E-mail: {email}\n"
#             "• Телефон: {phone}"
#         ),
#         Button(Const("Завершить"), id="finish", on_click=finish_handler),
#         state=ProfileSG.summary,
#     ),
# )
#
#
# # 6) Стартовый хэндлер
# async def cmd_register(message: Message, dialog_manager: DialogManager):
#     # стартуем диалог
#     await dialog_manager.start(ProfileSG.waiting_for_name)
#
# # 7) Функция-инициализатор: зовите её из register_handlers(dp)
# def setup_dialog(dp: Dispatcher):
#     # Обязательно назначаем storage
#     dp.fsm.storage = MemoryStorage()
#
#     # Регистрируем диалог и команду
#     setup_dialogs(dp)
#     dp.message.register(cmd_register, Command("register"))