__author__ = "Iyappan"
__email__ = "iyappan@trackerwave.com"
__status__ = "planning"

import re
import requests
from datetime import datetime
import traceback
import json
from cryptography.fernet import Fernet
import random
import string
import pytz
valid_dt = [dict, list, str, int, float, tuple, set, bool]
from sys import getsizeof
import os
import ssl
import psutil
import math
from os import path
import paho.mqtt.client as mqtt
import sqlite3

def frame_and_publish(g_info, err_msg, cid="", url=""):
    try:
        g_info["info"]["api_alert_info"]["api_alert_flag"] = True
        pub_data = \
            {
                "ctx": "alert",
                "typ": "api",
                "ope": "",
                "gid": g_info["gid"],
                "data": {
                    "jid": g_info["jid"],
                    "sid": g_info["sid"],
                    "msg": str(err_msg),
                    "cid": str(cid),
                    "url": str(url)
                }
            }
        g_info["info"]["client"][g_info["info"]["debug"]["log_client"]]["con"].publish(g_info["info"]["debug"]["log_topic"], str(data_encrypt(pub_data, g_info["private_key"])))
    except Exception:
        return

def check_api_alert(cid, g_info, url=None, api_resp=None, s_flag=False, vtme_flag=False):
    try:
        api_alert = g_info["info"]["api_alert"][cid]
        api_alert_info = g_info["info"]["api_alert_info"]
        if vtme_flag:
            if api_alert["flag"]:
                if datetime.now().timestamp() - api_alert["last_wt"] >=\
                        api_alert["wt_tme"]:
                    return True
                else:
                    return False
            return True
        else:
            if s_flag:
                api_alert["fcnt"] = 0
                api_alert["flag"] = False
                api_alert_info["api_alert_flag"] = False
            else:
                api_alert["fcnt"] += 1
                if not api_alert_info["api_alert_flag"] and \
                        api_alert["fcnt"] >= api_alert["flmt"]:
                    err_msg = "Failed by Exception. " if url is None else " "
                    api_alert_info["api_alert_flag"] = True
                    if api_resp not in ("", None):
                        if "statusCode" in api_resp:
                            err_msg += " Status Code = " + str(api_resp["statusCode"]) + "  "
                        if "errorCode" in api_resp:
                            err_msg += " Error Code = " + str(api_resp["errorCode"])
                        if "err_msg" in api_resp:
                            err_msg += " Error Message : " + str(api_resp["err_msg"])
                    frame_and_publish(g_info, err_msg, cid, url)
                    api_alert["flag"] = True
                    api_alert["last_wt"] = datetime.now().timestamp()
                    return [True, err_msg]
    except Exception:
        return [False, str(traceback.format_exc())]

def api_request(r_type, url, auth, cid, g_info, data=None):
    try:
        if cid in g_info["info"]["api_alert"] and auth in g_info["auth"] and r_type in ["get", "post", "put"]:
            auth = g_info["auth"][auth]
            api_alert = g_info["info"]["api_alert"][cid]
            api_alert_info = g_info["info"]["api_alert_info"]
            s_time = datetime.now().timestamp()
            g_info["info"]["api_alert"][cid]["s_time"] = datetime.now().timestamp()
            if "e_time" in api_alert:
                del api_alert["e_time"]
            response = None
            if r_type == "get":
                response = requests.get(url, headers=auth)
            elif r_type == "post" and data is not None:
                response = requests.post(url, data=json.dumps(data), headers=auth)
            elif r_type == "put" and data is not None:
                response = requests.put(url, data=json.dumps(data), headers=auth)
            else:
                response = {"error": "missing data"}
            if response is not None:
                response = response.json()
            res = {"status": True, "response": response, "time": datetime.now().timestamp() - s_time, "err_msg": "", "exc": ""}
            if api_alert is not None and api_alert_info is not None:
                if res["response"] is not None and "statusCode" in res["response"] and "results" in res["response"] and  res["response"]["statusCode"] in api_alert["ssc"]:
                    check_api_alert(cid, g_info, url, "", True)
                    clog(api_alert["lid"][0], {"msg": r_type + " request success " + str(url) + " " + str(auth), "time": res["time"], "cid": cid, "sts": "success"}, g_info)
                    if "empty" in api_alert and api_alert["empty"]:
                        if not res["response"]["results"]:
                            res["status"] = False
                            clog(api_alert["lid"][0], {"msg": r_type + " results empty " + str(url) + " " + str(auth), "time": res["time"], "cid": cid, "sts": "empty"}, g_info)
                else:
                    check_res = check_api_alert(cid, g_info, url, res["response"])
                    res["status"] = False
                    if check_res is not None:
                        if check_res[0]:
                            res["err_msg"] = check_res
                        else:
                            res["exc"] = check_res
                api_alert["e_time"] = datetime.now().timestamp()
            
        else:
            res = {"status": False, "response": None, "time": 0, "err_msg": "invalid request", "exc": ""}
        if not res["status"]:
            clog(api_alert["lid"][1], {"msg": r_type + "response failed " + str(res), "cid": cid, "sts": "failed"}, g_info)
        return res
    except Exception:
        res = {"status": False, "response": None, "time": datetime.now().timestamp() - s_time, "err_msg": "", "exc": str(traceback.format_exc())}
        if api_alert is not None:
            api_alert["e_time"] = datetime.now().timestamp()
        clog("", {"msg": "request exception " + str(res), "cid": cid, "sts": "failed"}, g_info)
        return res

