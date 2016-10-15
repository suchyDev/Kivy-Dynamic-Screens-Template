
screen_webview_kv = '''
<ScreenWebView>:
	id: screen_webview
	BoxLayout:
		Label:
			id: info_label
			halign: 'center'
'''




from kivy.app import App
from kivy.clock import Clock, mainthread

from generic import DynamicScreen

from kivy.utils import platform
if platform == 'android':
	from android.runnable import run_on_ui_thread
	from jnius import autoclass
	WebView 		= autoclass('android.webkit.WebView')
	CookieManager 	= autoclass('android.webkit.CookieManager')
	WebViewClient 	= autoclass('android.webkit.WebViewClient')
	activity 		= autoclass('org.renpy.android.PythonActivity').mActivity
else:
	def run_on_ui_thread(func):
		''' dummy wrapper for desktop compatibility '''
		return func


class ScreenWebView(DynamicScreen):
	view_cached = None
	webview 	= None
	wvc 		= None
	webview_lock= False 	# simple lock to avoid launching two webviews
	url = 'http://google.com'

	def __init__(self, **kwargs):
		self.name = 'screen_webview'
		self.kv_string = screen_webview_kv        
		super(ScreenWebView, self).__init__(**kwargs)


	def on_enter(self, *args):
		super(ScreenWebView, self).on_enter(*args)
		if platform == 'android':
			''' on android create webview for webpage '''
			self.ids["info_label"].text = "Please wait\nAttaching WebView"
			self.webview_lock = True
			Clock.schedule_once(self.create_webview, 0)			
		else:
			''' on desktop just launch web browser '''
			self.ids["info_label"].text = "Please wait\nLaunching browser"
			import webbrowser
			webbrowser.open_new(self.url)

	@run_on_ui_thread
	def key_back_handler(self, *args):
		if self.webview:
			if self.webview.canGoBack() == True:
				self.webview.goBack()
			else:
				Clock.schedule_once(self.detach_webview, 0)
		else:
			App.get_running_app().root.switch_screen()

	@mainthread
	def quit_screen(self, *args):
		app = App.get_running_app()
		app.root.switch_screen()

	@run_on_ui_thread
	def create_webview(self, *args):
		#cookie_manager.getInstance().removeAllCookie()
		#print(dir(cookie_manager))		
		#cookie_manager.removeSessionCookie()
		#'acceptCookie', 'allowFileSchemeCookies', 'equals', 'getClass', 'getCookie', 'getInstance', 'hasCookies', 'hashCode', 'instance', 'notify', 'notifyAll', 'removeAllCookie', 'removeExpiredCookie', 'removeSessionCookie', 'setAcceptCookie', 'setAcceptFileSchemeCookies', 'setCookie', 'toString', 'wait'
		if self.view_cached is None:
			self.view_cached = activity.currentFocus
		#if self.webview is None:
		self.webview = WebView(activity)
		#self.webview.clearCache(True)
		#self.webview.clearFormData()
		#self.webview.clearHistory()
		#self.webview.clearMatches()
		#self.webview.clearSslPreferences()

		cookie_manager = CookieManager.getInstance()
		cookie_manager.removeAllCookie()

		settings = self.webview.getSettings()
		settings.setJavaScriptEnabled(True)
		settings.setUseWideViewPort(True) 			# enables viewport html meta tags
		settings.setLoadWithOverviewMode(True) 		# uses viewport
		settings.setSupportZoom(True) 				# enables zoom
		settings.setBuiltInZoomControls(True) 		# enables zoom controls

		settings.setSavePassword(False)
		settings.setSaveFormData(False)
		#if self.wvc is None:
		self.wvc = WebViewClient()
		self.webview.setWebViewClient(self.wvc)
		activity.setContentView(self.webview)
		self.webview.loadUrl(self.url)
		self.webview_lock = False

	@run_on_ui_thread
	def detach_webview(self, *args):
		if self.webview_lock == False:
			if self.webview:
				self.webview.loadUrl("about:blank")
				self.webview.clearHistory() # refer to android webview api
				self.webview.clearCache(True)
				self.webview.clearFormData()
				self.webview.freeMemory()
				#self.webview.pauseTimers()
				activity.setContentView(self.view_cached)
			Clock.schedule_once(self.quit_screen, 0)