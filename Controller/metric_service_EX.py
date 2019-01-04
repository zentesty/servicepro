from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
from flask import Flask, Response
from flask import request



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
        self.app.run(port=5000)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler),methods=methods)

class Metric_Controller:
    s = Summary('reservation', 'A summary', ['instance', 'run_id', 'loop', 'packaging_level', 'quatity', 'size_epcs'])

    def __init__(self):
        start_http_server(8000)

    def create_service(self):
        print("INA")
        content = request.get_json()
        print(content)
        print(content['name'])
        print(content['endpoint'])


    def publish_metric(self):
        try:
            if(request.is_json):
                content = request.get_json()
                print(content)
                name = content['metrics']['name']
                instance = content['metrics']['instance']
                run_id = content['metrics']['run_id']

                loop = content['metrics']['run_id']
                level = content['metrics']['instance']

                for keys in content['metrics']:
                    print keys + " = " + content['metrics'][keys]

                print(content['metrics'])
                print(content['values'])

                self.s.labels('VE001', 'Run001', loop, level, 10000, '0').observe(17)

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
