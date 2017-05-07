from opencvGame import opencvGameClass;
class GameStarter(object):
    def __init__(self):
        self._opencvgameobject = opencvGameClass();
    def run(self):
        self._opencvgameobject.settingUpTheDisplay();
        self._opencvgameobject.gameLoop();
if __name__ == "__main__":
    GameStarter().run();
