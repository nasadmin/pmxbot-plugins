# -*- coding: utf-8 -*-
import socket
import dns.resolver

import pmxbot
from pmxbot.core import command

@command("dig", aliases=('host',), doc="query DNS records")
def dig(client, event, channel, nick, rest):
    if rest:
        target = rest
    else:
        yield("You must specify a URL to query")
        continue

    record_types = ['A','CNAME','MX']
    for t in record_types:
        rdata = dns.resolver.query('cryptkcoding.com',t,raise_on_no_answer=False)
        if type(rdata.rrset) == type(None):
            continue
        else:
            yield(rdata.rrset.to_text())

