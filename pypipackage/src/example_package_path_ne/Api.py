import json
import os
import logging
from flask import Flask, request, jsonify
from flask.logging import create_logger

app = Flask(__name__)
LOG = create_logger(app)


code_folder = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=f'{code_folder}\\console.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
LOG.info(f"code folder: {code_folder}")
LOG.info(f"database file: {code_folder}\\database.txt")


# API Reachability Test 
@app.route('/')
def index():
    # This function will be called for GET requests to /
    return jsonify({'name': 'network_engineer',
                    'email': 'network_engineer@path_ne.com',
                    'channel': 'http://www.youtube.com/@path_ne',
                    'message': 'GET Request to root URL successful'})


#GET Method to receive list of routers, list all devices without hostname argument.
@app.route('/routers', methods=['GET'])
def getRouter():
    try:
        hostname = request.args.get('hostname')
        #print(hostname)
        with open(f'{code_folder}\\database.txt', 'r') as cf:
            data = cf.read()
            records = json.loads(data)
            #print(records)
            if (hostname is None) or (hostname == ""):
                LOG.info('All devices shown')
                return jsonify(records), 200
            else:
                for record in records:
                    #print(f'{record['hostname']}')
                    #print(hostname)
                    if record['hostname'] == hostname:
                        LOG.info(f'{hostname} returned')
                        return jsonify(record), 200
                if record['hostname'] != hostname:
                    LOG.warning('No matching router')
                    return jsonify({"response": "No match"}), 200
    except Exception as err:
        LOG.error(f'Error during GET {err}')
        return jsonify({"error": err}), 401


# GET Method to receive list of routers, sends error without hostname argument
# @app.route('/routers', methods=['GET'])
# def getRouter():
#     try:
#         hostname = request.args.get('hostname')
#         #print(hostname)
#         if (hostname is None) or (hostname == ""):
#                 LOG.warning('Missing the hostname')
#                 raise ValueError 
#         with open(f'{code_folder}\\database.txt', 'r') as cf:
#             data = cf.read()
#             records = json.loads(data)
#             #print(records)
#             for record in records:
#                 #print(f'{record['hostname']}')
#                 #print(hostname)
#                 if record['hostname'] == hostname:
#                     LOG.info(f'{hostname} returned')
#                     return jsonify(record), 200
#                 if record['hostname'] != hostname:
#                     LOG.warning('No matching router')
#                     return jsonify({"response": "No match"}), 200
#     except ValueError:
#         LOG.error("NO HOSTNAME SPECIFIED ON REQUEST")
#         return jsonify({"error": "Missing the hostname, mate"}), 400
#     except Exception as err:
#         LOG.error(f'Error during GET {err}')
#         return jsonify({"error": err}), 401


@app.route('/routers', methods=['POST'])
def AddRouter():
    try:
        record = json.loads(request.data)
        LOG.info(f'inbound record {record}')
        with open(f'{code_folder}\\database.txt', 'r') as cf:
            data = cf.read()
            records = json.loads(data)
        if record in records:
            return jsonify({"status": "Device already exists"}), 200
        if record not in records:
            records.append(record)
            LOG.info(f"records output {records}")
            LOG.warning(f'router added {record["hostname"]}')
        with open(f'{code_folder}\\database.txt', 'w') as f:
            f.write(json.dumps(records, indent=2))
        return jsonify(record), 201
    except Exception as err:
        LOG.error(f'Error during ADD {err}')
        return jsonify({"error":err})




@app.route('/routers', methods=['DELETE'])
def deleteRouter():
    try:
        record = json.loads(request.data)
        new_records = []
        with open(f'{code_folder}\\database.txt', 'r') as cf:
            data = cf.read()
            records = json.loads(data)
            for r in records:
                if r['hostname'] == record['hostname']:
                    LOG.warning(f'Deleted {r["hostname"]}')
                    continue
                new_records.append(r)
        with open(f'{code_folder}\\database.txt', 'w') as f:
            f.write(json.dumps(new_records, indent=2))
        return jsonify(record), 204
    except Exception as err:
        LOG.error(f'Error raised {err}')
        return jsonify({"error": err})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)