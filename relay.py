#!/usr/bin/python3

import sys
import logging
from collections import deque

import asyncio
from aiosmtpd.controller import UnthreadedController as Controller
from signal import SIGINT, SIGTERM

from src.config import load_config


logging.basicConfig(encoding='utf-8', format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

logger = logging.getLogger(f"relay.{__name__}")


def help(retcode: int = 0) :
    print(f"usage: {sys.argv[0]} [--conf <conf_path>]")
    sys.exit(retcode)


def on_exit(controller: Controller):
    logger.info('Stopping')
    controller.loop.create_task(controller.finalize()).add_done_callback(lambda _: controller.loop.stop())

def main():

    args = deque(sys.argv[1:])

    if len(args) > 0 and args[0] in ['-h', '--help'] :
        help()
    
    conf_path = 'config.yml'
    if len(args) > 1 and args[0] == '--conf' :
        args.popleft()
        conf_path = args.popleft()
    
    if len(args) > 0 :
        help(1)

    conf = load_config(conf_path)

    logger.info("Server starting, listening on %s:%i", conf.smtp_host, conf.smtp_port)

    loop = asyncio.new_event_loop()
    controller = Controller(conf.handler, loop=loop, hostname=conf.smtp_host, port=conf.smtp_port)
    controller.begin()

    for sig in [SIGINT, SIGTERM] :
        loop.add_signal_handler(sig, on_exit, controller)

    loop.run_forever()

    logger.info('Stopped')
    


if __name__ == '__main__' :
    main()
