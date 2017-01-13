"""
Script to download all the sample .MAP files from the MapServer GitHub repository

pip install pygithub

See
https://help.github.com/articles/creating-an-access-token-for-command-line-use/

for generating an AUTH_KEY
"""

from github import Github
import os

AUTH_KEY = 'AUTH_KEY'

gh = Github(AUTH_KEY)
org = gh.get_organization('mapserver')
repo = org.get_repo("mapserver")
contents = repo.get_contents("msautotest")

subfolders = [c for c in contents if c.type == 'dir']

map_files = []
output_folder = "sample_maps"

for sf in subfolders:
    files = repo.get_contents(sf.path)
    map_files += [f for f in files if f.name.endswith(".map")
                      and f.type == 'file']
   
for mf in map_files:
    of = os.path.join(output_folder, os.path.basename(mf.path))
    print("Saving %s" % of)
    with open(of, "w") as f:
        f.write(mf.decoded_content)

print("Done!")
        


