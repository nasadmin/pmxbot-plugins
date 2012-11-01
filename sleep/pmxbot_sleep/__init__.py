# -*- coding: utf-8 -*-
import pmxbot
from pmxbot.core import command
import random

@command("sleep", aliases=(), doc="Sleep enforcer for Coders beyond their useful amount of time to code")
def sleep(client, event, channel, nick, rest):
    sleep = 'uses the banhammer to put WHO to sleep for the next 12 hours'

    if rest:
        target = rest
    else:
        target = "the room"

    response = sleep.replace("WHO",target)
    return response
