from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
from flask import Flask, Response
from flask import request
from Metrics.metric import Metric
import time
import sys



class EndpointAction(object):
    IN_PORT = 5000
    OUT_PORT = 9222

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class ServiceAppWrapper(object):
    app = None
    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        # Start the process binded to the default adpater on inbound port
        self.app.run(host="0.0.0.0", port=EndpointAction.IN_PORT)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler),methods=methods)


#########################################################################
##  Class Metric_Controller is responsible for accepting REST calls
##          and invoking the propoer objects
##
class Metric_Controller:
    s = Summary('osm_reservation', 'A summary', ['equipment', 'my_run_id', 'loop', 'packaging_level',
                                             'quantity', 'size_epcs','call_duration', 'timestamp'])
#    s = Histogram('reservation', 'A summary', ['instance', 'my_run_id', 'loop', 'packaging_level', 'quatity', 'size_epcs'])

    def __init__(self):
        self.metric_list = []
        start_http_server(EndpointAction.OUT_PORT)


    ## Create a generic service
    def srv_create_service(self):
        try:
            if(request.is_json):
                content = request.get_json()
                print(content)
                name = content['metric']['name']
                ## Check if the service already exists and return in such case
                if self.check_if_metric_already_exists(name):
                    print(f"Metric NAME={name} already exists")
                    return
                ## Now that we know the service does not exists we extract all the mandatory and
                ## optional fields in order to create the service
                type = content['metric']['type']
                persistance = content['metric']['persistance']
                ## extract all required metrics
                in_dimensions = content['dimensions']
                dimensions = []
                for dimension in in_dimensions:
                    dimensions.append(dimension)
                ## At this point since the service doe not already exist it gets created
                new_metric = Metric(name, type, persistance, dimensions)
                ## get added to the object metric list
                self.metric_list.append(new_metric)
                ## -----------------------------
                print("---->>> METRIC CREATED")
        except Exception as e:
            print("Metric Service : Exception could not <srv_create_service>")
            return False

    def check_if_metric_already_exists(self, name):
        for metric_object in self.metric_list:
            if metric_object.name == name: return True
        return False


    def srv_publish(self):
        try:
            if(request.is_json):
                content = request.get_json()
                print(content)
                name = content['name']
                client_id = content['client_id']
                metric_object = self.get_metric_from_name(name)
                if(metric_object):
                    dimensions = content['dimensions']
                    values = content['values']['value']
                    metric_object.create_new_entry(client_id, dimensions, values)
                    print("---->>> METRIC PUBLISHED")
                else:
                    print("---->>> METRIC NOT NOT NOT NOT PUBLISHED")
        except Exception as e:
            print("Metric Service : Exception could not <srv_publish>")
            return False

    def srv_dump_to_file(self):
        try:
            filename = request.args.get('prefix')
            for metric_object in self.metric_list:
                metric_object.write_to_file()

        except Exception as e:
            print("Metric Service : Exception could not <publish_metric>")
            return False


    def get_metric_from_name(self, name):
        for metric_object in self.metric_list:
            if metric_object.name == name: return metric_object
        return False

    #########################################################
    ## Temporary implementation
    #########################################################

    def publish_metric_reserve(self):
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
    print(sys.argv)

    ## accept port configuration from command line or assume defaults
    for param in sys.argv:
        if(param.startswith("in_port=")):
            ret = param.split("=")[1]
            if ret.isdigit():
                ret = int(ret)
                if(ret > 0 and ret < 65535): EndpointAction.IN_PORT = ret
        if(param.startswith("out_port=")):
            ret = param.split("=")[1]
            if ret.isdigit():
                ret = int(ret)
                if(ret > 0 and ret < 65535): EndpointAction.OUT_PORT = ret

    a = ServiceAppWrapper('MetricService')
    srv_controller = Metric_Controller()

    ## Create the REST endpoints of the exposed services
    a.add_endpoint(endpoint='/create', endpoint_name='create', handler= srv_controller.srv_create_service, methods=['POST'])
    a.add_endpoint(endpoint='/publish', endpoint_name='publish', handler= srv_controller.srv_publish, methods=['POST'])
    a.add_endpoint(endpoint='/dump', endpoint_name='dump', handler= srv_controller.srv_dump_to_file, methods=['GET'])
    ##
    ## TEMPORARY SERVICE
    a.add_endpoint(endpoint='/publish_reserve', endpoint_name='publish_reserve',
                   handler= srv_controller.publish_metric_reserve, methods=['POST'])
    a.add_endpoint(endpoint='/ad', endpoint_name='ad', handler=action_srv)
    a.run()
