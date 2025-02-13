# -*- encoding: utf-8 -*-
import mobase
from PyQt6.QtCore import QDir

from ..basic_features import BasicModDataChecker, GlobPatterns
from ..basic_game import BasicGame, replace_variables


class HogwartsLegacyModDataChecker(BasicModDataChecker):
    def __init__(self, patterns: GlobPatterns = GlobPatterns()):
        super().__init__(
            GlobPatterns(
                valid=["Content"],
                move={
                    "*.pak": "Content/Paks/~mods/",
                    "*.utoc": "Content/Paks/~mods/",
                    "*.ucas": "Content/Paks/~mods/",
                },
            ).merge(patterns),
        )


class HogwartsLegacyGame(BasicGame):
    Name = "Hogwarts Legacy Support Plugin"
    Author = "NeuroticNinjah"
    Version = "1.0.3"

    GameName = "Hogwarts Legacy"
    GameShortName = "hogwartslegacy"
    GameNexusName = "hogwartslegacy"
    GameBinary = "HogwartsLegacy.exe"
    GameDataPath = "%GAME_PATH%/Phoenix"
    GameDocumentsDirectory = (
        "%USERPROFILE%/AppData/Local/Phoenix/Saved/Config/WindowsNoEditor/"
    )
    GameDocumentsDirectorySteam = (
        "%USERPROFILE%/AppData/Local/Hogwarts Legacy/Saved/Config/WindowsNoEditor/"
    )
    # The userid will be appended under `.savesDirectory()`
    GameSavesDirectory = "%USERPROFILE%/AppData/Local/Phoenix/Saved/SaveGames/"
    GameSaveExtension = "sav"
    GameSteamId = 990080

    def init(self, organizer: mobase.IOrganizer):
        # Fairly hacky method, but should be reliable enough for the moment
        if not self.documentsDirectory().exists("engine.ini"):
            self.documentsDirectory()
        BasicGame.init(self, organizer)
        self._register_feature(HogwartsLegacyModDataChecker())
        return True

    def documentsDirectory(self) -> QDir:
        # Fairly hacky method to choose Epic/Steam path, but should be reliable enough for the moment
        if (documents_dir := super().documentsDirectory()).exists("engine.ini"):
            return documents_dir
        return QDir(replace_variables(self.GameDocumentsDirectorySteam, self))

    def initializeProfile(
        self, directory: QDir, settings: mobase.ProfileSetting
    ) -> None:
        # Create the mods directory if it doesn't exist
        if not (modsPath := self.dataDirectory()).exists():
            modsPath.mkpath(".")
        return super().initializeProfile(directory, settings)

    def iniFiles(self):
        return ["Engine.ini", "GameUserSettings.ini", "Game.ini", "Input.ini"]

    def savesDirectory(self) -> QDir:
        save_dir = super().savesDirectory()
        if save_dir.exists() and (user_ids := save_dir.entryList()):
            save_dir.cd(user_ids[0])
        return save_dir
