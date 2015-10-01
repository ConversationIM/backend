from app import database as db

class BaseDao(object):
    # TODO: figure out if we should use sessions here instead
    # the model setup seems like a temporary solution

    def __init__(self, model):
        self.database = db
        self.model = model

    def get_query_builder(self):
        return self.database.session.query(self.model)

    def commit(self):
        self.database.session.commit()

    def save(self, instance):
        self.database.session.add(instance)
        self.commit()

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.save(instance)
        return instance

    def update(self, instance, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(instance, key):
                setattr(instance, key, value)
            else:
                raise KeyError("The model '%s' has no field '%s'." % (type(instance), key))

    def delete(self, instance):
        self.database.session.delete(instance)

    def find_by_id(self, id):
        return self.get_query_builder().get(id)
