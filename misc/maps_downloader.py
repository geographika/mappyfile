"""
Script to download all the sample .MAP files from the MapServer GitHub repository

pip install pygithub

See
https://help.github.com/articles/creating-an-access-token-for-command-line-use/

for generating an AUTH_KEY
"""


activate_this = r'C:\VirtualEnvs\mappyfile-dev\Scripts\activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from github import Github
import os
import logging

AUTH_KEY = 'AUTH_KEY'

def get_repo():
    gh = Github(AUTH_KEY)
    org = gh.get_organization('mapserver')
    repo = org.get_repo("mapserver")


    return repo

def get_all_files(fld, repo):

    all_files = []
    print fld
    contents = repo.get_contents(fld)
    print contents

    for c in contents:

        all_files.append(c)

        if c.type == 'dir':
            all_files += get_all_files(c.path, repo)

    return all_files

def download_tests(output_folder, maps_only=True):
    """
    GithubException: 403 {u'documentation_url': u'https://developer.github.com/v3/repos/contents/#get-contents', 
    u'message': u'This API returns blobs up to 1 MB in size. The requested blob is too large to fetch via the API, but you 
    can use the Git Data API to request blobs up to 100 MB in size.', u'errors': [{u'field': u'data', u'code': u'too_large', u'resource': u'Blob'}]}
    """

    repo = get_repo()
    root_folder = "msautotest"

    all_files = get_all_files(root_folder, repo)

    if maps_only:
        files = [f for f in files if f.name.endswith(".map") and f.type == 'file']

    for fh in all_files:
        fld = os.path.join(output_folder, os.path.dirname(fh.path))

        if not os.path.isdir(fld):
            os.makedirs(fld)

        if fh.type == 'file':
            fn = os.path.join(fld, os.path.basename(fh.path))
            logging.info("Saving %s", fn)
            with open(fn, "w") as f:
                f.write(fh.decoded_content)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    output_folder = r"C:\Temp"
    download_tests(output_folder, maps_only=False)
    print("Done!")
        


