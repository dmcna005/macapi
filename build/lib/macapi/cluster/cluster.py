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

        try:
            # remove duplicate keys if any
            for key,value in details.items():
                if 'replicationSpecs' not in results.keys():
                    results[key] = value

                json_file = json.dumps(results, indent=1)

            return json_file

        except Exception as e:
            print('error found: ' + e)

    # creates an m10 replicaSet
    def create_small(self, group_id, name):
        s = Session()
        base_url = self.base_url
        path = os.path.abspath('macapi/json_files')
        directory = os.path.join(path, 'cluster_m10.json')
        name = name
        url = "{}/groups/{}/clusters".format(base_url, group_id)
        auth = HTTPDigestAuth(self.api_user, self.api_key)
        headers = {'content-type': 'application/json'}
        logging.info("Executing POST: {}".format(url))

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
            s = Session()
            base_url = self.base_url
            path = os.path.abspath('macapi/json_files')
            directory = os.path.join(path, 'cluster_m30.json')
            name = name
            url = "{}/groups/{}/clusters".format(base_url, group_id)
            auth = HTTPDigestAuth(self.api_user, self.api_key)
            headers = {'content-type': 'application/json'}
            logging.info("Executing POST: {}".format(url))

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

    def resize(self, group_id, name, size):
        base_url = self.base_url
        url = "{}/groups/{}/clusters/{}".format(base_url, group_id, name)
        data = {'providerSettings.instanceSizeName' : size}
        result = self.patch(url, data)
        return result

    def delete_cluster(self, group_id, name):
        base_url = self.base_url
        url = '{}/groups/{}/clusters/{}'.format(base_url, group_id, name)
        s = Session()
        headers = {'content-type': 'application/json'}
        auth=HTTPDigestAuth(self.api_user, self.api_key)
        try:
            result = s.delete(url, auth=auth, headers=headers)
            return result
        except Exception as e:
            print('\033[1;41m{}\033[1;m'.format(e))




# Initialize the command line options parser
parser = argparse.ArgumentParser()
parser.add_argument('-G', '--get', help="get's the currnet group cluster configuration")
parser.add_argument('-C', '--create', help='creates a new cluster')
parser.add_argument('-f', '--file', help='write file to current directy or path')
parser.add_argument('-n', '--name', required=True, help='the name of the cluster')
parser.add_argument('-g', '--group_id', required=True, help='id of the group that you are trying to make the changes for')
parser.add_argument('-u', '--api_user', required=True, help='the email address you use to login')
parser.add_argument('-k', '--api_key', required=True, help='Your Atlas api key')
parser.add_argument('-S', '--size', help='reszises an intance')
parser.add_argument('-D', '--delete', help='deletes a cluster from a project')
args = parser.parse_args()
run = Cluster(args.group_id, args.api_user, args.api_key)

if args.get:
    if args.file:
        # makes directory platform independent
        directory = os.path.relpath(args.file)
        with open(directory, 'w') as f:
            sys.stdout = f
            # get_cluster is a return method so we need to save it as an object for next line of the code
            get = run.get_cluster(args.group_id, args.name)
            # printing get so that it gets redirected into standard out which is the object f
            print(get)

    else:
        get = run.get_cluster(args.group_id, args.name)
        print(get)
elif args.create:
    answer = raw_input('Enter small or medium: ')
    if answer.lower().startswith('s'):
        run.create_small(args.group_id, args.name)
    elif answer.lower().startswith('m'):
        run.create_medium(args.group_id, args.name)

elif args.size:
    print('\033[1;33monly accepts sizes M10 or M30\033[1;m]')
    size_name = raw_input('enter the instance size: ')
    # check that the size_name variable is not empty
    if size_name != '':
        print('you are about to rezie {} to {} '.format(args.name, size_name))
        answer = raw_input('type y/n: ')
        if answer.lower().startswith('y'):
            update = run.resize(args.group_id, args.name, args.size)
            print(update)
        else:
            print('aborting...')
            sys.exit(0) # exit cleanly

elif args.delete:
    print('\033[1;33myou are about to delete {}\033[1;m'.format(args.name))
    answer = raw_input('are you sure you want to proceed?: ')

    while answer:

        if answer.lower().startswith('y'):
            delete = run.delete_cluster(args.group_id, args.name)
            print('\033[1;32mdeleted {}, {}\033[1;m'.format(args.name, delete))
            break
        elif answer.lower().startswith('n'):
            print('aborting...')
            break
        else:
            print('\033[1;33myou must enter either y/n\033[1;m')
            continue
    sys.exit(0)

else:
    print('you did not enter an option...')

def main():
    run


if __name__ == '__main__':
    sys.exit(main())
