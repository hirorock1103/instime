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
