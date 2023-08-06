#!/usr/bin/env python3
# import os
from celery import Celery
from stem.control import Controller
import stem
import stem.process
from stem.util import term
import requests

CELERY_BROKER_STR="pyamqp://admin:feihuo321@rabbitmq//"
CELERY_REDIS_STR="redis://:feihuo321@redis"

def create_celery_app():    
    app = Celery('mainapp', 
        broker=CELERY_BROKER_STR, 
        backend=CELERY_REDIS_STR)
    return app

app = create_celery_app()



def onion_up():
    """启动tor"""
    print("------")
    SOCKS_PORT=9050
    def print_bootstrap_lines(line):
        if line and len(line) > 0:
            print(term.format("Tor:", term.Attr.BOLD), end="", flush=True)
            print(term.format(line, term.Color.BLUE), flush=True)  
    tor_process = stem.process.launch_tor_with_config(
        config = {
            'SocksPort': str(SOCKS_PORT),
            # 'ExitNodes': '{ru}',
            # 'VirtualAddrNetworkIPv4': "10.192.0.0/10",
            "AutomapHostsOnResolve": "1",
            "AvoidDiskWrites": "1",
            "SocksPort": f"0.0.0.0:{SOCKS_PORT}",
            "TransPort": "127.0.0.1:9040",
            "DNSPort": "127.0.0.1:5353",
            "CookieAuthentication":"1",
            "ControlPort": "0.0.0.0:9051",
            # "HashedControlPassword": "16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF"
        },
        init_msg_handler = print_bootstrap_lines,
    )
    print(term.format("\nTor ready \n", term.Attr.BOLD), flush=True)


def proxy_with_tor():
    """
        运行本地tor, 并让本程序访问网络时自动通过tor。
        # 功能未验证，先掠过
    """
    onion_up()
    import socket
    import socks
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

    #测试tor sockets 是否有效
    url = 'https://check.torproject.org/api/ip'
    html = requests.get(url).text
    print(html)

def main():
    # 等同celery命令行参数
    app.start(argv=["-A","celery", "worker", "-l", "INFO"])
    
if __name__ == '__main__':
    main()