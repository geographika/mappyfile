import mappyfile

mf = mappyfile.open("./docs/examples/before.map")
mappyfile.save(mf, "./docs/examples/after.map")
