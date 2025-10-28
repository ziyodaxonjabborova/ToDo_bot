from aiogram.fsm.state import StatesGroup,State

class DataTask(StatesGroup):
    new_task = State()
    get_old_name = State()
    get_new_name = State()
    get_delete_task=State()
    get_status_task=State()
    get_new_status=State()
    get_delete_task=State()

    