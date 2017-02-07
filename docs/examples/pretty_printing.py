import mappyfile
mf = mappyfile.load("./docs/examples/before.map")
mappyfile.write(mf, "./docs/examples/after.map")