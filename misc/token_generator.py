from mappyfile.tokens import COMPLEX_TYPES, SINGLETON_COMPOSITE_NAMES

values = list(COMPLEX_TYPES) + list(SINGLETON_COMPOSITE_NAMES)
values = list(map(str.upper, values))
print("|".join(sorted(set(values))))