def api_file_download(url, auth, cid, g_info):
    try:
        if cid in g_info["info"]["api_alert"] and auth in g_info["auth"]:
            auth = g_info["auth"][auth]
            api_alert = g_info["info"]["api_alert"][cid]
            api_alert_info = g_info["info"]["api_alert_info"]
            s_time = datetime.now().timestamp()
            g_info["info"]["api_alert"][cid]["s_time"] = datetime.now().timestamp()
            if "e_time" in api_alert:
                del api_alert["e_time"]
            response = requests.get(url, headers=auth)
            res = {"status": True, "response": response, "time": datetime.now().timestamp() - s_time, "err_msg": "", "exc": ""}
            if api_alert is not None and api_alert_info is not None:
                if (res["response"] is not None and "statusCode" in res["response"] and  res["response"]["statusCode"] in api_alert["ssc"]) or res["response"].status_code == 200:
                    check_api_alert(api_alert, api_alert_info, url, "", True)
                    clog(api_alert["lid"][0], {"msg": "request success " + str(url) + " " + str(auth), "time": res["time"], "cid": cid}, g_info)
                else:
                    check_res = check_api_alert(api_alert, api_alert_info, url, res["response"])
                    if check_res is not None:
                        res["status"] = False
                        if check_res[0]:
                            res["err_msg"] = check_res
                        else:
                            res["exc"] = check_res
                api_alert["e_time"] = datetime.now().timestamp()
            
        else:
            res = {"status": False, "response": None, "time": 0, "err_msg": "invalid request", "exc": ""}
        if not res["status"]:
            clog(api_alert["lid"][1], {"msg": "response failed " + str(res), "cid": cid}, g_info)
        return res
    except Exception:
        res = {"status": False, "response": None, "time": datetime.now().timestamp() - s_time, "err_msg": "", "exc": str(traceback.format_exc())}
        if api_alert is not None:
            api_alert["e_time"] = datetime.now().timestamp()
        clog("", {"msg": "request exception " + str(res), "cid": cid}, g_info)
        return res



def clog(log_id, payload, g_info):
    """Frames and publishes the exception log message generated in this JOB
    params:
    log_id: A string identifier to uniquely identify the log
    payload: An object defining the exceptions caught in the module
    """
    def publish_rollback_log():
        """ Publishes the log data in global rollback object"""
        for data in g_info["info"]["log_rollback"]:
            g_info["info"]["client"][g_info["info"]["debug"]["log_client"]]["con"].publish(g_info["info"]["debug"]["log_topic"], str(data_encrypt(data, g_info["private_key"])))
        g_info["info"]["log_rollback"] = []
    if log_id == "":
        log_id = g_info["info"]["debug"]["clog"]
    hprint("Log : " + log_id + ' ' + str(payload), g_info)
    log_data = {
        "ctx": "log",
        "typ": "logging",
        "ope": "create",
        "gid": str(g_info["gid"]),
        "data":
            {
                "lid": log_id,
                "sid": g_info["sid"],
                "jid": g_info["jid"],
                "payload": str(payload),
                "etm": str(datetime.now())
            }
    }
    try:
        if 'info' in g_info and g_info["info"]["client"][g_info["info"]["debug"]["log_client"]]["con"] != '':
            if len(g_info["info"]["log_rollback"]) > 0:
                publish_rollback_log()
            g_info["info"]["client"][g_info["info"]["debug"]["log_client"]]["con"].publish(g_info["info"]["debug"]["log_topic"], str(data_encrypt(log_data, g_info["private_key"])))
        else:
            g_info["info"]["log_rollback"].append(log_data)
    except Exception:
        g_info["info"]["log_rollback"].append(json.dumps(traceback.format_exc()))
        g_info["info"]["log_rollback"].append(log_data)
        if len(g_info["info"]["log_rollback"]) >= g_info["info"]["rollback_limit"]:
            hprint("Log Rollback limit exceeded " + str(len(g_info["info"]["log_rollback"])), g_info)
            g_info["info"]["log_rollback"] = []

