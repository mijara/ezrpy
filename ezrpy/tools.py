# Tools to easily create, update, remove objects
import requests
import argparse

DELETE_URL = 'http://localhost:5000/api/%s/%d/'
CREATE_URL = 'http://localhost:5000/api/%s/'


def create_handler(collection, raw_body):
    body = {}

    for item in raw_body:
        try:
            key, value = item.split('=')
            body[key] = value
        except ValueError:
            return 'invalid body items'

    for key, value in body.items():
        print key + ':', value

    response = raw_input('Are you sure? Y/n: ')
    while response not in ('', 'n', 'y', 'Y', 'N'):
        response = raw_input('Are you sure? Y/n: ')

    if response in ['', 'Y', 'y']:
        r = requests.post(CREATE_URL % collection, json=body)
        if r.status_code == 200:
            return r.content
        return 'server response code %d' % r.status_code
    else:
        return 'aborted'


def delete_handler(collection, pk):
    url = DELETE_URL % (collection, pk)
    r = requests.delete(url)

    if r.status_code == 200:
        return 'ok'
    return 'server response code %d' % r.status_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='action')

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('collection')
    delete_parser.add_argument('pk', type=int)

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('collection')
    create_parser.add_argument('body', nargs='*')

    args = parser.parse_args()

    if args.action == 'delete':
        print delete_handler(args.collection, args.pk)
    elif args.action == 'create':
        print create_handler(args.collection, args.body)
