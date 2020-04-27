import mysql.connector

mydb = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = '1984Luke&'
	)
print(mydb)

path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/'
inputfile = path+'dewiki-20200101-page_props.1'
outputfile = path+'QID0401_1.txt'
outputfile1 = path+'PID0401_1.txt'
redrict_file = path + 'redrict_file.txt'

Qid = {}
Pid = {}
mycursor = mydb.cursor()

#mycursor.execute("select distinct pp_value from wikipageprops.page_props where pp_propname = 'wikibase_item'")
#mycursor.execute("SELECT * FROM entity_usage.wbc_entity_usage")
mycursor.execute("SELECT * FROM redirect.redirect;")

myresult = mycursor.fetchall()
print("Pid", len(Pid))
with open(redrict_file, 'w') as r:
	for x in myresult:
    		r.write(str(x) + '\n')

'''for x in myresult:
    	if 'Q' in x[1]:
		Qid[x[1]] = ''
		Pid[x[3]] = ''
print("Qid", len(Qid))
print("Pid", len(Pid))
with open(outputfile, 'w') as q, open(outputfile1, 'w') as p:
	for l in Qid:
		q.write(str(l)+ '\n')
	for l in Pid:
		p.write(str(l)+ '\n')'''
'''print(len(myresult))
with open(outputfile ,'w') as out:
	for x in myresult:
		out.write(str(x[0]) + '\n')
    		
print('mapping finished')'''


'''with open(outputfile, 'w') as out:
	for x in myresult:
		line = str(x[0]) + '\t' + str(x[1]) + '\n'
		out.write(line)
print('mapping finished')'''