def hprint(msg, g_info=None, hash_id="#0000"):
    """Frames and publishes the debug prints
    params:
    msg: a string message to be printed
    hash_id[optional]: A string identifier to identify the prints
    """
    try:
        del_req = []
        if g_info is not None:
            if hash_id == "#0000":
                hash_id = g_info["info"]["debug"]["hprint"]
            if g_info["info"]["debug"]["dev_mode"]:
                print(str(hash_id) + "   " + str(msg))
            if len(g_info["info"]["debug_tracker"]) > 0:
                for tid, req_info in g_info["info"]["debug_tracker"].items():
                    if not req_info["data"]["enable"] or datetime.now().timestamp() - \
                            req_info["data"]["last_update"] > req_info["data"]["duration"]:
                        del_req.append(tid)
                    else:
                        if req_info["data"]["enable"]:
                            pub_data = {
                                "ctx": req_info["ctx"],
                                "typ": "response",
                                "ope": req_info["ope"],
                                "gid": g_info["gid"],
                                "data": {
                                    "tid": req_info["data"]["tid"],
                                    "rid": req_info["data"]["rid"],
                                    "sid": g_info["sid"],
                                    "jid": g_info["jid"],
                                    "hash_id": str(hash_id),
                                    "data": str(msg),
                                    "remaining_time": req_info["data"]["duration"] - int(
                                        datetime.now().timestamp() - req_info["data"]["last_update"]),
                                }
                            }
                            g_info["info"]["client"][g_info["info"]["debug"]["log_client"]]["con"].publish(g_info["info"]["debug"]["h_topic"]+str(req_info["data"]["tid"])+"/"+str(req_info["data"]["rid"]), str(data_encrypt(pub_data, g_info["private_key"])))
                if len(del_req) > 0:
                    for tid in del_req:
                        del g_info["info"]["debug_tracker"][tid]
        else:
            print(str(hash_id) + "   " + str(msg))
    except Exception:
        clog("", {"exc": str(traceback.format_exc())})

def data_encrypt(raw_data, private_key):
    """Encrypts the raw data using the private key and outputs an encrypted byte
    params:
    raw_data: An object which is to be encrypted
    returns an encrypted byte equivalent to the given raw data
    """
    try:
        encode_data = json.dumps(raw_data).encode()
        encrypt_data = Fernet(private_key).encrypt(encode_data)
        return encrypt_data
    except Exception:
        return None


def data_decrypt(encrypt_data, private_key):
    """Decrypts the encrypted data using the private key and outputs a decrypted object
    params:
    encrypt_data: An encrypted byte which is to be decrypted
    returns an object equivalent to the given encrypted byte
    """
    try:
        decrypt_data = Fernet(private_key).decrypt(encrypt_data)
        decoded_data = json.loads(decrypt_data)
        return decoded_data
    except Exception:
        return None


def random_string(string_length=12):
    """Generates a random string of given length
    params:
    string_length[optional]: An integer defining the length of the string to be generated
    """
    try:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))
    except Exception:
        return "None"


def find_query_combination(res, cmmd, comb):
    for key, value in res.items():
        if cmmd == "":
            comb.append(str(key))
            if type(value) is dict and value:
                find_query_combination(value, str(key), comb)
        else:
            comb.append(cmmd+" "+str(key))
            if type(value) is dict and value:
                find_query_combination(value, cmmd+" "+str(key), comb)
    return comb

def find_key_values(res, key, f_data):
    if type(res) is dict:
        for k, v in res.items():
            if key == k:
                f_data.append([k, v])
            find_key_values(v, key, f_data)
    elif type(res) is list:
        for r in res:
            if type(r) is dict:
                for k, v in r.items():
                    if k == key:
                        f_data.append([k, v])
                    find_key_values(v, key, f_data)
    return f_data

def find_like_values(res, key, f_data):
    if type(res) is dict:
        for k, v in res.items():
            if key in k:
                f_data.append([k, v])
            find_key_values(v, key, f_data)
    elif type(res) is list:
        for r in res:
            if type(r) is dict:
                for k, v in r.items():
                    if key in k:
                        f_data.append([k, v])
                    find_key_values(v, key, f_data)
    return f_data
def int_convert(key):
    try:
        key = int(key)
        return True
    except Exception:
        return False

def res_check(res):
    if type(res) is dict:
        print("dict", str(getsizeof(res)) + " bytes", len(res))
        for key, val in res.items():
            print(key, val, type(val))
            if type(val) in valid_dt:
                print("vdt**********", val)
                res_check(val)
            else:
                print("nvdt*********", val)
                res[key]=str(val)
    elif type(res) is list:
        print("list", str(getsizeof(res)) + " bytes")
        for data in res:
            if type(data) in valid_dt:
                print("vdt**********", data)
            else:
                print("nvdt*********", data)


def res_validation(res):
    res_check(res)
    return res

