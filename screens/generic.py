
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class DynamicScreen(Screen):
    last_screen = None
    kv_string = None
    kv_file = None
    kv_loaded = False

    def __init__(self, **kwargs):
        '''
        if kv is not loaded the load it either from string or a file specified
        need to specify "kv_string" or "kv_file", as well as unique "name"
        '''
        if not self.kv_loaded:
            from kivy.lang import Builder
            if self.kv_string:
                Builder.load_string(self.kv_string)
            if self.kv_file:
                Builder.load_file(self.kv_file)
            self.kv_loaded = True
        super(DynamicScreen, self).__init__(**kwargs)








from kivy.storage.jsonstore import JsonStore
from kivy.properties import NumericProperty

class AppJsonStorage(object):
    '''
    Json storage interface. Inherited by app class.
    ----
    self.store.put('section', setting='setting, value='value')
    self.store.get('section')['setting']
    '''
    key = 'ThIsWoUlDbEyOuRrAnDoMkYe'
    example_property = NumericProperty()
    def __init__(self, **kwargs):
        self.init_settings()
        #self.get_stored_credentials()
        #self.get_stored_settings()

    def init_settings(self):
        #app = App.get_running_app()
        from os.path import join as os_path_join
        self.store = JsonStore(os_path_join(self.user_data_dir, 'storage'))
                
        # gui persistent settings
        try:
            self.example_property = self.store.get('example_property_section')['example_property']
             #Logger.info('StorageMdl: found stored gui_multi: {}'.format(self.gui_multi))
        except KeyError:
            self.example_property = 2.0
            #Logger.info('StorageMdl: failed to find gui_multi, setting default')
        

    def on_example_property(self, *args):
        self.store.put('example_property_section', example_property=self.example_property)
        #Logger.info('StorageMdl: changing gui_multi to: {}'.format(self.gui_multi))
    
    def encrypt(self, plaintext):
        from base64 import b64encode as base64_b64encode
        from Crypto.Cipher.XOR import new as XOR_new

        cipher = XOR_new(self.key)      
        return base64_b64encode(cipher.encrypt(plaintext))

    def decrypt(self, ciphertext):
        from base64 import b64decode as base64_b64decode
        from Crypto.Cipher.XOR import new as XOR_new

        cipher = XOR_new(self.key)
        return cipher.decrypt(base64_b64decode(ciphertext))











from kivy.app import App

class WidgetInterface(object):
    '''
    Interface for  global widget access.
    Creates dict object with sctructure: { widget.gid : widget_object }
    Registered widget needs unique 'gid' StringProperty
    Usually inherited by main App class, then access registered widget with app.get_widget(widget.gid)
    '''
    global_widgets = {}
    def register_widget(self, widget_object):
        ''' registers widget only if it has unique gid '''
        if widget_object.gid not in self.global_widgets:
            self.global_widgets[widget_object.gid] = widget_object
            #Logger.info('WidgetIf : registering widget: {}'.format(str(widget_object.gid)))
            #core.database["runtime_settings"]["registered_widgets"].append(widget_object.gid)

    def unregister_widget(self, widget_object, cleanup=False):
        ''' unregisters widget from registered widgets directly by object instance '''
        if widget_object.gid in self.global_widgets:
            #Logger.info('WidgetIf : unregistering widget: {}'.format(str(widget_object.gid)))
            self.global_widgets.pop(widget_object.gid)
            if cleanup:
                self.cleanup_widget(widget_object)              
        else:
            #Logger.info('WidgetIf : widget "{}" is not registered.'.format(str(widget_object.gid)))
            pass

    def unregister_widget_gid(self, gid, cleanup=False):
        '''  unregisters widget from registered widgets by its gid'''
        widget_object = self.get_widget(gid)
        if widget_object is not None and gid in self.global_widgets:
            #Logger.info('WidgetIf : unregistering widget: {}'.format(str(gid)))
            self.global_widgets.pop(gid)
            if cleanup:
                self.cleanup_widget(widget_object)
        else:
            #Logger.info('WidgetIf : widget "{}" is not registered.'.format(str(widget_object.gid)))
            pass

    def get_widget(self, widget_gid):
        ''' returns widget object by its 'gid' (if registered) '''
        if widget_gid in self.global_widgets:
            return self.global_widgets[widget_gid]
        else:
            return None

    def register_weak_object(self, widget_object):
        ''' registers object for aggressive memory cleanup (use for high memory objects, like large images)'''
        if widget_object.gid not in self.weak_objects:
            self.weak_objects[widget_object.gid] = widget_object
            #Logger.info('WidgetIf : registering weak object: {}'.format(str(widget_object.gid)))
            core.database["runtime_settings"]["weak_objects"].append(widget_object)

    def cleanup_weak_objects(self):
        ''' removes weak_objects with all of its children '''
        for obj in copy.copy(self.weak_objects):
            self.iterate_children(obj)
            self.cleanup_widget(obj)
        self.weak_objects = {} # resets weak_objects dict
        #gc.collect()

    def iterate_children(self, widget):
        ''' iterates through children and deletes all recursively '''
        for child in widget.children:
            #Logger.info('WidgetIf : purging: {}'.format(str(widget_object.gid)))            
            self.iterate_children(child)        # check for children first
            child.parent.remove_widget(child)   # deattach widget from parent
            if hasattr(child, 'gid'):
                self.unregister_widget(child, cleanup=True) # if current object is registered then unregister first
            self.cleanup_widget(child)          # cleanup and delete object

    def cleanup_widget(self, widget_object):
        #Logger.info('WidgetIf : trying to purge widget "{}"'.format(str(widget_object)))
        try:
            widget_object.canvas.clear() # also try to cleanup object
        except:
            pass
        widget_object.clear_widgets()
        del widget_object











from kivy.clock import Clock

class SelfRegister(object):
    def __init__(self, **kwargs):
        #super(SelfRegister, self).__init__(**kwargs)
        #print('self registered')
        self.register_self()
        Clock.schedule_once(self.post_init_setup, 0)

    #@mainthread
    def register_self(self):
        app = App.get_running_app()
        app.register_widget(self)

    def post_init_setup(self, *args):
        pass

    # def __del__(self):
    #     try:
    #         Logger.info('Widget: {} deleted'.format(str(self.gid)))
    #     except:
    #         Logger.info('Widget: {} deleted'.format(str(self)))






class WeakObject(object):
    def __init__(self, **kwargs):
        super(WeakObject, self).__init__(**kwargs)
        self.register_self_as_weak()

    #@mainthread
    def register_self_as_weak(self):
        app = App.get_running_app()
        app.register_weak_object(self)  # registers object for clearing canvas on gc

    # def __del__(self, **kwargs):
    #     try:
    #         Logger.info('Widget: (weak) {} deleted'.format(str(self.gid)))
    #     except:
    #         Logger.info('Widget: (weak) {} deleted'.format(str(self)))