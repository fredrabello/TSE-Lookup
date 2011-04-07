import re

import urllib
from BeautifulSoup import BeautifulSoup
import sqlite3

database = 'data/tselookup.sqlite'
db_doacoes = 'data/doacoes.sqlite'

class Empresa:
	def __init__(self, name, cnpj):
		self.name = name
		self.cnpj = cnpj

class Doacao:
	def __init__(self, name, cnpj, value, candidate, date, party, candidate_alias=''):
		self.name = name
		self.cnpj = cnpj
		self.value = value
		self.candidate = candidate
		self.date = date
		self.party = party
		self.candidate_alias = candidate_alias

class Article:
	def __init__(self, url):
		self.url = url
		self.story = self.getStory(url)
		self.title = self.story.html.head.title.renderContents()

	def getStory(self, url):
		html = urllib.urlopen(url)
		print 'Carregando pagina...'
		unicode(html)
		story = BeautifulSoup(html)
		return story

	def checkStory(self, companies):
		results = []
		for company in companies:
			hit = self.story.find(text=re.compile(company.name+'\s|' + company.name + ',|' + company.name + '\.'))
			if (hit):
				results.append(company)
		self.hits = list(results)

	def checkDonations(self, conn):
		results = []
		c = conn.cursor()
		for hit in self.hits:
			tmp_result = c.execute('''select name, cnpj, value, candidate, date, party from doacoes where cnpj=?''', [hit.cnpj])
			tmp_result = tmp_result.fetchall()			
			company = { 'name' : tmp_result[0][0],
				    'fantasy_name': hit.name,
				    'donations' : []}
			total = 0
			for r in tmp_result:
				valor = int(r[2].encode('utf-8').translate(None,'R$.,'))				
				company['donations'].append(Doacao(r[0], r[1], r[2], r[3], r[4], r[5]))
				total = valor + total
			company['total'] = total	
			results.append(company)

		c.close()
		return results

def connectDb(arquivo):
	conn = sqlite3.connect(arquivo)
	return conn

def loadEmpresas(conn):
	c = conn.cursor()
	c.execute('select nome, cnpj from empresas')
	results = []
	companies = c.fetchall()
	for company in companies:
		results.append(Empresa(company[0],company[1]))
	c.close()
	return results