def find_query(res, cmmd):
    cmmd = cmmd.split(" ")
    for i in range(len(cmmd)):
        key = cmmd[i]
        if key == "-query":
            if len(cmmd) == i+1:
                if type(res) is dict:
                    res = find_query_combination(res, "", [])
                    res = res_validation(res)
                    return {"status": True, "res": res}
            else:
                return {"status": False, "res": "invalid query '" + str(key) + "'"}
        elif key == "-count":
            res = len(res)
        elif key == "-size":
            res = str(getsizeof(res)) + " bytes"
        elif key == "-find":
            if len(cmmd) == i+2:
                res = find_key_values(res, cmmd[i+1], [])
                res = res_validation(res)
                return {"status": True, "res": res}
            else:
                return {"status": False, "res": "invalid query '" + str(key) + "'"}
        elif key == "-like":
            if len(cmmd) == i+2:
                res = find_like_values(res, cmmd[i+1], [])
                res = res_validation(res)
                return {"status": True, "res": res}
            else:
                return {"status": False, "res": "invalid query '" + str(key) + "'"}
        elif key == "-keys":
            if type(res) is dict:
                if len(cmmd) == i+1:
                    res = list(res.keys())
                    res = res_validation(res)
                    return {"status": True, "res": res}
            return {"status": False, "res": "invalid query '" + str(key) + "'"}
        elif key == "-help":
            res = ['-query or <key> -query', "-count or <key> -count", "-size or <key> -size", "-find <key> or <key> -find <key>", "-like or <key> -like <str>", "-keys or <key> -keys", "-help"]
        elif key in res:
            res = res[key]
        elif int_convert(key):
            key = int(key)
            if key in res:
                res = res[key]
            else:
                return {"status": False, "res": "invalid query '" + str(key) + "'"}
        else:
            return {"status": False, "res": "invalid query '" + str(key) + "'"}
    res = res_validation(res)
    return {"status": True, "res": res}

def raw_data_adpter(data):
    try:
        res = []
        if "MTI" in data:
            if data["MTI"] == "L1":
                if "RSN" in data and "DATA" in data:
                    for tag in data["DATA"].split(","):
                        tag = tag.split("|")
                        if len(tag) >= 3:
                            tag_data = {"TSN": tag[0],"RSN":data["RSN"],"TYP":tag[1],"RSSI":tag[2],"BCN":"","DTM":data["DTM"]}
                            if len(tag) >= 4:
                                tag_data["BCN"] = tag[3]
                            res.append(tag_data)
            elif data["MTI"] == "L2":
                if "RSN" in data and "DATA" in data and "TYP" in data:
                    for tag in data["DATA"].split(","):
                        tag = tag.split("|")
                        if len(tag) >= 2:
                            tag_data = {"TSN": tag[0],"RSN":data["RSN"],"TYP":data["TYP"],"RSSI":tag[1],"BCN":"","DTM":data["DTM"]}
                            if len(tag) >= 3:
                                tag_data["BCN"] = tag[2]
                            res.append(tag_data)
            elif data["MTI"] == "L3":
                if "TSN" in data and "DATA" in data and "TYP" in data and "BCN" in data and "DTM" in data and type(data["DATA"]) is list:
                    for tag in data["DATA"]:
                        tag_data = {"TSN": data["TSN"],"RSN":tag["RSN"],"TYP":data["TYP"],"RSSI":tag["RSSI"],"BCN":data["BCN"],"DTM":data["DTM"]}
                        res.append(tag_data)
            elif data["MTI"] == "L4":
                if "TSN" in data and "DATA" in data and "TYP" in data and "BCN" in data and "DTM" in data:
                    for tag in data["DATA"].split(","):
                        tag = tag.split("|")
                        if len(tag) >= 2:
                            tag_data = {"TSN": data["TSN"],"RSN":tag[0],"TYP":data["TYP"],"RSSI":tag[1],"BCN":data["BCN"],"DTM":data["DTM"]}
                            res.append(tag_data)
        elif "RSN" in data and "DATA" in data:
            for tag in data["DATA"]:
                if "TYP" in tag and tag["TYP"] == "BLE":
                    if "TSN" in tag and "TYP" in tag and "BCN" in tag and "DTM" in tag and "RSSI" in tag:
                        res.append({"TSN":tag["TSN"],"RSN":data["RSN"],"TYP":tag["TYP"],"RSSI":tag["RSSI"],"BCN":tag["BCN"],"DTM":tag["DTM"]})
                elif "TYP" in tag and tag["TYP"] == "ICT":
                    if "SNO" in tag and "CSNO" in tag and "TIME" in tag and "DRN" in tag and "SEQ" in tag and "LOC" in tag and "CV" in tag and "CRSSI" in tag :
                        res.append({"SNO":tag["SNO"],"RSN":data["RSN"],"TYP":tag["TYP"],"CSNO":tag["CSNO"],"TIME":tag["TIME"],"DRN":tag["DRN"],"SEQ":tag["SEQ"],"LOC":tag["LOC"],"CV":tag["CV"],"CRSSI":tag["CRSSI"]})
                elif "TYP" in tag and tag["TYP"] == "S3":
                    if "TSN" in tag and "TYP" in tag and "WATCH" in tag and "DTM" in tag and "RSSI" in tag:
                        res.append({"TSN":tag["TSN"],"RSN":data["RSN"],"TYP":tag["TYP"],"RSSI":tag["RSSI"],"WATCH":tag["WATCH"],"DTM":tag["DTM"]})
                elif "TYP" in tag and tag["TYP"] == "SP":
                    if "TSN" in tag and "TYP" in tag and "SMART_PLUG" in tag and "DTM" in tag and "RSSI" in tag:
                        res.append({"TSN":tag["TSN"],"RSN":data["RSN"],"TYP":tag["TYP"],"RSSI":tag["RSSI"],"SMART_PLUG":tag["SMART_PLUG"],"DTM":tag["DTM"]})
                else:
                    tag["RSN"] = data["RSN"]
                    res.append(tag)
        return res
    except Exception:
        return

