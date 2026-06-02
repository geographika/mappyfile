import mappyfile
import mappyfile.yaml

d = mappyfile.open("./docs/examples/before.map")
output = mappyfile.dumps(d)

# Save to YAML
mappyfile.yaml.save(d, "output.yaml")

# Load back
d2 = mappyfile.yaml.open("output.yaml")
output2 = mappyfile.dumps(d2)

print(output == output2)
print(output2)
