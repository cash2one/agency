#!/usr/bin/env python
# encoding: utf-8


"""
@author: william
@contact: 1342247033@qq.com
@site: http://www.xiaolewei.com
@file: client.py
@time: 22/03/2018 19:15
"""
import kafka
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from agency.core import logger

logger = logger.get('Client')

API_CLIENT = 'api'
BROWSER_CLIENT = 'browser'


class Account(object):
    def __init__(self, cfg):
        self._cfg = cfg


class Client(object):
    '''
    Client shouldn't block the process
    '''

    _producer = None  # type: kafka.KafkaProducer
    _statistic_topic = 'ad.original.statistic'

    def __init__(self, account: Account):
        self._account = account

    @property
    def producer(self):
        return self._producer

    @producer.setter
    def producer(self, producer):
        self._producer = producer

    def perform(self, commands):
        '''
        :param commands:
        :return:
        '''
        raise NotImplemented

    def report_perform_res(self, id, resp_cnt, resp_status):
        self._producer.send('agency.command.reporter', {
            'id': id,
            'resp_cnt': resp_cnt,
            'resp_status': resp_status,
        })
        logger.info('Reporter results of performing commands successfully')


    def statistic(self):
        '''
        This func should report the latest data
        :return:
        '''
        raise NotImplemented

    def quit(self):
        '''
        Client should quit elegantly when called this fun
        :return:
        '''
        raise NotImplemented


class APIClient(Client):
    _type = API_CLIENT

    def __init__(self, account: Account):
        Client.__init__(self, account)


class BrowserClient(Client):
    _type = BROWSER_CLIENT
    _wait_time = 5
    _browser = None
    _wait = None
    _ttl = 300

    def __init__(self, account: Account):
        self._browser = webdriver.Chrome()
        self._browser.implicitly_wait(10)
        self._wait = WebDriverWait(self._browser, self._wait_time)
        Client.__init__(self, account)
        self._login()

    def _login(self):
        raise NotImplemented