def timezone_converter(tz):
    try:
        time_zone = pytz.timezone(str(tz))
        return datetime.now(time_zone)
    except Exception:
        return

def sub_process_info():
    try:
        proc = psutil.Process(os.getpid())
        p_per = {
                "cpu": proc.cpu_percent(interval=1),
                "mem": round(float(proc.memory_full_info().rss / 1000000), 2),
                "mem_p": round(float(proc.memory_percent()), 2),
                "mem_v": round(float(proc.memory_full_info().vms / 1000000), 2)
            }
        return p_per
    except Exception:
        return {}

def compute_page_size(ps, tr):
    rem, cnt = tr, 1
    tmp_rem = rem
    while rem > int(ps) and \
            (rem - int(ps)) > 100:
        rem = tmp_rem
        rem = math.ceil(rem / cnt)
        cnt += 1
    return rem


def mqtt_client(g_info, client_id, b_type):
    
    def on_message(client, userdata, message):
        """Receives message individually and stores them in a global object
        params:
        message: received object/string to be evaluated
        """
        try:
            g_info["info"]["client"][client_id]["method_call"](message)
        except Exception:
            clog("", {"exc": str(traceback.format_exc()), "msg": str(message.payload)}, g_info)


    def on_connect(client, userdata, flags, rc):
        """Connects to the MQTT client and subscribes to the pre-defined topics
        params:
        rc: 0- connected, 1- not connected
        """
        try:
            if rc == 0:
                g_info["info"]["client"][client_id]["flag"] = True
                g_info["info"]["client"][client_id]["con"].connected_flag = True
                if "topic" in g_info["info"]["client"][client_id]["config"]:
                    for sub_topic in g_info["info"]["client"][client_id]["config"]["topic"]:
                        g_info["info"]["client"][client_id]["con"].subscribe(sub_topic)
                        clog("", {"msg": "Topic = " + str(sub_topic)}, g_info)
                clog("", {"msg": str(client_id) + " Connected Successfully"}, g_info)
            else:
                g_info["info"]["client"][client_id]["flag"] = False
                g_info["info"]["client"][client_id]["con"].connected_flag = False
                clog("", {"msg": str(client_id) + " Not Connected"}, g_info)
        except Exception:
            clog("", {"exc": str(traceback.format_exc())})


    def on_disconnect(client, userdata, rc):
        """Disconnects from the MQTT client
        params:
        rc: 0- connected, 1- not connected
        """
        try:
            g_info["info"]["client"][client_id]["flag"] = False
            g_info["info"]["client"][client_id]["con"].connected_flag = False
            clog("", {"msg": "Disconnected"}, g_info)
        except Exception:
            clog("", {"exc": str(traceback.format_exc())}, g_info)

    try:
        g_info["info"]["client"][client_id]["con"] = mqtt.Client(
            g_info["broker"][b_type]["client_name"] + random_string(20))
        g_info["info"]["client"][client_id]["con"].on_connect = on_connect
        g_info["info"]["client"][client_id]["con"].on_disconnect = on_disconnect
        g_info["info"]["client"][client_id]["con"].on_message = on_message
        if "ssl" in g_info["broker"][b_type] and "ca_path" in \
                g_info["broker"][b_type]:
            if g_info["broker"][b_type]["ssl"] and path.exists(
                    g_info["broker"][b_type]["ca_path"]):
                ssl_context = ssl.create_default_context(cafile=g_info["broker"][b_type]["ca_path"])
                if g_info["broker"][b_type]["ma"] and "cert_path" in \
                        g_info["broker"][b_type] and "key_path" in \
                        g_info["broker"][b_type]:
                    if path.exists(g_info["broker"][b_type]["cert_path"]) and path.exists(
                            g_info["broker"][b_type]["key_path"]):
                        ssl_context.load_cert_chain(certfile=g_info["broker"][b_type]["cert_path"],
                                                    keyfile=g_info["broker"][b_type]["key_path"])
                ssl_context.check_hostname = False
                g_info["info"]["client"][client_id]["con"].tls_set_context(ssl_context)
        if g_info["broker"][b_type]["authorize"]:
            g_info["info"]["client"][client_id]["con"].username_pw_set(
                username=g_info["broker"][b_type]["username"],
                password=g_info["broker"][b_type]["password"])
        g_info["info"]["client"][client_id]["con"].connect(
            g_info["broker"][b_type]["host"],
            g_info["broker"][b_type]["port"])
        g_info["info"]["client"][client_id]["con"].loop_forever()
    except Exception:
        clog("", {"exc": str(traceback.format_exc())}, g_info)

