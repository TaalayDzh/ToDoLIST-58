from db import main_db
import flet as ft


def main(page: ft.Page):
    page.title = "ToDo List"
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column()

    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completion in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completion=completion))

        page.update()

    def create_task_row(task_id, task_text, completion):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        checkbox = ft.Checkbox(
            value=bool(completion),
            on_change=lambda e: toggle_task(task_id=task_id, is_completion=e.control.value)
        )

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()
        
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_tasks(new_task=task_field.value, task_id=task_id)
            load_task()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def delete_single(_):
            main_db.delete_tasks(task_id)
            load_task()

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_single)

        return ft.Row([checkbox, task_field, edit_button, save_button, delete_button])

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completion=None))
            task_input.value = ""
            page.update()

    def clear_input(_):
        task_input.value = ""
        page.update()
    
    def toggle_task(task_id, is_completion):
        main_db.update_tasks(task_id=task_id, completion=int(is_completion))
        load_task()
    
    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    snackbar =ft.SnackBar(
        content=ft.Text(''), 
        bgcolor=ft.Colors.RED_400,
        duration=2000
    )
 
    def check_length():
        if len(task_input.value) >= 100:
          page.snack_bar = ft.SnackBar(ft.Text("Нельзя ввести больше 100 символов!"))
          page.snack_bar.open = True
          page.update()
          return

    task_input = ft.TextField(
        label='Введите задачу',
        expand=True,
        max_length=100,
        on_change=lambda e: check_length()
    )

    add_button = ft.ElevatedButton("ADD", on_click=add_task)
    delete_button = ft.ElevatedButton('CLEAR', on_click=clear_input)
    
    filter_button = ft.Row([
        ft.ElevatedButton('Все задачи!', on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('В работе!', on_click=lambda e: set_filter('uncompletion')),
        ft.ElevatedButton('Готово!', on_click=lambda e: set_filter('completion')),
    ])
        
    page.add(ft.Row([task_input, add_button, delete_button]), task_list, filter_button)

    load_task()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
