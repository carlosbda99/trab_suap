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
		t.exec_()
