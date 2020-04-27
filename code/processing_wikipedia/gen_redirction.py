import mysql.connector

path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/'
redrict_file = path + 'redrict_file1.txt'

mydb = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = '**&'
	)
print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SELECT depages.page.page_title, redirect.redirect.rd_title FROM depages.page, redirect.redirect where depages.page.page_id = redirect.redirect.rd_from;")

myresult = mycursor.fetchall()

with open(redrict_file, 'w') as r:
	for x in myresult:
    		r.write(str(x[0]) + '\t'  + str(x[1]) + '\n')