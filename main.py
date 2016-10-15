import sys
sys.dont_write_bytecode = True

__version__ = "1.0"


import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen

from screens.generic import WidgetInterface, AppJsonStorage



class AppScreenManager(ScreenManager):
    duration = .25
    def __init__(self, **kwargs):
        super(AppScreenManager, self).__init__(**kwargs) # make sure we aren't overriding any important functionality
        #self.transition = SlideTransition()
        
    def switch_screen(self, style = 'slide', screen_to_switch = None, clear = False, prompt = None, *args):
        '''
        switch screen with given transition
        if screen is not defined it will switch to the last remembered screen (screen variable: last_screen)
        if clear is true it will overwrite screen variable: last_screen
        '''
        # #from kivy.uix.screenmanager import ScreenManager, FadeTransition#, SlideTransition, SwapTransition, WipeTransition, FallOutTransition, RiseInTransition
        # #from kivy.garden.moretransitions import BlurTransition#,PixelTransition,RippleTransition,RVBTransition
        
        # #app = App.get_running_app()
        # #self.last_screen = app.root.current
        # #SlideTransition, SwapTransition, WipeTransition, FallOutTransition, RiseInTransition, FadeTransition
        # #PixelTransition,RippleTransition,BlurTransition,RVBTransition

        # transitions = { #'rise'  : RiseInTransition(),
        #                 #'fall'  : FallOutTransition(),
        #                 'slide' : SlideTransition(),
        #                 #'blur' : BlurTransition(),
        #                 #'fade'  : FadeTransition()  }
        # #transition = SlideTransition(direction="left")
        # self.transition = transitions[style]    # setting transition style
        self.transition.direction = 'down'
        self.transition.duration = self.duration
        cached_screen = self.current            # caching current screen to write it later as last_screen
        if screen_to_switch:
            ''' if there is target screen defined then switch to it '''
            self.current = screen_to_switch
            if prompt:
                self.get_screen(self.current).set_prompt(prompt)
        else:
            ''' else switch to last+screen '''
            self.current = self.get_screen(self.current).last_screen
        if self.get_screen(self.current).last_screen is None:
            ''' if current (newly switched) screen has no last_screen defined, then define it now from cached_screen '''
            self.get_screen(self.current).last_screen = cached_screen
        elif clear == True:
            ''' if clear is forced, then overwrite current last_screen with cached screen anyway '''
            self.get_screen(self.current).last_screen = cached_screen

    def on_current(self, *args):
        super(AppScreenManager, self).on_current(*args)











class KivyDynamicLoadingTemplate(App, WidgetInterface, AppJsonStorage):
    '''Main kivy application class.'''

    def build(self):
        '''Sets AppScreenManager as root widget.'''
        sm = AppScreenManager()
        from screens.screensbasic import PostSplashScreen
        sm.add_widget(PostSplashScreen())
        #self.title = core.app_name + " " + core.app_version
        return sm

    def on_start(self):
        '''Configures app when it starts.'''
        self.use_kivy_settings = False
        from kivy.base import EventLoop, runTouchApp
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)


    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def open_settings(self):
        '''Prevents the settings panel from opening.'''
        pass
    
    def hook_keyboard(self, window, key, *largs):               
        '''
        hooks back button (esc on desktop) to prevent auto close
        '''
        screens_to_ignore = ['screen_post_splash', 'screen_start', 'screen_menu']
        screens_with_key_back_handler = ['screen_webview']
        print self.root.current
        if key == 27:
            ''' on key back (escape) '''
            if self.root.transition.is_active:
                ''' if any transition is in progress, then do nothing and return'''
                return True
            else:
                if self.root.current in screens_to_ignore:
                    ''' if current screen is any of the specified, then ignore'''
                    return True
                elif self.root.current == 'screen_which_should_back_to_menu':
                    ''' if current screen is any of the speciied, then show screen_start '''
                    self.root.switch_screen('slide', 'screen_menu', clear=True)
                elif self.root.current in screens_with_key_back_handler:
                    self.root.get_screen(self.root.current).key_back_handler()                    
                else:
                    ''' if other screen then switch to last_screen remembered '''
                    self.root.switch_screen()
                return True
        ''' otherwise return and do nothing '''
        return False




if __name__ == '__main__':
    KivyDynamicLoadingTemplate().run()
