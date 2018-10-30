#!/usr/bin/env python

import os, argparse, json, logging, time, sys

from macapi.api_base import ApiBase
from pprint import pprint
from collections import OrderedDict
from requests.auth import HTTPDigestAuth
from requests import Session

class Cluster(ApiBase):
    """creates and gets cluster configruation"""
    def __init__(self, group_id, api_user, api_key):
        super(Cluster, self).__init__(group_id, api_user, api_key)

    def get_cluster(self, group_id, *argv):
        base_url = self.base_url
        url = "{}/groups/{}/clusters/{}".format(base_url, group_id, *argv)
        data = {}
        data = self.get(url)
        keys = ['links', 'groupId', 'id',
                'mongoURI', 'mongoURIUpdated',
                'mongoURIWithOptions', 'stateName'
                ]
        details = {k:v for (k, v) in data.items() if k not in keys}
        results = {}

        # remove duplicate keys if any
        for key,value in details.items():
            if 'replicationSpecs' not in results.keys():
                results[key] = value

        json_file = json.dumps(results, indent=1)

        print(json_file)

    # creates an m10 replicaSet
    def create_small(self, group_id, name):
        s = Session()
        base_url = self.base_url
        directory = os.path.join('cluster', 'json_files', 'cluster_m10.json')
        name = name
        url = "{}/groups/{}/clusters".format(base_url, group_id)
        auth = HTTPDigestAuth(self.api_user, self.api_key)
        headers = {'content-type': 'application/json'}
        logging.info("Executing POST: {}".format(url))
        #base_url = self.base_url
        #url = "{}/groups/{}/clusters/{}".format(base_url, group_id, name)
        with open(directory) as f:
            json_file = json.load(f)
            for key in json_file.keys():
                try:
                    if key == 'name':
                        json_file['name'] = name
                        print(json_file)
                        #yield True
                    #r = s.post(json_file)
                    r = s.post(url,
                        auth=auth,
                        data=json.dumps(json_file),
                        headers=headers
                        )

                        #yield false
                except:
                    self.check_response(r)

     #creates an m30 replicaSet

        def create_medium(self, group_id, name):
            base_url = self.base_url
            url = "{}/groups/{}/clusters/{}".format(base_url, group_id, name, json_file)
            self.post(url, 'cluster/cluster_m30.json')

        def resize(self, group_id, name):
            base_url = self.base_url
            url = "{}/groups/{}/clusters/{}".format(base_url, group_id, name)
            self.path(url, 'test_json')


# Initialize the command line options parser
parser = argparse.ArgumentParser()
parser.add_argument('-G', '--get', action='store_true', help="get's the currnet group cluster configuration")
parser.add_argument('-C', '--create', action='store_true', help='creates a new cluster')
parser.add_argument('-f', '--file', help='write file to current directy or path')
parser.add_argument('-n', '--name', required=True, help='the name of the cluster')
parser.add_argument('-g', '--group_id', required=True, help='id of the group that you are trying to make the changes for')
parser.add_argument('-u', '--api_user', required=True, help='the email address you use to login')
parser.add_argument('-k', '--api_key', required=True, help='Your Atlas api key')
args = parser.parse_args()
run = Cluster(args.group_id, args.api_user, args.api_key)

if args.get:
    if args.file:
        # makes directory platform independent
        directory = os.path.relpath(args.file)
        print(directory)
        with open(directory, 'w') as f:
            sys.stdout = f
            run.get_cluster(args.group_id, args.name)
    else:
        run.get_cluster(args.group_id, args.name)
elif args.create:
    answer = raw_input('Enter small or medium: ')
    if answer.lower().startswith('s'):
        run.create_small(args.group_id, args.name)
    elif answer.lower().startswith('m'):
        run.create_medium(args.group_id, args.name, 'cluster_m30.json')
else:
    print('you did not enter an option...')

def main():
    run
    return 0 # return an integer

if __name__ == '__main__':
    sys.exit(main())
