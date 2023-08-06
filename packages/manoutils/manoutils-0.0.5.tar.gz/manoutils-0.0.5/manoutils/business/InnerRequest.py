# -*- coding: utf-8 -*-
import requests
import json

from urlparse import urljoin
from manoutils.log.LogTemplate import LogTemplate
from manoutils.config.ConfigManager import configMgr

logger = configMgr.getLogger()


class InnerRequest(object):
    def __init__(self):
        self.innerIp = configMgr.getManoIp()
        self.innerPort = configMgr.getManoPort()
        self.innerBaseUrl = "http://{}:{}".format(self.innerIp, self.innerPort)
        self.innerServiceType = ""

    def getServiceUrl(self):
        pass

    def getRomteServiceName(self):
        return "nfvo"

    def getLocalServiceName(self):
        return configMgr.getConfigItem(name="SERVICE_NAME", defaultVal="nfvo")

    def makeSSLArgs(self):
        return {"verify": False}

    def makeUrl(self, resource='', url=''):
        if url:
            return url
        if resource:
            url = urljoin(self.innerBaseUrl, resource)
        else:
            url = self.innerBaseUrl
        return url

    def makeHeaders(self, headers):
        if headers:
            return headers
        else:
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            return headers

    def makeDesc(self, desc):
        if desc:
            if "->" not in desc:
                desc = "{}->{} {}".format(self.getLocalServiceName(), self.getRomteServiceName(), desc)
        else:
            desc = "{}->{} ".format(self.getLocalServiceName(), self.getRomteServiceName())
        return desc

    def makeBody(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        return data

    def get(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="GET", url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.get(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def post(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="POST", url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.post(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def put(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="PUT", url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.put(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def delete(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="DELETE", data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.delete(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp
