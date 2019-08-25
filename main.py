from time import sleep

from bs4 import BeautifulSoup
from requests import Session

ENPOINT = 'http://www.uceprotect.net/en/rblcheck.php'
WAIT_TIME = 60  # seconds

session = Session()
session.headers.update(
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})


def get_ip_list(f_name='data.txt'):
    ip_list = []
    with open(f_name, 'r') as file:
        for line in file:
            ip_list.append(line.rstrip('\n'))
    return ip_list


def save_result(ip, status, listing_risk):
    with open('results.txt', 'a+') as file:
        file.write('{} | {} | {}\n'.format(ip, status, listing_risk))


def get_subchannel():
    r = session.get(ENPOINT)
    soup = BeautifulSoup(r.content, 'html.parser')
    subchannel_input = soup.find('input', {'name': 'subchannel'})
    subchannel = subchannel_input.get('value')
    return subchannel


def crawler(ip_address):
    if not ip_address:
        return
    subchannel = get_subchannel()
    data = {
        'whattocheck': 'IP',
        'ipr': ip_address,
        'subchannel': subchannel,
    }
    r = session.post(ENPOINT, data=data)
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
        print('='*30)
        print('Checking: {}'.format(ip_address))
        ip, status, listing_risk = crawler(ip_address)
        print('{} | {} | {}'.format(ip, status, listing_risk))
        print('='*30)
        save_result(ip, status, listing_risk)
        # wait
        print('\nWait {} seconds until next!\n'.format(WAIT_TIME))
        sleep(WAIT_TIME)


if __name__ == '__main__':
    main()
