

# Generic class for metric to be conssumed by the metric service
# A metric being described by a name, type and a series of dimensions
class Metric:

    type_of_metric = 'summary'
    name = 'GENERIC_SERVICE'
    persistance = True


    def __init__(self, name, type, persistance, dimensions):
        self.name  = name
        self.type_of_metric = type
        self.persistance = persistance
        self.dimensions = dimensions
        self.entries = []


    def create_new_entry(self, client_id, dimensions, value):
        new_entry = Metric_Entry()
        new_entry.client_id = client_id
        new_entry.dimensions = self.create_dimension_dict(dimensions)
        new_entry.value = value
        self.entries.append(new_entry)

    def create_dimension_dict(self, in_dimensions):
        dims = {}
        for inbound in in_dimensions:
            if inbound in self.dimensions:
                dims[inbound] = in_dimensions[inbound]
        return dims

    def write_to_file(self, filename):
        f = open(f"~\Temp\{filename}-{self.name}.csv", "w+")
        for metric_entry in self.entries:
            f.write(f"abc")
        f.close()



    def create_for_prometheus(self):
        pass


class Metric_Entry:
    client_id = None
    value = None

    def __init__(self):
        self.dimensions = {}
        pass
