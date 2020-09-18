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
        cls.sleep = 5

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

        """
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise("+79002548344").touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise('Free Message').touch()
        self.vc.sleep(_s)
        """
        text_to_type = u'le privet девочка'
        self.vc.dump(window=-1)
        self.vc.findViewWithTextOrRaise(u'Type to compose').setText(u"сосисочка kurwa")
        self.vc.sleep(_s)

        """
        self.vc.dump(window=-1)
        self.vc.findViewByIdOrRaise("com.viber.voip:id/btn_send_extra").touch()
        self.vc.sleep(_s)
        self.vc.dump(window=-1)
        """

if __name__ == '__main__':
    CulebraTests.main()