def sub_pulse(g_info):
    """Monitors the threads and clients used in this job and its statuses"""
    try:
        if "p_info" not in g_info["info"]["pulse"]:
            g_info["info"]["pulse"]["p_info"] = {"jid": g_info["jid"],
                                                            "name": g_info["job_name"], "pid": os.getpid(),
                                                            "p_pid": os.getppid(), "thread": {}, "client": {}}
        if "level" not in g_info["info"]["pulse"]:
            g_info["info"]["pulse"]["level"] = "usual"

        for tid, thread in g_info["info"]["thread"].items():
            if thread["con"] not in ('', None):
                g_info["info"]["pulse"]["p_info"]["thread"][tid] = thread["con"].is_alive()
            else:
                g_info["info"]["pulse"]["p_info"]["thread"][tid] = False

            if not g_info["info"]["pulse"]["p_info"]["thread"][tid]:
                g_info["info"]["pulse"]["level"] = "unusual"
                recover_thread(tid, g_info)

        for cid, client in g_info["info"]["client"].items():
            g_info["info"]["pulse"]["p_info"]["client"][cid] = client["flag"]
            if not g_info["info"]["pulse"]["p_info"]["client"][cid]:
                if "thread" in g_info["info"]["client"][cid]["config"] and \
                        g_info["info"]["client"][cid]["config"]["thread"] not in ("", None):
                    thread_id = g_info["info"]["client"][cid]["config"]["thread"]
                    g_info["info"]["pulse"]["level"] = "unusual"
                    if g_info["info"]["thread"][thread_id]["con"] not in ("", None) and \
                            g_info["info"]["thread"][thread_id]["con"].is_alive():
                        verify_connection(cid,
                                                g_info["info"]["client"][cid]["config"][
                                                    "typ"], g_info)
                    else:
                        recover_thread(thread_id, g_info)
                else:
                    g_info["info"]["pulse"]["level"] = "unusual"
                    verify_connection(cid,
                                            g_info["info"]["client"][cid]["config"]["typ"], g_info)
        if g_info["info"]["pulse"]["level"] == "unusual":
            g_info["job_pulse"]["pub_flag"] = False
            pulse_publish(g_info)
        else:
            if not g_info["job_pulse"]["pub_flag"]:
                g_info["job_pulse"]["pub_flag"] = True
                pulse_publish(g_info)
            else:
                if (datetime.now().timestamp() - g_info["job_pulse"]["last_update"]) > \
                        g_info["job_pulse"]["publish_interval"]:
                    pulse_publish(g_info)
    except Exception:
        clog("", {"exc": str(traceback.format_exc())}, g_info)

def pulse_publish(g_info):
    """Frames and publishes the job related information and its status """
    try:
        pulse_obj = {
            "gid": g_info["gid"],
            "sid": g_info["sid"],
            "fid": g_info["facility"],
            "job": g_info["job_name"],
            "job_type": g_info["job_type"],
            "ctx": "sub_process",
            "level": g_info["info"]["pulse"]["level"],
            "etm": datetime.now().timestamp(),
            "p_info": g_info["info"]["pulse"]["p_info"]
        }
        pulse_obj["p_info"]["p_per"] = sub_process_info()
        g_info["job_pulse"]["last_update"] = datetime.now().timestamp()
        g_info["info"]["client"][g_info["info"]["debug"]["log_client"]]["con"].publish(g_info["info"]["debug"]["p_topic"], 
            str(data_encrypt(pulse_obj, g_info["private_key"])))
        g_info["p_info"] = {}
        g_info["info"]["pulse"]["level"] = "usual"
    except Exception:
        clog("", {"exc": str(traceback.format_exc())}, g_info)

def recover_thread(key, g_info):
    """Reconnects the threads which are disconnected
    params:
    key: A string identifier that uniquely identifies the threads
    """
    try:
        if "recovery" not in g_info["info"]["pulse"]["p_info"]:
            g_info["info"]["pulse"]["p_info"]["recovery"] = []
        temp = {"type": "thread", "id": key}
        if g_info["info"]["thread"][key]["config"]["client"] != "":
            cli = g_info["info"]["thread"][key]["config"]["client"]
            g_info["info"]["client"][cli][
                "flag"] = False  # if thread itself is not alive then the con flag must be false
        g_info["info"]["debug"]["thread_start"](key)
    except Exception:
        clog("", {"exc": str(traceback.format_exc())}, g_info)
        temp.update({"status": "not_recovered", "comments": "Thread Restart Failed"})
        g_info["info"]["pulse"]["p_info"]["recovery"].append(temp)
        return False
    else:
        temp.update({"status": "recovered", "comments": "Thread Not Alive-Restarted"})
        g_info["info"]["pulse"]["p_info"]["recovery"].append(temp)
        return True

