#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import requests
import unittest
import time

try:
    sys.path.insert(0, os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient, CulebraTestCase

TAG = 'CULEBRA'


class CulebraTests(CulebraTestCase):

    @classmethod
    def setUpClass(cls):
        cls.kwargs1 = {'ignoreversioncheck': False, 'verbose': False, 'ignoresecuredevice': False}
        cls.kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True, 'autodump': False, 'debug': {}, 'startviewserver': True, 'compresseddump': True}
        cls.options = {'start-activity': None, 'concertina': False, 'device-art': None, 'use-jar': False, 'multi-device': False, 'unit-test-class': True, 'save-screenshot': None, 'use-dictionary': False, 'glare': False, 'dictionary-keys-from': 'id', 'scale': 1, 'find-views-with-content-description': True, 'window': -1, 'orientation-locked': None, 'concertina-config': None, 'save-view-screenshots': None, 'find-views-by-id': True, 'log-actions': False, 'use-regexps': False, 'null-back-end': False, 'auto-regexps': None, 'do-not-verify-screen-dump': True, 'verbose-comments': False, 'gui': True, 'find-views-with-text': True, 'prepend-to-sys-path': True, 'install-apk': None, 'drop-shadow': False, 'output': 'viber_autoreg.py', 'unit-test-method': None, 'interactive': False}
        cls.sleep = 7

    def setUp(self):
        super(CulebraTests, self).setUp()

    def tearDown(self):
        super(CulebraTests, self).tearDown()

    def preconditions(self):
        if not super(CulebraTests, self).preconditions():
            return False
        return True

    def testSomething(self):
        if not self.preconditions():
            self.fail('Preconditions failed')

        _s = CulebraTests.sleep
        _v = CulebraTests.verbose

        self.vc.dump(window=-1)
        self.vc.findViewWithContentDescriptionOrRaise(u'Viber').touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Continue').touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Continue').touch()
        self.vc.sleep(_s)

        sms_activator = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key=56bfe0d6bc9000edefc2AA7400ed8820\",\"&action=getNumber&service=vi&operator=any")
        print("sms activator response is : " + sms_activator.text)
        nothing, transaction, phone = sms_activator.text.split(":")

        print("the phone is " + phone)
        print("the transaction is " + transaction)

        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Phone number').setText(phone[1:])
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Continue').touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'OK').touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)

        sms_request_url = "https://sms-activate.ru/stubs/handler_api.php?api_key=56bfe0d6bc9000edefc2AA7400ed8820&action=getStatus&id=" + transaction
        print(sms_request_url)
        sms_code_request = requests.get(sms_request_url)

        while sms_code_request.text == 'STATUS_WAIT_CODE':
            print(sms_code_request.text)
            time.sleep(30)
            sms_code_request = requests.get(sms_request_url)
        
        nothing, sms_code = sms_code_request.text.split(':')

        self.vc.findViewWithTextOrRaise(u'Enter it here').setText(sms_code)
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Enter Viber').touch()
        self.vc.sleep(_s * 2)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Enter Your name').setText(phone)
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Continue').touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'CONTACTS').touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewByIdOrRaise("com.viber.voip:id/filter_viber").touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewByIdOrRaise("com.viber.voip:id/no_id/29")
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise('Free Message').touch()


if __name__ == '__main__':
    CulebraTests.main()

