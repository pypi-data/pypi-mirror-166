from .decoradores import Singleton

@Singleton
class DataObserver:
    """
        Una clase de observacion de datos. Se necesita para poder transferir datos a funciones lambda y sacar informacion del proceso facilmente.
    """    
    def set(self, key, val):
        setattr(self, key, val)
        
    def get(self, key):
        return getattr(self, key)
      
    def rem(self, key):
        delattr(self, key)