def verify_connection(cid, broker_typ, g_info):
    def on_connect(client, userdata, flags, rc):
        """Connects to the MQTT client temporarily
        params:
        rc: 0- connected, 1- not connected
        """
        try:
            if "recovery" not in g_info["info"]["pulse"]["p_info"]:
                g_info["info"]["pulse"]["p_info"]["recovery"] = []
            temp = {"type": "client", "id": userdata["client_id"]}
            if rc == 0:
                clog("", {"msg": "Job Temp Connection Connected"}, g_info)
                client.connected_flag = True
                g_info["info"]["client"][userdata["client_id"]]["con"].reconnect()
                temp.update({"status": "recovered", "comments": "Client Not Alive- Reconnected"})
                g_info["info"]["pulse"]["p_info"]["recovery"].append(temp)
                client.disconnect()
            else:
                clog("", {"msg": "Job Temp Connection Not Connected"}, g_info)
                client.connected_flag = False
                temp.update({"status": "not_recovered", "comments": "Broker Down"})
                g_info["info"]["pulse"]["p_info"]["recovery"].append(temp)
        except Exception:
            clog("", {"exc": str(traceback.format_exc())}, g_info)

    def on_disconnect(client, userdata, rc):
        """Disconnects from the MQTT client
        params:
        rc: 0- connected, 1- not connected
        """
        try:
            client.connected_flag = False
            clog("", {"msg": "Job Temp Connection Disconnected"}, g_info)
        except Exception:
            clog("", {"exc": str(traceback.format_exc())}, g_info)

    
    """Establishes a MQTT client connection and validates SSL or Mutual Authentication if enabled prior
    connecting
    cid: A string identifier that defines client for which the temporary connection is to established
    broker_typ: A string defining the type of broker to be connected
    """
    try:
        client_userdata = {'client_id': cid}
        temp_client = mqtt.Client(client_id=g_info["broker"][broker_typ]["client_name"] + str(random_string()),
                                    userdata=client_userdata)
        temp_client.on_connect = on_connect
        temp_client.on_disconnect = on_disconnect
        if "ssl" in g_info["broker"][broker_typ] and "ca_path" in \
                g_info["broker"][broker_typ]:
            if g_info["broker"][broker_typ]["ssl"] and path.exists(
                    g_info["broker"][broker_typ]["ca_path"]):
                ssl_context = ssl.create_default_context(cafile=g_info["broker"][broker_typ]["ca_path"])
                if g_info["broker"][broker_typ]["ma"] and "cert_path" in \
                        g_info["broker"][broker_typ] and "key_path" in \
                        g_info["broker"][broker_typ]:
                    if path.exists(g_info["broker"][broker_typ]["cert_path"]) and path.exists(
                            g_info["broker"][broker_typ]["key_path"]):
                        ssl_context.load_cert_chain(certfile=g_info["broker"][broker_typ]["cert_path"],
                                                    keyfile=g_info["broker"][broker_typ]["key_path"])
                ssl_context.check_hostname = False
                temp_client.tls_set_context(ssl_context)
        temp_client.username_pw_set(username=g_info["broker"][broker_typ]["username"],
                                    password=g_info["broker"][broker_typ]["password"])
        broker = g_info["broker"][broker_typ]["host"]
        temp_client.connect(broker)
        temp_client.loop_forever()
    except Exception:
        clog("", {"exc": str(traceback.format_exc())}, g_info)


def job_ack_process(data, ack_flag, cmnts, g_info):
    """ Updates the local sqlite db with the table id given
    I/P params:
    job_data: an object with necessary job related information
    ack_flag: a boolean flag that signifies that the job is started properly
    cmnts: a string that defines the reason for failure incase the ack_flag = false
    """
    try:
        def update_process(upd_data):
            cur.execute(
                "UPDATE process_history SET evtdt=?, last_communicated_on=?, acknowledge=? , acknowledge_time =? , "
                "remarks =? WHERE id = ?",
                upd_data[0])
            db.commit()
            cur.close()

        table_process_history_exist = "SELECT name FROM sqlite_master WHERE type='table' AND name='process_history'"
        db = sqlite3.connect(g_info["db_path"])
        cur = db.cursor()
        if cur.execute(table_process_history_exist).fetchone() is not None:
            query = """select * from process_history where id = """ + str(data["table_id"])
            cur.execute(query)
            records = cur.fetchall()
            if len(records) > 0:
                if os.getppid() == records[0][3] and data["jid"] == records[0][4]:
                    ack = "Y" if ack_flag else "N"
                    ins_data = [{
                        "evtdt": datetime.now(),
                        "last_communicated_on": datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'),
                        "acknowledge": ack,
                        "acknowledge_time": datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'),
                        "remarks": cmnts,
                        "table_id": data["table_id"]
                    }]
                    put_data = [tuple(val.values()) for val in ins_data]
                    update_process(put_data)
                    clog("", {"msg": "Job ack update success", "data": put_data}, g_info)
        else:
            clog("", {"msg": "process_history table Doesn't exists"}, g_info)
    except Exception:
        clog("", {"exc": str(traceback.format_exc())}, g_info)
    else:
        cur.close()

