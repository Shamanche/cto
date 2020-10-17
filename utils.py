def save_to_html(html):
    with open('response.html', 'w', encoding='UTF-8') as f:
        f.write(html)

def get_soup(any_url = ''):
    print('*****get_soup*****')
    ATTEMPTS = 5
    url = BASE_URL + any_url
    print(url)
    for att in range(ATTEMPTS):
        try:
            r = requests.get(url)
        except ConnectionError:
            print ('ConnectionError, attempt: ', att)
            continue
    if r:
        soup = BeautifulSoup(r.text, 'html.parser')
        save_to_html(r.text)
    else:
        soup = ''
    return soup

def squeezed (client_name):
    return client_name.replace('Индивидуальный предприниматель', 'ИП')



