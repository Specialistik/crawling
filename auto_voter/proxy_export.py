from models import Proxy
from main_proxy import text_proxy_generator

for proxy in text_proxy_generator():
    proxy = Proxy(host_port=proxy)
    proxy.save()
