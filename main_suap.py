import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import json
import requests
from getpass import getpass
from os import system
from time import sleep
op = 0
login = ''
senha = ''
ano = ''
per = ''

class boletim(QDialog):

	def _init_ (self,parent=None):
		super(boletim,self)._init_(parent)
		uic.loadUi('tela3.ui',self)
		global ano, per
		self.meuboletim.addItem('Período: ' + ano + '.' + per)
		self.back.clicked.connect(self.voltar)
		self.end.clicked.connect(self.close)

		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			notas = resp.json()
			for x in notas:
				self.meuboletim.addItem(x['disciplina'])
				self.meuboletim.addItem('\t\tNota 1: ' + str(x['nota_etapa_1']['nota']) +'\t\t\tNota 2: ' + str(x['nota_etapa_2']['nota']))
				self.meuboletim.addItem('\t\tNota 3: ' + str(x['nota_etapa_3']['nota']) +'\t\t\tNota 4: ' + str(x['nota_etapa_4']['nota']))
				self.meuboletim.addItem('\t\tMédia Final: '+ str(x['media_final_disciplina']))

	def close(self):
		sys.exit()

	def voltar(self):
		t=SUAP(self)
		t.activateWindow()
		self.hide()
		t.exec_()

class mails(QDialog):
	def _init_ (self,parent=None):
		super(mails,self)._init_(parent)
		uic.loadUi('tela4.ui',self)
		global ano, per
		self.back.clicked.connect(self.voltar)
		self.end.clicked.connect(self.close)
		self.meuscontatos.addItem('Período: ' + ano + '.' + per)
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			notas = resp.json()
			for x in notas:
				cod=str(x['codigo_diario'])
				resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turmas-virtuais/%s/'%cod, auth=(login,senha))
				if resp.status_code == 200:
					turma = resp.json()
					for x in turma['professores']:
						self.meuscontatos.addItem('Nome: ' + x['nome'] + '\nEmail: ' + x['email'] + '\n')

	def close(self):
		sys.exit()

	def voltar(self):
		t=SUAP(self)
		t.activateWindow()
		self.hide()
		t.exec_()


class SUAP(QDialog):
	def _init_(self,parent=None):
		super(SUAP, self)._init_(parent)
		uic.loadUi('tela1.ui',self)
		self.func1.clicked.connect(self.getMat)
		self.func2.clicked.connect(self.notas)
		self.func3.clicked.connect(self.emails)
		self.func4.clicked.connect(self.close)

	def notas(self):
		global ano, per, login, senha, notas
		ano = self.ano.text()
		per = self.periodo.text()
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			e=boletim()
			e.activateWindow()
			self.hide()
			e.exec_()
		else:
			self.mensagem.setText('Ocorreu um erro, verifique os dados e tente novamente')

	def emails(self):
		global ano, per, login, senha, notas
		ano = self.ano.text()
		per = self.periodo.text()
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			e=mails()
			e.activateWindow()
			self.hide()
			e.exec_()
		else:
			self.mensagem.setText('Ocorreu um erro, verifique os dados e tente novamente')

	def close(self):
		sys.exit()

	def getNot(self):
		global ano, per, login, senha, notas
		ano = self.ano.text()
		per = self.periodo.text()
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			notas = resp.json()
		else:
			self.mensagem.setText('Ocorreu um erro, verifique os dados e tente novamente')
			notas = resp.json()
		return notas

	def getMat(self):
		self.mensagem.setText('Aguarde...')
		global login,senha
		notas = self.getNot()
		for x in notas:
			if x!='detail':
				cod=str(x['codigo_diario'])
				resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turmas-virtuais/%s/'%cod, auth=(login,senha))
				if resp.status_code == 200:
					turma = resp.json()
					diretorio = x['disciplina'].replace('/','-').split(' ')
					diretorio = '_'.join(diretorio)
					system ('mkdir -p %s-%s/'%(ano,per) + diretorio )
					for x in turma['materiais_de_aula']:
						if x['url'][0]=='/':
							link = 'https://suap.ifrn.edu.br' +(x['url'])
							system ('wget -P ' + '%s-%s/'%(ano,per)+ diretorio + ' ' + link)
						else:
							link = x['url']
							system ('echo ' + link + ' > %s-%s/'%(ano,per) + diretorio + '/Link de materiais')
					self.mensagem.setText('Realizado')
				elif resp.status_code == 404:
					self.mensagem.setText('Ocorreu um erro, tente novamente')
			else:
				self.mensagem.setText('Ocorreu um erro, tente novamente')
		return
