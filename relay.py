#!/usr/bin/python3

import asyncio
from aiosmtpd.controller import UnthreadedController as Controller
from signal import SIGINT, SIGTERM

from src.config import load_config



def on_exit(controller: Controller):
    print('Stopping')
    controller.loop.create_task(controller.finalize()).add_done_callback(lambda _: controller.loop.stop())

def main():
    conf = load_config('config.yml')

    loop = asyncio.new_event_loop()

    controller = Controller(conf.handler, loop=loop, port=conf.smtp_port)
    controller.begin()

    for sig in [SIGINT, SIGTERM] :
        loop.add_signal_handler(sig, on_exit, controller)

    loop.run_forever()

    print('Stopped')
    


if __name__ == '__main__' :
    main()
