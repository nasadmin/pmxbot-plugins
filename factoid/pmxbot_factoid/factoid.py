# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import random

import pmxbot
from pmxbot.core import command
from pmxbot import storage

class Factoid(storage.SelectableStorage):

    @classmethod
    def initialize(cls):
        cls.store = cls.from_URI(pmxbot.config.database)
        cls._finalizers.append(cls.finalize)

    @classmethod
    def finalize(cls):
        del cls.store

class SQLiteFactoid(Factoid, storage.SQLiteStorage):
    def init_tables(self):
        query = "CREATE TABLE IF NOT EXISTS factoids (key varchar, factoid varchar, PRIMARY KEY (key));"
        self.db.execute(query)
        self.db.commit()

    def get_factoid(self, key):
        query = "SELECT factoid FROM factoids WHERE key = ?"
        result = self.db.execute(query, [key]).fetchall()
        if len(result) > 0:
            return result[0][0]
        else:
            return "I don't have a factoid for %s" % key

    def set_factoid(self, key, factoid):
        query = "INSERT INTO factoids (key, factoid) values (?, ?)"
        try:
           self.db.execute(query, [key, factoid])
           self.db.commit()
        except self.db.IntegrityError:
            currFactoid = self.get_factoid(key)
            return "But %s is already %s (perhaps try !factoid replace:)" % (key, currFactoid)
        return "Factoid Added!"

    def update_factoid(self, key, factoid):
        query = "INSERT OR REPLACE INTO factoids (key, factoid) values (?, ?)"
        try:
           self.db.execute(query, [key, factoid])
           self.db.commit()
        except self.db.IntegrityError:
            factoid = self.get_factoid(key)
            return "I couldn't update the factoid for %s... sorry..." % key
        return "Factoid Added!"

    def delete_factoid(self, key):
        query = "DELETE FROM factoids WHERE key =?"
        try:
           self.db.execute(query, [key])
           self.db.commit()
        except self.db.IntegrityError:
            factoid = self.get_factoid(key)
            return "Couldn't delete factoid for %s (perhaps I didn't have one...)" % (result[0], result[1])
        return "Factoid Deleted!"


@command("factoid", aliases=("f",), doc='If passed with nothing then get a '
    'random factoid. If passed with some string then return that factoid.'
    'If prepended with "add:" then add it to the db, eg "!factoid add: foo is bar'
    'If prepended with replace: then replace an existing factoid')
def FactoidCmd(client, event, channel, nick, rest):
    rest = rest.strip()
    if rest.startswith('add: '):
        cmdString = rest.split(' ', 1)[1]
        m = re.match("(?P<key>.*) is (?P<factoid>.*)", cmdString)
        if m:
            return Factoid.store.set_factoid(m.group('key').strip(), m.group('factoid').strip())
        return "Sorry, I didn't quite catch that... try !factoid add: something is something else"
    if rest.startswith('replace: '):
        cmdString = rest.split(' ', 1)[1]
        m = re.match("(?P<key>.*) is (?P<factoid>.*)", cmdString)
        if m:
            return Factoid.store.update_factoid(m.group('key').strip(), m.group('factoid').strip())
        return "Sorry, I didn't quite catch that... try !factoid replace: something is something else"
    if rest.startswith('delete: '):
        cmdString = rest.split(' ', 1)[1]
        if cmdString:
           return Factoid.store.delete_factoid(cmdString)
        else:
           return "Sorry, I didn't quite catch that... try !factoid delete: something"
    openers = ['methinks','i heard','i guess','from memory,','hmm...','rumour has it,','it has been said that','somebody said','well,','extra, extra, read all about it,']
    joiners = ['is','is probably','is, like,','was','could me','just might be']
    opener = random.sample(openers, 1)[0]
    joiner = random.sample(joiners, 1)[0]
    return "%s %s %s %s" % (opener, rest, joiner, Factoid.store.get_factoid(rest))
