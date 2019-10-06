from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://pythonclock.org')

#run without javascript rendering
tmp = r.html.search('Python 2.7 will retire in...{}Enable Guido Mode')[0]
print("run without javascript rendering ",tmp)
print("")

#Run With Javascript Rendering
r.html.render()
tmp = r.html.search('Python 2.7 will retire in...{}Enable Guido Mode')[0]
print("run with javascript rendering ",tmp)