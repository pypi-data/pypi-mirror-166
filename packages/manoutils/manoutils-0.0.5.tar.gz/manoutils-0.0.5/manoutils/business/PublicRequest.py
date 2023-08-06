# -*- coding: utf-8 -*-
from manoutils.config.ConfigManager import configMgr
from manoutils.business.ExsysRequest import ExsysClient

logger = configMgr.getLogger()


class PublicRequest(ExsysClient):
    pass
