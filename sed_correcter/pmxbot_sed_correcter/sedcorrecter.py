# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import logging

import pmxbot
from pmxbot.core import command, contains
from pmxbot import storage

log = logging.getLogger(__name__)

class SedCorrecter(storage.SelectableStorage):

    @classmethod
    def initialize(cls):
        cls.store = cls.from_URI(pmxbot.config.database)
        cls._finalizers.append(cls.finalize)

    @classmethod
    def finalize(cls):
        del cls.store

class SQLiteSedCorrecter(SedCorrecter, storage.SQLiteStorage):
    def init_tables(self):
        query ='CREATE INDEX IF NOT EXISTS ix_log_channel_nick_datetime ON logs (channel, nick, datetime desc)'
        self.db.execute(query)
        self.db.commit()

    def get_last_msg(self, channel, nick, hasnick):
        channel = channel.replace('#', '').lower()
        query = """
            SELECT message
            FROM logs
            WHERE channel = ?
            AND nick = ?
            ORDER BY datetime desc
            LIMIT 2"""
        result = self.db.execute(query, [channel, nick]).fetchall()
        if len(result) == 2:
            if hasnick == False:
                return result[1][0]
            else:
                return result[0][0]
        else:
            return False

@contains("s/", priority=1)
def SedCorrectCmd(client, event, channel, nick, rest):
    if rest:
        m = re.match(".*s/(?P<find>[^/]+)/(?P<replace>[^/]+)/(?P<user>[^ ]+).*", rest)
        hasnick = True
    if m == None:
        m = re.match(".*s/(?P<find>[^/]+)/(?P<replace>[^/]+)/", rest)
        hasnick = False
    if m == None:
        return
    result = False
    if hasnick:
        lastmsg = SedCorrecter.store.get_last_msg(channel, m.group('user'), hasnick)
        if lastmsg:
            result = "%s thinks %s meant: %s" % (nick, m.group('user'), lastmsg.replace(m.group('find'), m.group('replace')))
    else:
        lastmsg = SedCorrecter.store.get_last_msg(channel, nick, hasnick)
        if lastmsg:
            result = "%s meant: %s" % (nick, lastmsg.replace(m.group('find'), m.group('replace')))
    if result:
       return result
