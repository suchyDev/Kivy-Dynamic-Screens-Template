
menuscreen_kv = '''
<ScreenMenu>:
    id: screen_menu

    BoxLayout:
        orientation: 'vertical'
        InputField:
            id: text_input_field
            gid: 'text_input_field_global_id'
        Button:
            text: 'Save'
            # this is great for local widget tree:
            #on_release: text_input_field.save_text()
            # this is great for registered widgets accessible globally:
            on_release: app.get_widget('text_input_field_global_id').save_text()
        ButtonLaunchWebView:
            text: 'WebView'
        Button:
            text: 'Quit'
            on_release: screen_menu.leave()
'''

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from generic import DynamicScreen
from generic import SelfRegister


class ScreenMenu(DynamicScreen):
    def __init__(self, **kwargs):
        self.name = 'screen_menu'
        self.kv_string = menuscreen_kv        
        super(ScreenMenu, self).__init__(**kwargs)

    def leave(self):
        self.manager.current = 'screen_quit'


class InputField(TextInput, SelfRegister):
    gid = 'text_input_field_global_id'
    def __init__(self, **kwargs):        
        super(InputField, self).__init__(**kwargs)

    def post_init_setup(self, *args):
        app =  App.get_running_app()
        #try and get encrypted text from storage
        try:
            self.stored_text = app.decrypt(app.store.get('stored_text_section')['stored_text'])
        except KeyError:
            self.stored_text = ""
        self.text = self.stored_text

    def save_text(self, *args):
        app =  App.get_running_app()
        app.store.put('stored_text_section', stored_text=app.encrypt(self.text))


class ButtonLaunchWebView(Button):
    def on_release(self, *args):
        screen_manager = App.get_running_app().root
        if not screen_manager.has_screen('screen_webview'):
            from screens.screenwebview import ScreenWebView
            screen_manager.add_widget(ScreenWebView())
        screen_manager.switch_screen('slide', 'screen_webview')