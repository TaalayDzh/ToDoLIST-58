from db import main_db
import flet as ft


def main(page: ft.Page):
    page.title = "ToDo List"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))

        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()
        
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        return ft.Row([task_field, edit_button, save_button])

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            task_input.value = ""
            page.update()

    def delete_task(_пш):
            main_db.delete_all()
            load_task()
    
    

    task_input = ft.TextField(label='Введите задачу', expand=True)
    add_button = ft.ElevatedButton("ADD", on_click=add_task)
    delete_button = ft.ElevatedButton('DELETE', on_click=delete_task)

    page.add(ft.Row([task_input, add_button, delete_button]), task_list)

    load_task()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)