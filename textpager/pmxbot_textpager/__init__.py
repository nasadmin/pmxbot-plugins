# -*- coding: utf-8 -*-
import pmxbot
from pmxbot.core import command
import smtplib
import string
import logging

log = logging.getLogger(__name__)

@command("pager", aliases=('page',), doc="Text message someone requesting their presence in the channel")
def pager(client, event, channel, nick, rest):
    args = rest.split(None, 1)
    pagee = args[0]
    if len(args) > 1:
        text = "%s in %s: %s" % (nick, channel, args[1])
    else:
        text = "You have been summoned to %s by %s" % (channel, nick)
    if channel not in pmxbot.config.textpager_channels:
        return ("I'm sorry %s, but this is restricted to certain channels" % nick)
    if not rest:
        return ("%s: You have to tell me who to page" % nick)
    for target in pmxbot.config.textpager_users:
        if pagee == target.keys()[0]:
            HOST = "localhost"
            TO = target[pagee]
            FROM = "nas-bot@cryptkcoding.com"
            BODY = string.join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "",
                text
                ), "\r\n")
            server = smtplib.SMTP(HOST)
            server.sendmail(FROM, [TO], BODY)
            server.quit()
