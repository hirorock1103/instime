# import sys
# sys.path.append(r"c:\users\user\appdata\local\programs\python\python37-32\lib\site-packages")
import eel
import sqlite3
from selenium import webdriver

class Driver:
	path = r"C:\Users\USER\Desktop\chromedriver_win32 (2)/chromedriver.exe"

	def open(self, url):
		driver = webdriver.Chrome(self.path)
		driver.get(url)


def main():
	print("起動成功")
	eel.init("web")
	eel.start("postlist.html")


@eel.expose
def bt_launch_instagram(url):
	print(url)
	driver = Driver()
	driver.open(url)


@eel.expose
def bt_launch_get_post(kw):
	print(kw)
	from subprocess import Popen
	cmd = "py scroll.py " + kw
	proc = Popen(cmd, shell=True)


@eel.expose
def bt_search_post_list(keyword, hashtag):
	print("bt_search_post_list")
	con = sqlite3.connect('sample.db')
	cursor = con.cursor()

	formWordKeyWord = keyword
	formWordHashTag = hashtag

	bt1_s = formWordKeyWord.split(",")

	query = ""
	query2 = ""
	args = ""
	if formWordKeyWord == "" and formWordHashTag == "":
		query2 = "SELECT * FROM SampleGetPostList ORDER BY id ASC"

	elif formWordKeyWord != "" and formWordHashTag == "":

		if bt1_s.__len__() > 1:
			query2 = "SELECT * FROM SampleGetPostList"

			bt1_args = []
			where = ""
			for b in bt1_s:
				if where == "":
					where += " WHERE word like ? "
				else:
					where += " or word like ? "

				bt1_args.append("%" + b + "%")

			query2 += where
			query2 += " ORDER BY id ASC"
			args = bt1_args

		else:
			query2 = "SELECT * FROM SampleGetPostList" + " WHERE word like ?  ORDER BY id ASC"
			args = ("%" + formWordKeyWord + "%",)

	elif formWordKeyWord == "" and formWordHashTag != "":
		query2 = "SELECT * FROM SampleGetPostList" + " WHERE h_tags like ?  ORDER BY id ASC"
		args = ("%" + formWordHashTag + "%",)

	else:
		query2 = "SELECT * FROM SampleGetPostList" + " WHERE word like ? AND h_tags like ?  ORDER BY id ASC"
		args = ("%" + formWordKeyWord + "%", "%" + formWordHashTag + "%",)

	if args != "":
		cursor.execute(query2, args)
	else:
		cursor.execute(query2)

	eel.delete_rows()

	for row in cursor:
		try:
			dataId = row[0]
			word = row[1]
			postDate = row[2]
			url = row[3]
			user = row[4]
			tag = row[5]
			create = row[7]
			converted_post_date = row[6]

			# create row
			print(word)
			print(url)
			eel.add_record(dataId, word, url, tag, user, converted_post_date)

		except:
			print("err")

	return True

@eel.expose
def bt_start_hashtag():
	from subprocess import Popen
	cmd = "py hashtagsearch.py "
	proc = Popen(cmd, shell=True)
	print("pid: " + str(proc.pid))



if __name__ == "__main__":

	main()


