CACHE_TTL = 60*60*24

def cached_property(func):

	@wraps(func)
	def fget(self):
		cache_key = hash('%s.%s.%s(%s)' %(self.__class__.__module__,self.__class__.__name__,func.__name__,self.pk))
		val = cache.get(cache_key)
		if val is None:
			val = func(self)
			cache.set(cache_key,val,CACHE_TTL)
		return val

	@wraps(func)
	def fset(self,new_val):
		cache_key = hash('%s.%s.%s(%s)' %(self.__class__.__module__,self.__class__.__name__,func.__name__,self.pk))
		cache.set(cache_key,new_val,CACHE_TTL)

	@wraps(func)
	def fdel(self):
		cache_key = hash('%s.%s.%s(%s)' %(self.__class__.__module__,self.__class__.__name__,func.__name__,self.pk))
		cache.delete(cache_key)

	return property(fget,fset,fdel)