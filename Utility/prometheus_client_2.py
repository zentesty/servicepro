from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
import random
import time


# Create a metric to track time spent and requests made.
# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
# @REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)

if __name__ == '__main__':
    i = 0
    # Start up the server to expose the metrics.

    # c = Counter('cc', 'Product X counter')
    # c.inc()

    # g = Gauge('gg', 'A gauge')
    # g.set(17)

    ## GOOD ONE
    plevel = ['A', 'B', 'C', 'D']
    s = Summary('reservation', 'A summary', ['instance', 'run_id' ,'loop', 'packaging_level','quatity', 'size_epcs'])
    s.labels('VE001', 'Run001', str(i), plevel[i % 4], 10000, '0'  ).observe(17)

    # h = Histogram('hh', 'A histogram')
    # h.observe(.25)

    start_http_server(8000)
    # Generate some requests.
    time.sleep(5)

    while True:
        # h.observe(random.randint(1, 10))
        # process_request(random.random())
        i += 1
        s.labels('VE001', 'Run001', str(i/4), plevel[i % 4], 10000, '0').observe(18)

        # g.set(55)
        time.sleep(1.25)