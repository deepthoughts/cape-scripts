#!/bin/sh

# This script removes the default routes added by OpenVPN
# so that the VPN tunnel may be accessed only by applications
# which are bound to the VPN interface

# Checks to see if there is an IP routing table named 'vpn', create if missing
if [ $(cat /etc/iproute2/rt_tables | grep tun0 | wc -l) -eq 0 ]; then
            echo "100     tun0" >> /etc/iproute2/rt_tables
fi

# Remove any previous routes in the 'vpn' routing table
/bin/ip rule | sed -n 's/.*\(from[ \t]*[0-9\.]*\).*tun0/\1/p' | while read RULE
do
        /bin/ip rule del ${RULE}
done

# Add routes to the vpn routing table
/bin/ip rule add from ${ifconfig_local} lookup tun0

# Add the route to direct all traffic using the the vpn routing table to the tunX interface
/bin/ip route add default via ${route_vpn_gateway} table tun0

exit 0
