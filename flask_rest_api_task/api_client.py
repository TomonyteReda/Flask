import requests, sys


prekes_info = {
    "pavadinimas": "lekste",
    "kaina": 10.00,
    "kiekis": 50
}


def return_arguments():
    args = {}
    action = sys.argv[1]
    args["action"] = action
    if len(sys.argv) > 2:
        id = sys.argv[2]
        args["id"] = id
    return args


def change_product_data(action, id):
    if action == 'add':
        r = requests.post('http://10.250.0.47:5000/preke', json=prekes_info)
    elif action == 'review_all':
        r = requests.get('http://10.250.0.47:5000/preke')
    elif action == 'review':
        r = requests.get(f'http://10.250.0.47:5000/preke/{id}')
    elif action == 'change':
        r = requests.put(f'http://10.250.0.47:5000/preke/{id}', json=prekes_info)
    elif action == 'delete':
        r = requests.delete(f'http://10.250.0.47:5000/preke/{id}')
    return r.json()


def main():
    arguments = return_arguments()
    action = arguments["action"]
    if len(arguments.keys()) > 1:
        id = arguments["id"]
        result = change_product_data(action, id=id)
    else:
        result = change_product_data(action, id=None)
    print(result)


main()