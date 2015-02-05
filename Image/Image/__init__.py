
_Modules = []
for name in os.listdir(os.path.dirname(__file__)):
	if not name.startswith("_") and name.endswith(".py"):
			name = "." + os.path.splitext(name)[0]
			try:
				module = importlib.import_module(name, "Image")
				_Modules.append(module)
			except ImportError as err:
				warning.warn("failed to load Image module: {}".format(err))

del name, module
