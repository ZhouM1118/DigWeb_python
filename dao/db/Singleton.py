class Singleton(object):
	"""单例模式，实现__new__方法
	并在将一个类的实例绑定到类变量_instance上,
    如果self._instance为None说明该类还没有实例化过,实例化该类,并返回
    如果self._instance不为None,直接返回self._instance
	"""
	def __new__(self, *args, **kw):
		if not hasattr(self, '_instance'):
			instance = super(Singleton, self)
			self._instance = instance.__new__(self, *args, **kw)
		return self._instance