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


class Singleton(type):
	"""Classic Singleton Object metaclass. It will create an instance the first time it is called, and then return it all the other times."""

	_instance = None

	def __call__(cls, *args, **kwargs):
		if cls._instance == None:
			cls._instance = super().__call__(*args, **kwargs)
		return cls._instance
