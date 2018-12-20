import time
import json
import traceback
import logging
import clipboard
import sys

from wox import Wox, WoxAPI

LOG_FILE = "./logs/log_tips.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE,
                    filemode='a')

class Main(Wox):
    TIPS_FILE = "./DB/tips.json"

    def query(self, key):

        if key == "":
            return self.list_tips()
        if key in "delete":
            return self.list_delete_tips()

        results = []
        results.append({
            "Title": 'stroe tip : "%s"' % key,
            "SubTitle": 'tips : "%s"' % key,
            "IcoPath": "Images/pic.png",
            "JsonRPCAction": {
                "method": "store_tip",
                "parameters": [key],
                "dontHideAfterAction": True
            }
        })

        return results

    def store_tip(self, info):
        try:
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tip = {"tip": info, "updated_time": times}
            with open(self.TIPS_FILE, "a") as f:
                f.write(json.dumps(tip) + "\n")
            WoxAPI.change_query("tip")
        except:
            logging.error(traceback.format_exc())

    def get_tips(self):
        try:
            results = []
            with open(self.TIPS_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        tip = json.loads(line.strip())
                        results.append({"tip": tip['tip'], "updated_time": tip['updated_time']})
            return reversed(results)
        except:
            logging.error(traceback.format_exc())

    def list_delete_tips(self):
        tips = self.get_tips()
        results = []
        for tip in tips:
            results.append({
                "Title": "delete %s" % tip['tip'],
                "SubTitle": tip['updated_time'],
                "IcoPath": "Images/pic.png",
                "JsonRPCAction": {
                    "method": "delete_tip",
                    "parameters": [tip['updated_time']],
                    "dontHideAfterAction": True
                }
            })
        return results

    def delete_tip(self, times):
        try:
            tips = []
            with open(self.TIPS_FILE, "r") as f:
                for line in f:
                    tips.append(json.loads(line.strip()))
            for tip in tips:
                if times == tip["updated_time"]:
                    tips.remove(tip)
                    break
            with open(self.TIPS_FILE, "w") as f:
                for tip in tips:
                    f.write(json.dumps(tip) + "\n")
            WoxAPI.change_query("tip")
        except:
            logging.error(traceback.format_exc())

    def list_tips(self):
        tips = self.get_tips()
        results = []
        for tip in tips:
            results.append({
                "Title": tip['tip'],
                "SubTitle": tip['updated_time'],
                "IcoPath": "Images/pic.png",
                "JsonRPCAction": {
                    "method": "copy_to_clip",
                    "parameters": [tip['tip']],
                    "dontHideAfterAction": False
                }
            })
        return results

    def copy_to_clip(self, text):
        clipboard.copy(text)


if __name__ == "__main__":
    Main()
