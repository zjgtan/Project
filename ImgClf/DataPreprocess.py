import json
import os

fd = open("kernel.dat", "w")

for name in os.listdir("./kernel"):
	if not name.endswith("txt"):
		continue

	data = ""
	label = int(name.split("_")[0])
	id = int(name.split("_")[-1].rstrip().split(".")[0])
	data += "{},{}".format(id, label)
	for i, line in enumerate(file("./kernel/"+name), start=1):
		data += ",{}".format(float(line))

	print >>fd, data

fd.close()
