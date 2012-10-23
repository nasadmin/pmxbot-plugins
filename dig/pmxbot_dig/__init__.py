# -*- coding: utf-8 -*-
import socket
import dns.resolver

import pmxbot
from pmxbot.core import command

@command("dig", aliases=('host',), doc="query DNS records")
def dig(client, event, channel, nick, rest):
    if rest:
        record_types = ['A','CNAME','MX']
        for t in record_types:
            try:
                rdata = dns.resolver.query(rest,t)
            except dns.resolver.NXDOMAIN:
                    yield("Domain %s does not appear to exist" % rest)
                    break
            except dns.resolver.NoAnswer:
                    yield("No %s records found for %s" % (t, rest))
                    continue
            yield(rdata.rrset.to_text())
    else:
        yield("You must specify a FQDN to query (without the protocol)")

