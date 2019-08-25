from time import sleep

import requests
from bs4 import BeautifulSoup

ENPOINT = 'http://www.uceprotect.net/en/rblcheck.php'
wait_time = 60  # seconds


def get_ip_list(f_name='data.txt'):
    ip_list = []
    with open(f_name, 'r') as file:
        for line in file:
            ip_list.append(line.rstrip('\n'))
    return ip_list


def crawler(ip_address):
    if not ip_address:
        return
    data = {
        'whattocheck': 'IP',
        'ipr': ip_address,
        'subchannel': '6b583eebda3',
    }
    r = requests.post(ENPOINT, data=data)
    print(r.content)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', {'class': 'db'})
    row = table.find_all('tr')[1]
    cols = row.find_all('td')
    ip = cols[0].get_text().strip()
    status = cols[1].get_text().strip()
    listing_risk = cols[2].get_text().strip()
    return (ip, status, listing_risk)


def main():
    ip_list = get_ip_list()
    for ip_address in ip_list:
        print('Checking: {}'.format(ip_address))
        ip, status, listing_risk = crawler(ip_address)
        print('{} | {} | {}'.format(ip, status, listing_risk))
        # wait
        sleep(wait_time)


if __name__ == '__main__':
    main()