# print(compute_page_size(1000, 3175))
# print(sub_process_info())
# url = "https://liveapi.trackerwave.com/live/api/pf-gateway/gw0011?serverId=5"
# auth = {'content-type': 'application/json', 'API_KEY': 'U7evNMPjsQENFdVEHA38Dh9pajcFlVj2vk60GAtFb0F83R3md0eFRrrtmqr1zkGXDBQpoSEUQdoNIiKLu0OckBEfwQ/+KSWSCTZNvvQ2AIN0cMW5AsvpNPDDGmhXprLi'}
# print(api_request("get", url, auth))

# print(random_string())
# print(data_encrypt("test",eval("b'NdwQvMq6F_Wjm-0rzshB_MiWQdvQoXcXUYCB1A2SCog='")))

# print(raw_data_adpter({"RSN":"100001950","ESWV":"1.22","SEQ":"45714","DATA":[{"TSN":"200008781","TYP":"BLE","RSSI":"-89","BCN":"fe6400000000000000000035","DTM":"1659698430"},{"TSN":"250050148","TYP":"BLE","RSSI":"-89","BCN":"10334a0bebe4530000000017","DTM":"1659698430"},{"TSN":"250050148","TYP":"BLE","RSSI":"-88","BCN":"10334a0bebe4530000000017","DTM":"1659698430"}]}))

# print(raw_data_adpter({"RSN":"100001965","MTI":"L1","DTM":"11","DATA":"200000003|BLE|-69,200000009|BLE|-80,200000003|BLE|-74,200000009|BLE|-75,200003558|BLE|-76"}))

# print(raw_data_adpter({"RSN":"100001965","MTI":"L2","TYP":"BLE","DTM":"11","DATA":"200000003|-69,200000009|-80,200000003|-74,200000009|-75,200003558|-76"}))

# print(raw_data_adpter({"MTI":"L3","TSN":"200006404","SEQ":"65700","DTM":"1660643091","TYP":"BLE","BCN":"005a32000000000000000013","DATA":[{"RSN":"100000115","RSSI":"-70"},{"RSN":"100000116","RSSI":"-71"}]}))

# print(raw_data_adpter({"MTI":"L4","TSN":"200006404","SEQ":"65700","DTM":"1660643091","TYP":"BLE","BCN":"005a32000000000000000013","DATA":"100000115|-70,100000116|-60"}))

# print(raw_data_adpter(
# {"RSN":"100001950","ESWV":"1.17","SEQ":"201","DATA":[{"TSN":"250009005","TYP":"BLE","RSSI":"-52","BCN":"40641E1C0000000000000011","DTM":"8717"},
# {"TSN":"E31AA560792A","TYP":"S3","WATCH":"02010617ff0a0a63000000618a854a00000000640061015c004e0103095333","RSSI":"-74","DTM":"1636453481"},
# {"TSN":"F6DF4F80D3D5","TYP":"SP","SMART_PLUG":"0a09313134422d6433643502010610ffff20d3d50bebc56945000000000000","RSSI":"-61","DTM":"1643358060"}]}))

# print(raw_data_adpter({"RSN":"100001906","ESWV":"6.20","SEQ":"54231","DATA":[{"SNO":"280022006","TYP":"ICT","CSNO":"200000759","TIME":1610286403,"DRN": 33,"SEQ":1,"LOC": "200000759","CV":"4","AT":"0","CRSSI":"-63"},{"SNO":"280022006","TYP":"ICT","CSNO":"200001434","TIME":1610286399,"DRN": 49,"SEQ":2,"LOC": "200001434","CV":"4","AT":"0","CRSSI":"-57"}]}))

# {"RSN":"100001906","ESWV":"6.20","SEQ":"54231","DATA":[{"SNO":"280022006","TYP":"ICT","CSNO":"200000759","TIME":1610286403,"DRN": 33,"SEQ":1,"LOC": "200000759","CV":"4","AT":"0","CRSSI":"-63"},{"SNO":"280022006","TYP":"ICT","CSNO":"200001434","TIME":1610286399,"DRN": 49,"SEQ":2,"LOC": "200001434","CV":"4","AT":"0","CRSSI":"-57"}]}

