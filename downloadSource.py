import requests, urllib, lxml.html, ctypes, re, sys, time, os
from bs4 import BeautifulSoup
from mechanize import Browser
#getting the form attribute
def select_form(form):
    return form.attrs.get('id',None)=='form1'
url = "http://61.12.70.61:8084/"

def result(number):
    br = Browser()
    br.open(url)
    br.select_form(predicate=select_form)
    br['roll'] = str(number)    #inserting the roll number and semester
    br['sem'] = ['2']
    resp = br.submit() # submiting and storing the source code in resp
    soup = BeautifulSoup(resp, "lxml").prettify()
    l = soup.split('\n')
    #print l[77].strip(), l[72].strip(), l[340].strip()
    msg = l[3].strip()
    if msg != "No such student exists in this database":
        reg, name, ygpa = l[77].split(), l[72].split(), l[340].split()
        return (reg[-1]), " ".join(name[2:]), "".join(ygpa[-1])
    else :
        return "Roll {} does not exist".format(number)

compStart, compEnd = 12616001001, 12616001200     #for computer science and engineering
civilStart, civilEnd = 12616013001, 12616013121   # for civil
#filename = "file.txt"
filename = "result.txt"
file = open(filename, "w")
file.write("Roll\t\tName\t\tYGPA\n")
file.close()
print("Creating a file...")
time.sleep(1)
print ("Writing {} data to file...".format(int(sys.argv[2]) - int(sys.argv[1]) + 1))
time.sleep(1)
print ("Waiting...")
if len(sys.argv) < 3:
    print "Usage: python downloadSource.py [InitialRollNo] [FinalRollNo]"
    exit()
for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
    file = open(filename, "a")
    x = result(i)
    if(len(x) == 3):
        file.write("{} {} {}\n".format(x[0], x[1], x[2]))
    else:
        file.write("Roll No. {} does not exist.\n".format(i))
    #print x[0], x[1],x[2]
    file.close()
print("Finished Writing...")
print ("Data saved to " + os.getcwd() + "\\" +filename)
