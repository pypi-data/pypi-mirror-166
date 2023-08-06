from .connects import FireStore
from .fields import FireMap, FireArray, Field
import weakref


class FireModel(FireStore, Field):
    __type_name__ = 'BaseModel'

    def __init__(self, *args, **kwargs):
        super().__init__(self)
        self.update_dict = {}
        self.__firemodel_item__ = 'FireModel'
        if hasattr(self, '__required__'):
            for attr in self.__required__:
                if attr not in kwargs:
                    raise TypeError(
                        f"{type(self).__name__}"
                        f"missing required keyword argument: '{attr}'")
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def to_dict(self):
        dict_repr = {}
        for key in self.__field_items__:
            if (self.__dict__.get(key) is None) or isinstance(
                    self.__dict__[key], type(None)):
                dict_repr[key] = None
            elif isinstance(self.__dict__[key],
                            (FireModel, FireMap, FireArray)):
                dict_repr[key] = self.__dict__[key].to_dict()
            else:
                dict_repr[key] = self.__dict__[key]
        return dict_repr

    def __del__(self):
        keys = list(self.__dict__.keys()).copy()
        for key in keys:
            if isinstance(self.__dict__[key],
                          (FireModel,
                           FireMap,
                           FireArray)):
                if hasattr(self.__dict__[key], '__path__'):
                    del self.__dict__[key].__path__['root']
                    del self.__dict__[key]

    def route_paths(self, mm: weakref = None, root_path: str = '',
                    root_object: weakref = None):
        if not mm:
            mm = weakref.ref(self)
        if not root_object:
            root_object = mm
        model_dict = {}
        if isinstance(mm(), list):
            for i, item in enumerate(mm()):
                if isinstance(item, (FireModel, FireMap, FireArray)):
                    self.route_paths(weakref.ref(item),
                                     root_path=f'{root_path}.[{i}]',
                                     root_object=root_object)
        elif isinstance(mm(), FireModel):
            model_dict = mm().__dict__
        elif isinstance(mm(), FireMap):
            model_dict = mm()
        else:
            return
        for n in model_dict:
            if isinstance(model_dict[n], (FireModel, FireMap, FireArray)):
                name = mm().__object_name__
                path = f"{root_path}.{name}.{n}".strip('..')
                model_dict[n].__path__ = {
                    'path': path,
                    'root': root_object
                }
                self.route_paths(
                    weakref.ref(model_dict[n]),
                    root_path=f"{root_path}.{name}",
                    root_object=root_object
                )
