#!python
#
# pretty print a MUD file into readable documentation.
#

import json
import sys

def domudpp(mudfile):
    mudmeta = mudfile["ietf-mud:mud"]
    fromacls=mudmeta["from-device-policy"]["access-lists"]["access-list"]
    toacls=mudmeta["to-device-policy"]["access-lists"]["access-list"]
    res = ''
    referenced = {}
    for a in fromacls:
        referenced[a["name"]] = "from"
    for a in toacls:
        referenced[a["name"]] = "to"
    pprint="<html><body>" + \
        '<br>The following access controls are recommended for the device:</br>'
    acls=mudfile["ietf-access-control-list:acls"]["acl"]

    for a in acls:
        if not a["name"] in referenced:
            print("unreferenced ACL " + a["name"])
            continue
        direction=referenced[a["name"]]
        if a['type'] == "ipv6-acl-type":
            acltype="IPv6"
        else:
            acltype="IPv4"

        for ace in a["aces"]["ace"]:
            pprint=pprint + "<br>Allow " + acltype + " "
            match=ace["matches"]
            if "ietf-mud:mud" in match:
                mudarr=match["ietf-mud:mud"]
                if "my-controller" in mudarr:
                    theotherend="<b>controllers</b> for devices with this MUD-URL"
                if "same-manufacturer" in mudarr:
                    theotherend="all devices built by the <b>same manufacturer</b>"
                if "manufacturer" in mudarr:
                    theotherend="all devices with MUD-URLs that contain <b>" + mudarr['manufacturer'] + "</b>"
                if "controller" in mudarr:
                    theotherend="all devices that are members of the class <b>" + mudarr['controller'] + "</b>"
                if "local-networks" in mudarr:
                    theotherend="all devices connected to the <b>local network</b>"
            iparr=None
            if "ipv4" in match:
                iparr=match["ipv4"]
            if "ipv6" in match:
                iparr=match["ipv6"]

            if not iparr == None:
                if "ietf-acldns:src-dnsname" in iparr:
                    theotherend="host <b>" + iparr["ietf-acldns:src-dnsname"] + "</b>"
                if "ietf-acldns:dst-dnsname" in iparr:
                    theotherend="host <b>" + iparr["ietf-acldns:dst-dnsname"] + "</b>"

            proto=None
            if "udp" in match:
                pprint = pprint + "<b>UDP</b> "
                proto=match["udp"]
            if "tcp" in match:
                pprint = pprint + "<b>TCP</b> "
                proto=match["tcp"]
            if proto == None:
                if direction == "to":
                    pprint=pprint+"from " + theotherend + " to this device"
                else:
                    pprint=pprint+"from this device to " + theotherend
            else:
                portno=None
                if "destination-port" in proto:
                    portno=proto["destination-port"]["port"]
                    if direction == "to":
                        pprint=pprint + "port <b>" + str(portno) + "</b> on this device from " + theotherend
                    else:
                        pprint=pprint + "port <b>" + str(portno) + "</b> on " + theotherend
                if "source-port" in proto:
                    portno=proto["source-port"]["port"]
                    if direction == "from":
                        pprint=pprint + "port <b>" + str(portno) + "</b> on this device from " + theotherend
                    else:
                        pprint=pprint + "port <b>" + str(portno) + "</b> on " + theotherend
                if portno == None:
                    pprint=pprint + direction + theotherend

    pprint=pprint + '</body></html>'
    return pprint

if __name__ == "__main__":
    data=sys.stdin.read()
    mudj=json.loads(data)
    output=domudpp(mudj)
    print("Content-type: text/html\n")
    print(output)
#    print("</BODY><HTML>")
