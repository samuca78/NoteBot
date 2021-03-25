# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

from datetime import datetime

from speedtest import Speedtest
from telethon import functions

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.speed$")
async def speedtst(spd):
    """ For .speed command, use SpeedTest to check server speeds. """
    await spd.edit("`Executando teste de velocidade . . .`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    await spd.edit(
        "`"
        "Início em "
        f"{result['timestamp']} \n\n"
        "Download "
        f"{speed_convert(result['download'])} \n"
        "Upload "
        f"{speed_convert(result['upload'])} \n"
        "Ping "
        f"{result['ping']} \n"
        "ISP "
        f"{result['client']['isp']}"
        "`"
    )


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern=r"^\.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(
        f"País : `{result.country}`\n"
        f"Datacenter mais próximo : `{result.nearest_dc}`\n"
        f"Este Datacenter : `{result.this_dc}`"
    )


@register(outgoing=True, pattern=r"^\.ping$")
async def pingme(event):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await event.edit("**Pong!**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await event.edit("**Pong!\n%sms**" % (duration))


CMD_HELP.update(
    {
        "speed": ">`.speed`" "\n**Uso:** Faz um teste de velocidade e mostra os resultados.",
        "dc": ">`.dc`" "\n**Uso:** Encontra o datacenter mais próximo de seu servidor.",
        "ping": ">`.ping`" "\n**Uso:** Mostra quanto tempo leva para pingar seu bot.",
    }
)
