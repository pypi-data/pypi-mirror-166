# -*- coding: utf-8 -*-
import logging
import inspect

from manoutils.config.ConfigManager import configMgr
from manoutils.common.constant import BASE1_HEADERS

logger = configMgr.getLogger()


class LogTemplate(object):
    def receive_req(self, desc="", request="", ext_msg="", log_level=logging.INFO):
        try:
            method = request.method
            url = "https://{}{}".format(request.get_host(), request.get_full_path())
            headers = "Content-Type: {}, ".format(request.META.get("CONTENT_TYPE"))
            if request.META.get("HTTP_X_AUTH_TOKEN"):
                headers = headers + "X-Auth-Token: {}, ".format(request.META.get("HTTP_X_AUTH_TOKEN"))
            if request.META.get("HTTP_X_AUTH_USERNAME"):
                headers = headers + "X-Auth-Username: {}, ".format(request.META.get("HTTP_X_AUTH_USERNAME"))
            if request.META.get("HTTP_X_AUTH_PASSWORD"):
                headers = headers + "X-Auth-Password: {}, ".format(request.META.get("HTTP_X_AUTH_PASSWORD"))
            if len(str(request.data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_data = '***data too big to print***'
            else:
                message_data = request.data
            message = "Receive {} request: method: {}, url {}, headers: {}, body: {} ".format(desc,method,url,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.log(level=log_level, msg=message)
        except:
            pass

    def response_req(self, desc="", status="", headers=BASE1_HEADERS, data="", ext_msg="", result="", logLevel=logging.INFO):
        try:
            if result:
                status = result.get_code()
                data = result.get_result()
            if len(str(data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_data = '***data too big to print***'
            else:
                message_data = data
            message = "Response {} : status_code: {}, headers: {}, body: {} ".format(desc,status,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.log(level=logLevel, msg=message)
        except:
            pass


    def before_send_req(self, desc="", method="", url="", headers=BASE1_HEADERS, data="", ext_msg="", logLevel=logging.INFO):
        try:
            if len(str(data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_data = '***data too big to print***'
            else:
                message_data = data
            message = "Send {} request: method: {},  url: {}, headers: {}, body: {} ".format(desc,method,url,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.log(level=logLevel, msg=message)
        except:
            pass

    def after_send_req(self, desc="", request="", ext_msg="", logLevel=logging.INFO):
        try:
            try:
                data = request.json()
                if len(str(data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                    message_data = '***data too big to print***'
                else:
                    message_data = data
            except:
                message_data = ""
            headers = request.headers
            status_code = request.status_code
            message = "Receive {} response: status_code: {}, headers: {}, body: {} ".format(desc,status_code,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.log(level=logLevel, msg=message)
        except:
            pass

