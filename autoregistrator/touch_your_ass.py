# -*- coding: utf-8 -*-
"""
Copyright (C) 2013-2018  Diego Torres Milano
Created on 2019-03-02 by Culebra v15.5.1
                      __    __    __    __
                     /  \  /  \  /  \  /  \
____________________/  __\/  __\/  __\/  __\_____________________________
___________________/  /__/  /__/  /__/  /________________________________
                   | / \   / \   / \   / \   \___
                   |/   \_/   \_/   \_/   \    o \
                                           \_____/--<
@author: Diego Torres Milano
@author: Jennifer E. Swofford (ascii art snake)
"""


import re
import sys
import os


import unittest


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
        cls.kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True, 'autodump':
False, 'debug': {}, 'startviewserver': True, 'compresseddump': True}
        cls.options = {'start-activity': None, 'concertina': False, 'device-art': None, 'use-jar': False, 'multi-device': False, 'unit-test-class': True, 'save-screenshot': None, 'use-dictionary': False, 'glare': False, 'dictionary-keys-from': 'id', 'scale': 1, 'find-views-with-content-description': True, 'window': -1, 'orientation-locked': None, 'concertina-config': None, 'save-view-screenshots': None, 'find-views-by-id': True, 'log-actions':
False, 'use-regexps': False, 'null-back-end': False, 'auto-regexps': None, 'do-not-verify-screen-dump': True, 'verbose-comments': False, 'gui': True, 'find-views-with-text': True, 'prepend-to-sys-path': True, 'install-apk': None, 'drop-shadow': False, 'output': None, 'unit-test-method': None, 'interactive': False}
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
        _v = CulebraTests.verbose

        #self.vc.dump(window=-1)
        #self.device.touchDip(305.33, 154.67, 0)
        #self.vc.sleep(_s)
        self.vc.dump(window=-1)
        self.vc.sleep(_s)
        self.vc.device.dragDip((301.33, 140.67), (143.33, 400.67), 50, 20, 0)
        #self.vc.swipe(500, 1000, 300, 300)
        #print(dir(self.vc)) #('input swipe 500 1000 300 300')
        #adb shell input swipe 500 1000 300 300 

if __name__ == '__main__':
    CulebraTests.main()

