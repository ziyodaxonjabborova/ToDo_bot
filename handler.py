from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from buttons import CRUD_BUTTON, SEE_BUTTON, BACK_BUTTON, UPDATE_BUTTON
from states import DataTask
from database import add_task as db_add_task, get_tasks_by_status, update_task_name, delete_task, update_task_status

router = Router()

# 🔹 /start handler
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("📝 Quyidagilardan birini tanlang:", reply_markup=CRUD_BUTTON)

# ➕ Add task
@router.message(F.text == "➕ Add task")
async def add_task(message: Message, state: FSMContext):
    await message.answer("✍️ Yangi vazifa nomini kiriting:", reply_markup=BACK_BUTTON)
    await state.set_state(DataTask.new_task)

@router.message(DataTask.new_task)
async def save_task(message: Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await state.clear()
        await message.answer("🏠 Asosiy menyuga qaytdingiz:", reply_markup=CRUD_BUTTON)
        return

    task = message.text.strip()
    db_add_task(message.chat.id, task)
    await message.answer("✅ Vazifa muvaffaqiyatli saqlandi!", reply_markup=CRUD_BUTTON)
    await state.clear()

# 📋 See tasks
@router.message(F.text == "📋 See tasks")
async def see_button(message: Message):
    await message.answer("📝 Bittasini tanlang:", reply_markup=SEE_BUTTON)
    await message.answer("⬅️ Orqaga qaytish uchun tugmani bosing 👇", reply_markup=BACK_BUTTON)

@router.callback_query(F.data.startswith("see_"))
async def see_tasks(call: CallbackQuery):
    status = call.data.split("_")[1]
    tasks = get_tasks_by_status(call.from_user.id, status)

    if not tasks:
        await call.message.answer("❌ Hozircha bu toifada vazifa yo'q.", reply_markup=BACK_BUTTON)
        return

    text = "📝 <b>Topilgan vazifalar:</b>\n\n"
    for task in tasks:
        text += f"🔹 {task['name']} — <i>{task['status'].capitalize()}</i>\n"

    await call.message.answer(text, parse_mode="HTML", reply_markup=BACK_BUTTON)

# ⬅️ Back
@router.message(F.text == "⬅️ Back")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Asosiy menyuga qaytdingiz:", reply_markup=CRUD_BUTTON)

# ✏️ Update task
@router.message(F.text == "✏️ Update task")
async def update_button(message: Message):
    await message.answer("Qaysi birini o'zgartirmoqchisiz:", reply_markup=UPDATE_BUTTON)

# 📝 Update name
@router.callback_query(F.data == "update_name")
async def update_name_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("✏️ Qaysi task nomini o‘zgartirmoqchisiz?", reply_markup=BACK_BUTTON)
    await state.set_state(DataTask.get_old_name)
    await state.update_data(user_id=call.from_user.id)

@router.message(DataTask.get_old_name)
async def get_old_name(message: Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await state.clear()
        await message.answer("🏠 Asosiy menyuga qaytdingiz:", reply_markup=CRUD_BUTTON)
        return

    await state.update_data(old_name=message.text)
    await message.answer("🆕 Yangi nomni kiriting:", reply_markup=BACK_BUTTON)
    await state.set_state(DataTask.get_new_name)

@router.message(DataTask.get_new_name)
async def get_new_name(message: Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await state.clear()
        await message.answer("🏠 Asosiy menyuga qaytdingiz:", reply_markup=CRUD_BUTTON)
        return

    data = await state.get_data()
    user_id = data["user_id"]
    old_name = data["old_name"]
    new_name = message.text

    result = update_task_name(user_id, old_name, new_name)
    if result:
        await message.answer("✅ Task nomi muvaffaqiyatli o‘zgartirildi!", reply_markup=CRUD_BUTTON)
    else:
        await message.answer("⚠️ Bunday nomdagi task topilmadi. ⬅️ Back tugmasini bosing yoki bosh menyuga qayting.", reply_markup=BACK_BUTTON)
    await state.clear()

# 🔄 Update status
@router.callback_query(F.data == "update_status")
async def update_status_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🔄 Qaysi taskning statusini o‘zgartirmoqchisiz?", reply_markup=BACK_BUTTON)
    await state.set_state(DataTask.get_status_task)
    await state.update_data(user_id=call.from_user.id)

@router.message(DataTask.get_status_task)
async def get_status_task(message: Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await state.clear()
        await message.answer("🏠 Asosiy menyuga qaytdingiz:", reply_markup=CRUD_BUTTON)
        return

    await state.update_data(task_name=message.text)
    await message.answer("🟢 Yangi statusni kiriting (pending yoki done):", reply_markup=BACK_BUTTON)
    await state.set_state(DataTask.get_new_status)

@router.message(DataTask.get_new_status)
async def get_new_status(message: Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await state.clear()
        await message.answer("🏠 Asosiy menyuga qaytdingiz:", reply_markup=CRUD_BUTTON)
        return

    data = await state.get_data()
    user_id = data["user_id"]
    task_name = data["task_name"]
    new_status = message.text.lower()

    if new_status not in ["pending", "done"]:
        await message.answer("⚠️ Status noto'g'ri kiritildi. Iltimos 'pending' yoki 'done' yozing:", reply_markup=BACK_BUTTON)
        return  

    result = update_task_status(user_id, task_name, new_status)
    if result:
        await message.answer(f"✅ Status '{new_status}' ga o'zgartirildi!", reply_markup=CRUD_BUTTON)
    else:
        await message.answer("⚠️ Bunday nomdagi task topilmadi!", reply_markup=BACK_BUTTON)

    await state.clear()

# 🗑 Delete task
@router.message(F.text == "🗑 Delete task")
async def delete_task_start(message: Message, state: FSMContext):
    await message.answer("🗑 Qaysi taskni o'chirmoqchisiz?", reply_markup=BACK_BUTTON)
    await state.set_state(DataTask.get_delete_task)
    await state.update_data(user_id=message.chat.id)

@router.message(DataTask.get_delete_task)
async def delete_task_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    task_name = message.text

    result = delete_task(user_id, task_name)
    if result:
        await message.answer("🗑 Task muvaffaqiyatli o'chirildi!", reply_markup=CRUD_BUTTON)
    else:
        await message.answer("⚠️ Bunday task topilmadi. ⬅️ Back tugmasini bosing va qayta urinib ko'ring.", reply_markup=BACK_BUTTON)

    await state.clear()
