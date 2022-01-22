import mappyfile
mf = mappyfile.open("./docs/examples/before.map")
mappyfile.write(mf, "./docs/examples/after.map")