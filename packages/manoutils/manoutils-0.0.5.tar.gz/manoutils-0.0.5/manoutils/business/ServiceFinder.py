# -*- coding: utf-8 -*-
import copy
import random
import requests
import logging

from manoutils.log.LogTemplate import LogTemplate
from manoutils.config.ConfigManager import configMgr
from manoutils.common.common import ignore_case_get

logger = configMgr.getLogger()


class ServiceFinder(object):
    services = list()
    def __init__(self):
        self.msbIp = configMgr.getManoIp()
        self.msbPort = configMgr.getManoPort()
        self.msbUrl = "http://{}:{}/api/microservices/v1/services".format(self.msbIp, self.msbPort)

    def getMsbServices(self):
        desc = "{}->{}".format(configMgr.getConfigItem(name="SERVICE_NAME", defaultVal="nfvo"), "MSB")
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        url = self.msbUrl
        LogTemplate().before_send_req(desc=desc, method="GET", url=url, headers=headers, logLevel=logging.DEBUG)
        rsp = requests.get(url=url, headers=headers, timeout=10, verify=False)
        LogTemplate().after_send_req(desc=desc, request=rsp, logLevel=logging.DEBUG)
        if rsp.ok:
            services = rsp.json()
            services = services if isinstance(services, list) else list()
            return services
        else:
            return list()

    def syncServices(self):
        ServiceFinder.services = self.getMsbServices()

    def getService(self, serviceName):
        services = copy.deepcopy(ServiceFinder.services)
        for service in services:
            if serviceName == ignore_case_get(service, "serviceName"):
                return service
        return dict()

    def getServices(self):
        return copy.deepcopy(ServiceFinder.services)

    def pickNode(self, nodes):
        if isinstance(nodes, list):
            return nodes[random.randint(0,len(nodes)-1)]
        else:
            return dict()

    def getNode(self, serviceName):
        servcie = self.getService(serviceName=serviceName)
        nodes = ignore_case_get(servcie, "nodes")
        node = self.pickNode(nodes=nodes)
        return node

    def getServiceNodeUrl(self, url):
        services = self.getServices()
        for i in range(0, len(url.split("/"))):
            if i == "api":
                url.split("/")
        url.split("/")




