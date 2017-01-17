from datetime import datetime as dt
import os
import time

import boto
import boto.s3.connection


access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
)


bucket = conn.get_bucket('ot-app-builds')

def get_builds_by_prefix(prefix):
    return sorted(bucket.list(prefix=prefix), key=lambda k: k.last_modified)


def get_latest_builds(prefix, branch='master', lim=10):
    all_builds = get_builds_by_prefix(prefix)

    # keep builds that end with zip, exe or deb ignore dmgs, nupks, etc...
    def can_keep(build):
        return any([
            build.name.endswith(i) and (branch in build.name)
            for i in ('.zip', '.exe', '.deb')
        ])

    clean_list = filter(can_keep, all_builds)

    # return last n builds in reverse order
    return list(clean_list)[-lim:][::-1]



def get_builds_dict(branch='master'):
    prefixes = ['mac', 'win', 'linux']
    builds_dict = dict((k, []) for k in prefixes)
    url_tmpl = "https://s3.amazonaws.com/ot-app-builds/{name}"
    for prefix in prefixes:
        for i, key in enumerate(get_latest_builds(prefix, branch=branch, lim=1)):
            modified = time.strptime(key.last_modified, '%Y-%m-%dT%H:%M:%S.000Z')
            builds_dict[prefix].append({
                'index': i,
                'url': url_tmpl.format(name=key.name),
                'name': key.name.split('/')[1],
                'last_modified': dt.fromtimestamp(time.mktime(modified))
            })
            print(type(key.last_modified))
    return builds_dict


def print_latest():
    prefixes = ['mac', 'win', 'linux']
    url_tmpl = "https://s3.amazonaws.com/ot-app-builds/{name}"

    for prefix in prefixes:
        print('-' * 30, '{} BUILDS'.format(prefix.upper()), '-' * 30)
        for i, key in enumerate(get_latest_builds(prefix, lim=1)):
            print('Build #{}'.format(i + 1))
            print(url_tmpl.format(name=key.name))
            print('-' * 80)
        print('\n')

if __name__ == '__main__':
    print_latest()
