#!/usr/bin/python
import csv
import webapp
import os

class acortador(webapp.webApp):
	DiccURL = {}
	DiccNum = {}

	def parse(self,request):
		metodo = request.split(' ',1)[0]
		recurso = request.split(' ',2)[1]
		cuerpo = request.split('\r\n\r\n')[1]
		return (metodo, recurso, cuerpo)

	def process(self,peticion):
		metodo, recurso, cuerpo = peticion

		if metodo == 'GET': # ESTA CONDICION VE QUE EL DICCIONARIO1 ESTE VACIO Y QUE EXISTA O NO EL FICHERO
			if not self.DiccURL and os.access('url.csv', os.R_OK):# existe fichero csv:
				ifile = open('url.csv','r')
				reader = csv.reader(ifile)
				for index, row in enumerate(reader):
					self.DiccURL[row[0]] =row[1]
					self.DiccNum[row[1]] = row[0]
			if recurso == '/':
				httpCode = '200 OK'
				htmlBody = '<html><body>'
				htmlBody += '<form method="POST" action="">'
				htmlBody += '<input type = "text" name="ULRs">'
				htmlBody += '<input type ="submit" value="Enviar">'	
				for num in self.DiccNum:
					htmlBody += '<p>'+self.DiccNum[num]+' : '+num+'</p>'			
				htmlBody += '</form></body></html>'
			else:
				if recurso[1:] in self.DiccNum:
					print recurso[1:]
					httpCode = '302 Found\r\nLocation: '+self.DiccNum[recurso[1:]]
					htmlBody = " "
				else:
					httpCode = '404 Not Found'
					htmlBody = 'Not Found'
		elif metodo == 'POST':
			cuerpo = cuerpo.split('=')[1]
			if not cuerpo.startswith('http://'):
				cuerpo = "http://" + cuerpo #guarda la clave "cuerpo" al segundo diccionario

			if cuerpo not in self.DiccURL:
				self.DiccURL[cuerpo] = len(self.DiccNum)
				self.DiccNum[len(self.DiccURL)] = cuerpo
				#escribo en el fichero TODO EL DICCIONARIO
				m2  = open('url.csv','a')
				m2_c = csv.writer(m2)
				l = [cuerpo,self.DiccURL[cuerpo]]
				m2_c.writerow(l)
				m2.close()
			httpCode = "200 OK"
			htmlBody = '<html><body>'
			htmlBody += cuerpo +' = <a href="http://localhost:1234/'
			htmlBody += str(self.DiccURL[cuerpo])+'">'+str(self.DiccURL[cuerpo])+'</a>'
			htmlBody += '</html></body>'
		return (httpCode, htmlBody)  
if __name__ == "__main__":
	main = acortador("localhost", 1234)

