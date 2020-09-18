# -*- coding: utf-8 -*-
import os
import time
import random
from models import UserAgent, Proxy
from peewee import fn


def text_proxy_generator():
    with open('proxy_accs.txt') as proxy_accs:
        for proxy_acc in proxy_accs:
            yield proxy_acc.rstrip('\n')


def proxy_generator():
    for proxy_acc in Proxy.select().where(Proxy.used == False):
        proxy_acc.used = True
        proxy_acc.save()
        yield proxy_acc.host_port


def random_user_agent_generator():
    return UserAgent.select().order_by(fn.Random())
    #return 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


def account_generator():
    with open('vk_accounts.txt') as vk_accs:
        for vk_acc in vk_accs:
            vk_email, vk_pass = vk_acc.split(':')
            yield vk_email, vk_pass.rstrip('\n')


if __name__ == "__main__":
    for i in proxy_generator():
        bash_command = "casperjs casperas.js --proxy=" + i
        print "--------------new casper command : " + bash_command
        os.system(bash_command)
        random_secs = random.randint(3,30)
        print "---------------------sleep for " + str(random_secs)
        time.sleep(random_secs)
