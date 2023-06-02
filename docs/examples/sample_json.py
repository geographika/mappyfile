import mappyfile
import json

mf = mappyfile.open("./docs/examples/after.map")

with open("./docs/examples/sample.json", "w") as f:
    json.dump(mf, f, indent=4)
