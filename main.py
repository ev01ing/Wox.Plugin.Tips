# coding:utf-8
from wox import Wox
import sqlite3
import time
import traceback
import clipboard

class Main(Wox):
	DB_NAME = "./DB/Tips.db"
	LOG_FILE = "./logs/error.txt"

	def query(self, key):
		if key == "":
			return self.list_tips()
		if key in "delete":
			return self.list_delete_tips()
		results = []
		results.append({
			"Title": "stroe tip : %s" % key,
			"SubTitle": u"tips: %s" % key,
			"IcoPath": "Images/pic.png",
			"JsonRPCAction":{
				"method": "store_tip",
				"parameters": [key, ],
				"dontHideAfterAction": False
			}
		})
		return results

	def store_tip(self, info):
		try:
			conn = sqlite3.connect(self.DB_NAME)
			conn.execute("CREATE TABLE IF NOT EXISTS tips (id INTEGER PRIMARY KEY , tip TEXT, updated_time TEXT);")
			times = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
			conn.execute("insert into tips (tip, updated_time) values (?, ? );", (info, times))
			conn.commit()
			conn.close()
		except:
			self.log_error("store_tip")


	def get_tips(self):
		try:
			conn = sqlite3.connect(self.DB_NAME)
			cursor = conn.execute("select * from tips order by id desc;")
			results = []
			for item in cursor:
				results.append({"id": item[0], "tip": item[1], "updated_time": item[2]})
			conn.close()
			return results
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
					"parameters": [tip['id']],
					"dontHideAfterAction": False
				}
			})
		return results

	def delete_tip(self, id):
		try:
			conn = sqlite3.connect(self.DB_NAME)
			conn.execute("delete from tips where id = %s;" % str(id))
			conn.commit()
			conn.close()
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
				"JsonRPCAction":{
					"method": "copy_to_clip",
					"parameters": [key, ],
					"dontHideAfterAction": False
				}
			})
		return results

	def copy_to_clip(self, text):
		clipboard.copy(text)

	def log_error(self, fun_str):
		with open(self.LOG_FILE, "a") as f:
			f.write("%s: \n%s" % (fun_str, traceback.format_exc()))

if __name__ == "__main__":
	Main()
