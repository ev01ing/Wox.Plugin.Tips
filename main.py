# coding:utf-8
from wox import Wox
import time
import json
import traceback
import clipboard
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Main(Wox):
    LOG_FILE = "./logs/error.txt"
    TIPS_FILE = "./DB/tips.json"

    def query(self, key):

        with open("temp.txt", "a") as output:
            output.write(key + "\n")

        if key == "":
            return self.list_tips()
        if key in "delete":
            return self.list_delete_tips()

        results = []
        results.append({
            "Title": u"stroe tip : %s" % key,
            "SubTitle": u"tips: %s" % key,
            "IcoPath": "Images/pic.png",
            "JsonRPCAction": {
                "method": "store_tip",
                "parameters": [key, ],
                "dontHideAfterAction": False
            }
        })

        return results

    def store_tip(self, info):
        try:
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tip = {"tip": info, "updated_time": times}
            with open(self.TIPS_FILE, "a") as f:
                f.write(json.dumps(tip) + "\n")
        except:
            self.log_error("store_tip")

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
            self.log_error("get_tips")

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
                    "dontHideAfterAction": False
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
        except:
            self.log_error("delete_tip")

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
        with open("temp.txt", "a") as f:
            for item in results:
                f.write(json.dumps(item) + "\n")
        return results

    def copy_to_clip(self, text):
        clipboard.copy(text)

    def log_error(self, fun_str):
        with open(self.LOG_FILE, "a") as f:
            f.write("%s: \n%s" % (fun_str, traceback.format_exc()))


if __name__ == "__main__":
    Main()
