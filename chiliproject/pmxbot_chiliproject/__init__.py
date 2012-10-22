# -*- coding: utf-8 -*-
import pmxbot
from pmxbot.core import contains
import httplib2
import json
import re
import logging

log = logging.getLogger(__name__)

@contains("#")
def chiliproject(client, event, channel, nick, rest):
    if rest:
        m = re.match(".*#(?P<ticket_number>[\d]+).*", rest)
    if m == None:
        return
    if not m.group('ticket_number') or not pmxbot.config.chiliproject_apikey or not pmxbot.config.chiliproject_url:
        return
    ticket_number = m.group('ticket_number')
    apikey = pmxbot.config.chiliproject_apikey
    h = httplib2.Http(".cache")
    try:
        resp, content = h.request("%s/issues/%s.json" % (pmxbot.config.chiliproject_url, ticket_number), "GET", headers={'X-Chiliproject-API-Key': pmxbot.config.chiliproject_apikey})
    except:
        log.exception("Error retrieving ticket %s", ticket_number)
    if resp['status'] == '404':
        return
    try:
        ticket = json.loads(content)
    except ValueError:
        return ("Received invalid json from %s/issues/%s.json" % (pmxbot.config.chiliproject_url, ticket_number))
    return ("%s: %s is %s/issues/%s \"%s - %s: %s\" It's status is %s and is assigned to %s" % (nick, ticket_number, pmxbot.config.chiliproject_url, ticket_number, ticket['issue']['project']['name'], ticket['issue']['tracker']['name'], ticket['issue']['subject'], ticket['issue']['status']['name'], ticket['issue']['assigned_to']['name']))
