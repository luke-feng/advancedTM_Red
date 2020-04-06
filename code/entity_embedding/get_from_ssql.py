import mysql.connector

mydb = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = '**&'
	)
print(mydb)

path = '../end2end_neural_el/deep-ed/basic_data/'
inputfile = path+'dewiki-20200101-page_props.1'
outputfile = path+'mapping.txt'

mycursor = mydb.cursor()
mycursor.execute("select pp_page, pp_value from wikipageprops.page_props where pp_propname = 'wikibase_item'")
myresult = mycursor.fetchall()
with open(outputfile, 'w') as out:
	for x in myresult:
		line = str(x[0]) + '\t' + str(x[1]) + '\n'
		out.write(line)
print('mapping finished')