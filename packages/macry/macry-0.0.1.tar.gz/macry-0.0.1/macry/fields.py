from datetime import datetime

models_data = {}


class Field:
    def __set_name__(self, owner_cls, prop_name):
        self.prop_name = prop_name
        if not hasattr(owner_cls, '__field_items__'):
            owner_cls.__field_items__ = set()
        owner_cls.__field_items__.add(self.prop_name)

        if hasattr(owner_cls, '__data_path__'):
            data_path = owner_cls.__data_path__
            models_data[data_path] = {
                'type': owner_cls,
                'collection_type': owner_cls.__collection_type__,
                'repr_type': owner_cls.__repr_type__
            }
        if hasattr(self, 'required') and self.required:
            if '__required__' in owner_cls.__dict__:
                owner_cls.__required__.append(self.prop_name)
            else:
                owner_cls.__required__ = []

    def __set__(self, instance, value):
        if self.validate(value):
            if value is None:
                value = self.default
            instance.__dict__[self.prop_name] = value
            # --------------------------------------------------------
            if hasattr(instance, '__path__'):
                instance.__path__["root"]().update_stack.setdefault(
                    f'{instance.__path__["path"]}.{self.prop_name}', value
                )
            # --------------------------------------------------------
        else:
            if hasattr(self, 'entity') and self.entity:
                if isinstance(self.entity, list):
                    _name = [e.__name__ for e in self.entity]
                else:
                    _name = self.entity.__name__
            else:
                _name = type(self).__name__
            raise ValueError(f'{self.prop_name} must be a type: {_name}')

    def __get__(self, instance, owner_cls):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self.prop_name, None)


class FireObject(Field):
    def __init__(self, default=None, required=False):
        self._type = 'fire_object'
        self.default = default
        self.required = required

    def validate(self, value):
        if isinstance(value, (str, type(None))):
            return True
        return False


class FireString(Field):
    def __init__(self, default=None, required=False):
        self._type = 'string'
        self.default = default
        self.required = required

    def validate(self, value):
        if isinstance(value, (str, type(None))):
            return True
        return False


class FireNumber(Field):
    def __init__(self, default=None, required=False):
        self._type = 'number'
        self.default = default
        self.required = required

    def validate(self, value):
        if isinstance(value, (int, float, type(None))):
            return True
        return False


class FireBool(Field):
    def __init__(self, default: bool = type(None), required=False):
        self._type = 'boolean'
        self.default = default
        self.required = required

    def validate(self, value):
        if isinstance(value, bool):
            return True
        return False


class FireMap(Field, dict):

    def __init__(self,
                 obj_type=None,
                 default=None,
                 entity: Field = None,
                 required=False,
                 key=None):
        super().__init__()
        self._type = 'map'
        self.default = default
        self.entity = entity
        self.obj_type = obj_type
        self.required = required
        self.key = None

    def to_dict(self):
        dict_repr = {}
        for key in self:
            if hasattr(self[key], 'to_dict'):
                sub_dict = self[key].to_dict()
                dict_repr[key] = sub_dict
            else:
                dict_repr[key] = self[key]
        return dict_repr

    def validate(self, value):
        if self.entity:
            if isinstance(self.entity, list):
                if isinstance(value, (type(None), *self.entity)):
                    return True
            elif isinstance(value, (type(None), self.entity)):
                return True
        elif isinstance(value, (type(None), FireMap)):
            return True
        return False


class FireArray(Field, list):
    def __init__(self,
                 default=None,
                 entity: Field = None,
                 required=False,
                 key=None):
        super().__init__()
        self._type = 'array'
        self.default = default
        self.required = required
        self.key = None

    def to_dict(self):
        dict_repr = []
        for item in self:
            if type(item).__name__ in ('FireDict', 'FireArray') or \
               hasattr(item, '__firemodel_item__'):
                sub_dict = item.to_dict()
                dict_repr.append(sub_dict)
            else:
                dict_repr.append(item)
        return dict_repr

    def validate(self, value):
        if isinstance(value, (FireArray, type(None))):
            return True
        return False


class FireTimeStamp(Field):
    def __init__(self, default: datetime = datetime.utcnow(), required=False):
        self._type = 'datetime'
        self.default = default
        self.required = required

    def validate(self, value):
        if isinstance(value, (datetime, type(None))):
            return True
        return False


class FireDocument(Field):
    def __set__(self, owner_cls, prop_name):
        raise Exception('Not implemented!')


class FireGeopoint(Field):
    def __set__(self, owner_cls, prop_name):
        raise Exception('Not implemented!')


class FireReference(Field):
    def __set__(self, owner_cls, prop_name):
        raise Exception('Not implemented!')


class FireItems(Field):
    def __set__(self, owner_cls, prop_name):
        raise Exception('Not implemented!')
