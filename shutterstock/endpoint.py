from collections import OrderedDict


class EndPointParam:
    def __init__(self, vtype=str, default=None, help_text=None, required=False):
        self.name = 'param'
        self.data_type = vtype
        self.default = default
        self.help_text = help_text
        self.required = required


class ChoicesParam(EndPointParam):
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices


class EndpointMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        print('__prepare__ meta')
        return OrderedDict()

    def __new__(mcs, clsname, bases, clsdict):
        clsdict['params'] = []
        for name, val in clsdict.items():
            if isinstance(val, EndPointParam):
                clsdict[name].name = name
                clsdict['params'].append(val)

        clsobj = super().__new__(mcs, clsname, bases, dict(clsdict))
        return clsobj


class EndPoint(metaclass=EndpointMeta):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def format(self, **params):
        return self.endpoint.format(**params)

    def explain(self):
        return "URL: {endpoint}\n\nDescription: {doc}\n\nParams:\n{params}".format(
            endpoint=self.endpoint,
            doc=self.__doc__,
            params="\n".join(
                [
                    '{name}: {help_text}'.format(
                        name=param.name,
                        help_text=param.help_text
                    )
                    for param in self.params
                ]
            )
        )
