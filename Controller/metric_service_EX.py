from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
from flask import Flask, Response
from flask import request
import time



class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run(host="0.0.0.0", port=5000)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler),methods=methods)

class Metric_Controller:
    s = Summary('reservation', 'A summary', ['equipment', 'my_run_id', 'loop', 'packaging_level',
                                             'quantity', 'size_epcs','call_duration', 'timestamp'])
#    s = Histogram('reservation', 'A summary', ['instance', 'my_run_id', 'loop', 'packaging_level', 'quatity', 'size_epcs'])

    def __init__(self):
        start_http_server(9222)

    def create_service(self):
        content = request.get_json()
        pass

    def publish_metric(self):
        try:
            if(request.is_json):
                content = request.get_json()
                print(content)
                name = content['metrics']['name']
                if(name == "RESERVATION"):
                    instance = content['metrics']['instance']
                    run_id = content['metrics']['run_id']

                    loop = content['metrics']['loop']
                    packaging_level = content['metrics']['packaging_level']
                    quantity = content['metrics']['quantity']
                    env_size = content['metrics']['env_size']
                    # from  Value
                    call_duration = content['values']['value']
                    value = content['values']['value']

                    self.s.labels(instance, run_id, loop, packaging_level, quantity, env_size,
                                  call_duration, int(round(time.time() * 1000))).observe(value)
                # Execute anything
        except Exception as e:
            print("Metric Service : Exception could not <publish_metric>")
            return False


def action_srv():
    # print(request.is_json)
    content = request.get_json()
    print(content)
    print(content['name'])
    print(content['id'])
    # Execute anything


if __name__ == '__main__':
    a = FlaskAppWrapper('wrapA')

#    a.add_endpoint(endpoint='/ad', endpoint_name='ad', handler=action)
    metric = Metric_Controller()
    a.add_endpoint(endpoint='/create', endpoint_name='create', handler= metric.create_service,methods=['POST'])
    a.add_endpoint(endpoint='/publish', endpoint_name='publish', handler= metric.publish_metric,methods=['POST'])
    a.add_endpoint(endpoint='/ad', endpoint_name='ad', handler=action_srv)
    a.run()
