from prometheus_client import Gauge,start_http_server
from time import sleep
import pycurl
from io import BytesIO
from urllib.parse import urlencode
import threading

table_number_rows = Gauge(
    "table_number_rows", 
    "Number of rows in the requested table", 
    ['table_name','shard_number', 'replica_name']
    )



def curl_request(url, auth, params):
    params = {f'{params[0]}': f'{params[1]}'}
    buffer_curl = BytesIO()
    application_curl = pycurl.Curl()
    application_curl.setopt(application_curl.URL, url + '?' + urlencode(params))
    application_curl.setopt(application_curl.USERPWD, f'{auth[0]}:{auth[1]}')
    application_curl.setopt(application_curl.WRITEDATA, buffer_curl)
    application_curl.perform() 
    application_curl.close()
    get_body = buffer_curl.getvalue()
    return(get_body.decode('utf8'))



def gauge_metric(value, table, shard_number, replica_name):
    if type(value) != int and not value.isdigit():
        raise Exception('Only integer, please!')
    else:
        int(value)

    table_number_rows.labels(
        f'{table}', 
        f'{shard_number}', 
        f'{replica_name}').set(value)



# Управление потоком, выполнять curl url каждые 15 секунд
def gauge_threads(replica, auth, database, table):
    while True:
        row_value = curl_request(
               f'http://{replica[1]}:{replica[2]}/', 
                auth, 
                ("query", f"""
                SELECT log_max_index FROM system.replicas 
                WHERE (database = '{database}' and table = '{table}') 
                FORMAT Vertical
                """ )
                )
        finish_value = int(row_value.split(":")[-1].strip())

        t = threading.Thread(target=gauge_metric,args=(
            finish_value, 
            table, 
            replica[0], 
            replica[1]))
        t.setDaemon(True)
        t.start()
        sleep(15)



if __name__ == '__main__':
    start_http_server(9091)
    credentials = ('default', 'EZxoDNmAXKcAFbq2fza4Z25R')
    database = 'test_metrics'
    table = 'calc_success_request'
    table_list = ['calc_success_request', 'calc_error_request']
    replica_list = [
            (1, 'click-znmp1-rep1.innoseti.ru', 8123),
            (2, 'click-znmp2-rep2.innoseti.ru', 8124),
            (2, 'click-znmp2-rep1.innoseti.ru', 8123),
            (3, 'click-znmp3-rep2.innoseti.ru', 8124),
            (3, 'click-znmp3-rep1.innoseti.ru', 8123),
            (1, 'click-znmp1-rep2.innoseti.ru', 8124)
            ]
    threads = []
    for table in table_list:
        for replica in replica_list:
            t = threading.Thread(target=gauge_threads,args=(
                replica, credentials, database, table))
            threads.append(t)
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
    thread.join()
