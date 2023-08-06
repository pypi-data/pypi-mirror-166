# -*- coding: utf-8 -*-
import copy
import logging

from manoutils.config.defualtConfig import configItems


class ConfigManager(object):
    configs = dict()
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(ConfigManager, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        if not ConfigManager.configs:
            self.loadConfigJsonItmes(configItems=configItems)

    def makeConfigName(self, mod, sub_mod="", desc=""):
        if sub_mod:
            return "{}_{}_{}".format(mod.upper(), sub_mod.upper(), desc.upper())
        else:
            return "{}_{}".format(mod.lower(), desc.lower())

    def getConfigItem(self, name=None, defaultVal=""):
        if not name:
            return copy.deepcopy(ConfigManager.configs)
        else:
            return ConfigManager.configs.get(name, defaultVal)

    def setConfigItem(self, name, value):
        setattr(self, name, value)
        ConfigManager.configs.update({name: value})

    def getManoIp(self):
        return self.getConfigItem("MANO_IP")

    def getManoPort(self):
        return self.getConfigItem("MANO_PORT")

    def setManoIp(self, ip):
        self.setConfigItem("MANO_IP", ip)

    def setManoPort(self, port):
        self.setConfigItem("MANO_PORT", port)

    def loadConfigFile(self):
        pass

    def loadConfigJsonItmes(self,configItems):
        for name, value in configItems.items():
            self.setConfigItem(name=name, value=value)

    def setLogger(self, logger):
        setattr(self, "logger", logger)

    def getLogger(self, keyWords="log/cmcc"):
        if self.logger:
            return self.logger
        logger = logging.getLogger(__name__)
        names = logger.manager.loggerDict.keys()
        for name in names:
            try:
                logger = logging.getLogger(name)
                if logger.handlers:
                    handler = logger.handlers[0]
                    if not hasattr(handler, "lockFilename"):
                        continue
                    if keyWords in handler.lockFilename:
                        self.setLogger(logger=logger)
                        return logger
            except Exception as e:
                pass
        return logging.getLogger(__name__)



configMgr = ConfigManager()
