

startscreen_kv = '''
<ScreenStart>:
    #kv_string: 'startscreen_kv'
    #name: 'screen_start'

    Label:
        text: 'Welcome! Tap to start...'
        #on_release: root.start()
'''

from kivy.app import App
from kivy.uix.screenmanager import Screen
from generic import DynamicScreen




class PostSplashScreen(Screen):
    last_screen = None
    def __init__(self, **kwargs):
        self.name = 'screen_post_splash'
        super(PostSplashScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        # from kivy.config import Config
        # Config.set('graphics', 'maxfps', '60')
        # Config.set('graphics', 'multisamples', '0')
        # Config.write()

        if not self.manager.has_screen('screen_start'):
            #from screens.screensbasic import ScreenStart, ScreenPreLeave
            self.manager.add_widget(ScreenStart())
            self.manager.add_widget(ScreenPreLeave())
        self.manager.switch_screen('slide', 'screen_start')


class ScreenStart(DynamicScreen):
    def __init__(self, **kwargs):
        self.kv_string = startscreen_kv
        self.name = 'screen_start'
        super(ScreenStart, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        if not self.manager.has_screen('screen_menu'):
            from screenmenu import ScreenMenu
            self.manager.add_widget(ScreenMenu())
        self.manager.current = 'screen_menu'



class ScreenPreLeave(Screen):
    last_screen = None
    def __init__(self, **kwargs):
        self.name = 'screen_quit'
        super(ScreenPreLeave, self).__init__(**kwargs)

    def on_enter(self, *args):
        #app.stop_event.set()
        App.get_running_app().stop()
