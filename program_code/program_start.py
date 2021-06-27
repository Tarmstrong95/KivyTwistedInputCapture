from kivy.config import Config
Config.set('graphics', 'show_cursor', 1)
Config.set('graphics', 'borderless', 1)
Config.set('graphics','resizable',0)
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 800)

host_width: int = 1920
host_height: int = 1080

app_width: int = int(Config.get('graphics', 'width'))
app_height: int = int(Config.get('graphics', 'height'))

Config.set('graphics','position','custom')
Config.set('graphics', 'left', (host_width - app_width))
Config.set('graphics', 'top', (host_height - app_height))
Config.write()

from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from main import Main
from factory import Factory
from twisted.internet import reactor

screen_helper: str = """
ScreenManager: 
    Main:

<Main>:
    name: 'Main'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

"""


class Application(App):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.IV_screen: Builder = Builder.load_string(screen_helper)
        self.IV_comms_to_pg40: Factory = Factory()

    def on_start(self) -> None:
        import threading
        thread: threading.Thread = threading.Thread(target=self.runFactory, daemon = True)
        thread.start()

    def build(self) -> Builder:
        return self.IV_screen
    
    def runFactory(self) -> None:
        reactor.connectTCP("localhost", 8000, self.IV_comms_to_pg40)
        reactor.run(installSignalHandlers=False)



## RUN THE APPLICATION
if __name__ == "__main__":
    try:
        Application().run()
    except KeyboardInterrupt:
        Logger.info("KEYBOARD INTERUPT: Closing application")
        import sys
        sys.exit()
    except Exception as error:
        Logger.error("EXCEPTION: Main app exception occured: {}".format(error))

