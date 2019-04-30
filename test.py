# import sys
# sys.path.append(r"c:\users\user\appdata\local\programs\python\python37-32\lib\site-packages")
import eel
import sqlite3
from selenium import webdriver

my_options = {
    'mode': "chrome-app", #or "chrome-app",
    'port': 0,
    # 'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
}

class Driver:
    path = r"C:\Users\USER\Desktop\chromedriver_win32 (2)/chromedriver.exe"

    def open(self, url):
        driver = webdriver.Chrome(self.path)
        driver.get(url)


def main():
    print("起動成功")
    eel.init("web")
    eel.start("index.html", options=my_options)


# ****************post list page******************

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
	count = 0
	for row in cursor:
		try:
			count += 1
			dataId = row[0]
			word = row[2]
			postDate = row[3]
			url = row[1]
			tag = row[4]
			user = row[5]
			create = row[7]
			converted_post_date = row[6]

			# create row
			eel.add_record(count, dataId, word, url, tag, user, converted_post_date)

		except:
			print("err")

	return True

@eel.expose
def bt_start_hashtag():
	from subprocess import Popen
	cmd = "py hashtagsearch.py "
	proc = Popen(cmd, shell=True)
	print("pid: " + str(proc.pid))

@eel.expose
def show_check_area():

	con = sqlite3.connect('sample.db')
	cursor = con.cursor()
	q = "SELECT word FROM SampleGetPostList GROUP BY word"
	cursor.execute(q)
	count = 0
	for row in cursor:
		count += 1
		eel.add_check_box(count, row[0])


@eel.expose
def create_post_list_file(fileName):
    print(fileName)




# ****************user list page******************
@eel.expose
def bt_launch_get_user(u):
	from subprocess import Popen
	cmd = "py getlist.py " + u
	proc = Popen(cmd, shell=True)
	print("pid: " + str(proc.pid))

@eel.expose
def bt_search_users(user, follower):

	con = sqlite3.connect('sample.db')
	cursor = con.cursor()

	query = "CREATE TABLE IF NOT EXISTS SampleGetUserList(id integer primary key AUTOINCREMENT, url text, user text, createdate text)"
	cursor.execute(query)

	formWordUser = user
	formWordFollower = follower

	query2 = ""
	args = ""
	if formWordUser == "" and formWordFollower == "":
		query2 = "SELECT * FROM SampleGetUserList ORDER BY id ASC"

	elif formWordUser != "" and formWordFollower == "":
		query2 = "SELECT * FROM SampleGetUserList" + " WHERE user like ?  ORDER BY id ASC"
		args = ("%" + formWordUser + "%",)

	elif formWordUser == "" and formWordFollower != "":
		query2 = "SELECT * FROM SampleGetUserList" + " WHERE url like ?  ORDER BY id ASC"
		args = ("%" + formWordFollower + "%",)

	else:
		query2 = "SELECT * FROM SampleGetUserList" + " WHERE user like ? AND url like ?  ORDER BY id ASC"
		args = ("%" + formWordUser + "%", "%" + formWordFollower + "%",)

	if args != "":
		cursor.execute(query2, args)
	else:
		cursor.execute(query2)

	eel.delete_user_rows()
	count = 0
	eel.add_user_record(count, "", "", "", "")
	for row in cursor:
		try:
			count += 1
			dataId = row[0]
			userId = row[2]
			follower = row[1]
			create = row[3]

			# create row
			eel.add_user_record(count, dataId, userId, follower, create)

		except:
			print("err")

	con.commit()



@eel.expose
def link(url):
	print(url)
	# eel.start(url, block=False)
	eel.browsers.open([url, ], options=my_options)


if __name__ == "__main__":
	main()


