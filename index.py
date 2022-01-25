import ovh
import time
import requests
# Visit 
# https://eu.api.ovh.com/createToken/ - for EU region
# https://ca.api.ovh.com/createToken/ - for CA region
# https://api.ovh.com/createToken/ - for US region
# to get your credentials
#
# Permissions Required:
# /ip
# /ip/*


client = ovh.Client(
    endpoint='',
    application_key='',
    application_secret='',
    consumer_key='',
)

WEBHOOK = ''


ipInMitigation = []

while True:
    ips = client.get('/ip')
    for ip in ips:
        if len(ip.split(':')) == 0: # If the ip is not a v6 address (ik its a shitty way to detect ipv6)
            ip = ip.split('/')[0]
            print(f'Checking {ip}')
            try:
                data = client.get(f'/ip/{ip}/mitigation/{ip}')
                print(f'{ip} is being ddosed')
                if data['auto'] or data['permanent']:
                    if ip not in ipInMitigation:
                        ipInMitigation.append(ip)
                        requests.post(WEBHOOK, json={'content': f'{ip} is in mitigation mode'})
            except ovh.exceptions.ResourceNotFoundError:
                print(f'{ip} is not being ddosed')
                if ip in ipInMitigation:
                    ipInMitigation.remove(ip)
                    requests.post(WEBHOOK, json={'content': f'{ip} is out of mitigation mode'})
                pass 
    print('Sleeping for 30 seconds')
    time.sleep(30) # every 30 seconds