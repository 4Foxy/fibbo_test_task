from flask import Flask, make_response, jsonify
import logging
from mongolog.handlers import MongoHandler
app = Flask(__name__)



def read_data():
    with open('readData.txt', 'r') as f:
        lst = [[int(num) for num in line.split(',')] for line in f if line.strip() != ""]
    return lst


def checkIsFibonacci(arr, n):
    if n == 1 or n == 2:
        return True
    arr.sort()
    for i in range(2, n):
        if ((arr[i - 1] +
             arr[i - 2]) != arr[i]):
            return False

    return True


def reverse(arr):
    n = len(arr)
    for i in range(int(n / 2)):
        lst = arr[i]
        arr[i] = arr[n - i - 1]
        arr[n - i - 1] = lst
    return arr


def main_func(arr):
    N = len(arr)
    res_list = []
    for i in range(N):
        if checkIsFibonacci(arr[i], len(arr[i])):
            res_list.append(reverse(arr[i]))
        else:
            res_list.append(arr[i])
    return res_list


@app.route('/', methods=["GET"])
def return_fibo():
    log = logging.getLogger('GET')
    log.setLevel(logging.DEBUG)
    log.addHandler(MongoHandler.to(db='TestTask', collection='Logs'))
    log.debug('GET info from file')
    return str(read_data())


@app.route("/", methods=["POST"])
def save_fibo():
    tmp_lst = read_data()
    result = main_func(tmp_lst)
    with open('readData.txt', 'w') as file:
        for row in result:
            file.write(','.join([str(item) for item in row]))
            file.write('\n')
    res = make_response(jsonify({"message": "Success"}), 201)
    app.logger.info('PUT processed data into file')
    log = logging.getLogger('PUT')
    log.setLevel(logging.DEBUG)
    log.addHandler(MongoHandler.to(db='TestTask', collection='Logs'))
    log.debug('PUT processed data into file')
    return res


if __name__ == '__main__':
    app.run()
