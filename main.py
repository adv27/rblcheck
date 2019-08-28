from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

ENDPOINT = 'http://www.uceprotect.net/en/rblcheck.php'
WAIT_TIME = 60  # seconds


def get_phantomjs_path():
    import platform

    system = platform.system()
    if system == 'Windows':
        return './drivers/windows/phantomjs.exe'
    if system == 'Linux':
        return './drivers/linux/phantomjs'

    return 'phantomjs'


def get_ip_list(f_name='data.txt'):
    ip_list = []
    with open(f_name, 'r') as file:
        for line in file:
            ip_list.append(line.rstrip('\n'))
    return ip_list


def save_result(ip, status, listing_risk):
    with open('results.txt', 'a+') as file:
        file.write('{} | {} | {}\n'.format(ip, status, listing_risk))


def crawler(ip_address, webdriver):
    if not ip_address:
        return

    webdriver.get(ENDPOINT)

    ip_address_field = webdriver.find_element_by_name('ipr')
    ip_address_field.click()
    ip_address_field.send_keys(ip_address)
    submit_btn = webdriver.find_element_by_name('testform')
    submit_btn.submit()

    # wait until form sent
    try:
        element = WebDriverWait(webdriver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'db')))
    except TimeoutException:
        webdriver.save_screenshot('img/{}_error.png'.format(ip_address))
    finally:
        pass

    filename = 'img/{}_result.png'.format(ip_address)
    sss = webdriver.save_screenshot(filename)
    if sss:
        print('Success save result image to: {}'.format(filename))
    else:
        print('Failed to save result image!')
    soup = BeautifulSoup(webdriver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'db'})
    row = table.find_all('tr')[1]
    cols = row.find_all('td')
    ip = cols[0].get_text().strip()
    status = cols[1].get_text().strip()
    listing_risk = cols[2].get_text().strip()
    return (ip, status, listing_risk)


def main():
    ip_list = get_ip_list()
    webdriver = PhantomJS(executable_path=get_phantomjs_path())
    for ip_address in ip_list:
        print('='*30)
        print('Checking: {}'.format(ip_address))
        ip, status, listing_risk = crawler(ip_address, webdriver)
        print('{} | {} | {}'.format(ip, status, listing_risk))
        print('='*30)
        save_result(ip, status, listing_risk)
        # wait
        print('\nWait {} seconds until next!\n'.format(WAIT_TIME))
        sleep(WAIT_TIME)


if __name__ == '__main__':
    main()
