from nicegui import ui, app

data = {"alcon": "marmut", 'test': 'pisang'}

def check_pass():
    if data.values(username.value) == password.value:
        ui.notify("Correct password!")
    else:
        ui.notify("SOmec thing is not right")

with ui.card().classes('absolute-center'):
    username = ui.input('Username')
    password = ui.input('Password', password=True, password_toggle_button=True)
    ui.button('Log in', on_click=check_pass)

ui.run()
        