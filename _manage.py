#!/usr/bin/env python
import os
import sys

import asyncio

async def hello():
    while True:
        print('Hello ...')
        await asyncio.sleep(1)
        print('... World!')

async def main():

    if __name__ == '__main__':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arduino_django.settings')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)

#asyncio.run(main())
#asyncio.run(hello())


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()