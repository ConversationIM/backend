from app import database as db

class BaseDao(object):
    """
    Provides access to database operations common to
    all database objects
    """

    def __init__(self, model):
        """
        Initializes the DAO instance
        :model the model associated with the DAO instance (e.g., User)
        """
        
        self.database = db
        self.model = model

    def get_query_builder(self):
        """
        Gets the query object for the associated model, returning
        it or None
        """
        
        return self.database.session.query(self.model)

    def commit(self):
        """
        Commits the current session to the database
        """
        
        self.database.session.commit()

    def save(self, instance):
        """
        Adds the instance to the current session and 
        commits it to the database
        :instance the instance that will be added to the session
        """
         
        self.database.session.add(instance)
        self.commit()

    def create(self, **kwargs):
        """
        Creates a new instance of the associated model and saves it to the
        database, returning the persisted model
        :kwargs the arguments to use for creating a new instance
        """
        
        instance = self.model(**kwargs)
        self.save(instance)
        return instance

    def update(self, instance, **kwargs):
        """
        Updates the instance with the provided arguments but does not save it
        to the database
        :instance the instance to update
        :kwargs the arguments to use to update the instance
        """
        
        for key, value in kwargs.iteritems():
            if hasattr(instance, key):
                setattr(instance, key, value)
            else:
                raise KeyError("The model '%s' has no field '%s'." % (type(instance), key))

    def delete(self, instance):
        """
        Deletes the instance and commits this change to the database
        :instance the instance to delete
        """
        
        self.database.session.delete(instance)
        self.commit()

    def find_by_id(self, id):
        """
        Finds an instance by its ID
        :id the unique ID to use for locating an instance
        """
        
        return self.get_query_builder().get(id)
