#    This file is part of MUM.
#
#    MUM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MUM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MUM.  If not, see <http://www.gnu.org/licenses/>.
import inspect
from collections import OrderedDict


class NoDuplicates(type):
	"""This class extends the concept of Singleton. Classes with NoDuplicates as metaclass will create new instances everytime they are called with new 
	argument values, but if they are called more than once with the same parameters, they will return the same instance of the first time."""
	
	_instances = {}
	
	def _make_hashable(cls, arguments: OrderedDict):
		arguments["kwargs"] = tuple(sorted(arguments["kwargs"].items(), key = lambda pair: pair[0]))
	
	def __call__(cls, *args, **kwargs):

		#we build a tuple of pairs from kwargs and we sort it on the key names:
		kwargs_pairs = tuple(sorted(kwargs.items(), key = lambda pair: pair[0]))
		
		#now we store create an instance_key:
		instance_key = (cls, args, kwargs_pairs)
		
#		print(instance_key)
		
		#if instance_key is not in _instances, we create the corresponding instance and store it in the dictionary:
		if instance_key not in cls.__class__._instances.keys():
			cls.__class__._instances[instance_key] = super().__call__(*args, **kwargs)
		
		#finally we return the instance in _instances:
		return cls.__class__._instances[instance_key]

if __name__ == "__main__":

	class NDClass(metaclass=NoDuplicates):

		def __init__(self, arg1, arg2, *args, **kwargs):
			pass

	instance1 = NDClass(1, 2)
	instance1 = NDClass(arg1=1, arg2=2)
