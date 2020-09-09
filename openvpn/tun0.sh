client
dev tun0
# optional
local <local ip>
pull-filter ignore redirect-gateway
# protocol may be udp or tcp based on your vpn
proto udp
remote <vpn domain> <vpn port>
route-noexec
route-up tun0.sh
lport 0
resolv-retry infinite
persist-key
persist-tun
cipher aes-128-cbc
auth sha1
tls-client
remote-cert-tls server
auth-user-pass login.conf
auth-retry interact
comp-lzo
verb 5
reneg-sec 0
crl-verify <certificate file name>
log-append tun0.log
script-security 2
ca <certificate file name>
disable-occ
