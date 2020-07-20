import asyncio
import argparse
from nats.aio.client import Client as NATS
from tkinter import *

room_name = 'room1_2_3'
nats_addr = 'nats://127.0.0.1:4222'

pr = argparse.ArgumentParser()
pr.add_argument('-n', action='store', required=True, dest="my_name")
parsed_args = pr.parse_args()


async def start_gui():
    root = Tk()
    loop = asyncio.get_event_loop()

    text = Text(root, width=30)
    ent = Entry(root, width=30)

    text.pack()
    ent.pack()
    nats = NATS()

    async def add_text(msg):
        print('call')
        text.insert(END, msg.data.decode())

    await nats.connect(nats_addr, loop=loop)

    await nats.subscribe(room_name, cb=add_text)

    async def i_send(msg):
        await nats.publish(room_name, (parsed_args.my_name + " > " + msg + "\n").encode())

    def send_msg(event):
        loop.create_task(i_send(ent.get()))
        ent.delete(0, END)

    ent.bind('<Return>', send_msg)

    try:
        while True:
            root.update()
            await asyncio.sleep(.01)
    except TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


asyncio.get_event_loop().run_until_complete(start_gui())
