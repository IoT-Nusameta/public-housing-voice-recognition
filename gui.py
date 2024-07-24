from nicegui import ui

old_read_str = ''
txt_path = 'test.txt'
data = {"alcon": "marmut", 'test': 'pisang'}

def read_txt(current_page):
    global old_read_str

    txt_file = open(txt_path, "r+")
    read_str = txt_file.read().lower()
    if old_read_str != read_str:
        print(read_str)
    
    if current_page == 'login':
        if 'ikaris' in read_str:
            ui.navigate.to(test_page)
    elif current_page == 'test':
        if 'tutup' in read_str:
            ui.navigate.to(login)
        
    old_read_str = read_str

@ui.page('/login')
def login():    
    def check_pass():
        if data.get(username.value) == password.value:
            ui.notify("Correct password!")
            ui.navigate.to(test_page)
        else:
            ui.notify("something is not right")
    
    ui.timer(1.0, lambda: read_txt('login'))
    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=check_pass)

@ui.page('/test_page')
def test_page():
    ui.label("This is test page")
    ui.timer(1.0, lambda: read_txt('test'))

login()
ui.run()