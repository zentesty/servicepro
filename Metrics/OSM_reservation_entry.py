from Metrics.metric import Metric_Entry

class Reservation_Entry(Metric_Entry):
    loop = None
    packaging_level = None
    quantity = None

    call_duration = None
    time_stamp = None

    value = None
    dimension_dict = {}

    def __init__(self, ):
        pass

    def publish(self):
        pass

'''
                name = content['metrics']['name']
                if(name == "RESERVATION"):
                    instance = content['metrics']['instance']
                    run_id = content['metrics']['run_id']
                    loop = content['metrics']['loop']
                    packaging_level = content['metrics']['packaging_level']
                    quantity = content['metrics']['quantity']
                    # from  Value
                    call_duration = content['values']['value']
                    value = content['values']['value']
                    '''