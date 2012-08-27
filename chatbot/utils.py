from importlib import import_module

def import_class(string_path):
	bits = string_path.rpartition('.')
	module = import_module(bits[0])
	return getattr(module, bits[2])