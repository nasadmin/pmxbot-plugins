# -*- coding: utf-8 -*-
import socket
import dns.resolver

import pmxbot
from pmxbot.core import command

@command("dig", aliases=('host',), doc="query DNS records")
def dig(client, event, channel, nick, rest):
    if rest:
        record_types = ['A','CNAME','MX']
        results = []
        for t in record_types:
            rdata = dns.resolver.query(rest,t,raise_on_no_answer=False)
            if type(rdata.rrset) == type(None):
                continue
            else:
                results.append(rdata.rrset.to_text())
        if len(results) == 0:
            yield("No records found for: %s" % rest)
        else:
            for res in results:
                yield(res)
    else:
        yield("You must specify a FQDN to query (without the protocol)")

