# Kivy-Dynamic-Screens-Template
Modular and dynamic screen-based Kivy mobile App template (lazy importing for faster loading), with global widget interface and custom json storage with encryption capabilities.

# Features

* Screens are loaded on the fly, with lazy imports - drastically improves startup time on mobile
* Escape key (Back key on mobile) hook with screens history (every **Screen()** instance remembers previous screen automatically if there is no default "parent" screen defined; on escape\back ScreenManager will switch to the previous\"parent" screen)
* Global widget interface (**WidgetInterface()** class inherited by main App() class) provides global access from any point to self-registered widget (**SelfRegister()** class inherited by any widget class; self-registered widget needs unique 'gid' property, to properly register)
* Custom modular json storage (**AppJsonStorage()** class, inherited by main App() class) provides storage with encryption/decryption capabilities; any widget/class can store it's own local settings or access global settings. On mobile storage is a file stored in app's home folder on sdcard.
* Native android attachable/detachable WebView.


# Credits
lazy importing greatly inspired by https://github.com/rafalo1333/KivyLazyloadingExample
