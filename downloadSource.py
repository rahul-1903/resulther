import lxml.html, sys, time, os
from bs4 import BeautifulSoup
from mechanize import Browser

#getting the form attribute
def select_form(form):
    return form.attrs.get('id',None)=='form1'

#url for downloading the data
url = "http://61.12.70.61:8084/"

#filename
filename = "result.txt"

def result(number):
    br = Browser()
    br.open(url)
    br.select_form(predicate=select_form)
    # inserting the roll number and semester
    br['roll'] = str(number)
    br['sem'] = ['2']

    # submiting and storing the source code in resp
    resp = br.submit()

    soup = BeautifulSoup(resp, "lxml").prettify()
    l = soup.split('\n')
    msg = l[3].strip()
    if msg != "No such student exists in this database":
        sgpa1, sgpa2 = l[326].split(), l[333].split()
        reg, name, ygpa = l[77].split(), l[72].split(), l[340].split()
        return (reg[-1]), " ".join(name[2:]), "".join(sgpa1[-1]), "".join(sgpa2[-1]), "".join(ygpa[-1])
    else:
        return None
    
file = open(filename, "w")
file.write("%-5s%-12s%-25s%-7s%-6s%-6s\n"%("Rank", "Roll No.", "Name", "Odd", "Even", "YGPA"))
file.close()
print("Creating a file...")
time.sleep(1)
print("Writing data to the file...")
'''
print ("Writing {} data to file...".format(int(sys.argv[2]) - int(sys.argv[1]) + 1))
time.sleep(1)
print ("Waiting...")
if len(sys.argv) < 3:
    print "Usage: python downloadSource.py [InitialRollNo] [FinalRollNo]"
    exit()
'''
#creating a list to store details
l = []

#for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
def res(a, b):
    total = b - a + 1
    for i in range(a, b):
        time.sleep(0.5)
        if i>0:
            perComplete = ((float(i-a)/total)*100)
            if(perComplete % 5 == 0):
                print ("Completed {}% ".format(perComplete))
        x = result(i)
        if(x != None and len(x) == 5):
            m = [x[0], str(x[1]), float(x[2]), float(x[3]), float(x[4])]
            l.append(m)
    print("Finished Writing...")
    print ("Data saved to " + os.getcwd() + "\\" +filename)

    #sorting the data in descending order of YGPA
    l.sort(key=lambda x: x[4], reverse=True)

    rank = 1
    for i in range(len(l)):
        file = open(filename, 'a')
        if (i >= 1 and l[i][4] != l[i-1][4]):
            rank += 1
        file.write ("%-4d%-12s%-25s%-7.2f%-7.2f%-7.2f\n"%(rank, l[i][0], l[i][1], l[i][2], l[i][3], l[i][4]))
        file.close()

# Roll Numbers of the various departments
compStart, compEnd = 12616001001, 12616001188   #for computer science and engineering
civilStart, civilEnd = 12616013001, 12616013121   # for civil

#calling res function
res(compStart, compEnd)
