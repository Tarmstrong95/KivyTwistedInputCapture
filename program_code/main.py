from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.logger import Logger

class Main(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.IV_touch_grabber: Widget = Widget()
        self.IV_touch_grabber.on_touch_up = self.release
        self.add_widget(self.IV_touch_grabber)

    def on_enter(self) -> None:
        Logger.info('Screen transition: Entered Main')

    def release(self, touch) -> None:
        Logger.info("Touch UP: {}".format(touch.pos)) # log touch to console
        event: dict[str] = { "coords": touch.pos }
        app: App = App.get_running_app()
        factory = app.IV_comms_to_pg40
        factory.setEvent(event)
