# -*- coding: utf-8 -*-
import socket
import dns.resolver
import time

import pmxbot
from pmxbot.core import command

@command("dig", aliases=('host',), doc="query DNS records")
def dig(client, event, channel, nick, rest):
    if rest:
        record_types = ['A','CNAME','MX','NS']
        for t in record_types:
            try:
                rdata = dns.resolver.query(rest,t)
            except dns.resolver.NXDOMAIN:
                    yield("Domain %s does not appear to exist" % rest)
                    break
            except dns.resolver.NoAnswer:
                    yield("No %s records found for %s" % (t, rest))
                    continue
            for entry in rdata.rrset.to_text().split('\n'):
                yield(entry)
                time.sleep(.5)
    else:
        yield("You must specify a FQDN to query (without the protocol)")
