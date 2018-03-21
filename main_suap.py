import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import json
import requests
from getpass import getpass
from os import system
from time import sleep
from datetime import datetime
hora = datetime.now()
op = 0
login = ''
senha = ''
ano = ''
per = ''
arq=open('test.json','w')
log = {'log':[]}

class boletim(QDialog):
	def __init__ (self,parent=None):
		super(boletim,self).__init__(parent)
		uic.loadUi('tela3.ui',self)
		global ano, per
		self.meuboletim.addItem('Período: ' + ano + '.' + per)
		self.back.clicked.connect(self.voltar)
		self.end.clicked.connect(self.close)
		link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per) + ' --> ' + str(hora.now())
		log['log'][-1][login][0]['enviados'].append(link)
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			notas = resp.json()
			for x in notas:
				self.meuboletim.addItem(x['disciplina'])
				var1 = x['disciplina'] + ' ' + str(hora.now())
				log['log'][-1][login][0]['recebidos'].append(var1)
				self.meuboletim.addItem('\t\tNota 1: ' + str(x['nota_etapa_1']['nota']) +'\t\t\tNota 2: ' + str(x['nota_etapa_2']['nota']))
				var2 = 'Nota 1: ' + str(x['nota_etapa_1']['nota']) +'        Nota 2: ' + str(x['nota_etapa_2']['nota']) + ' --> ' + str(hora.now())
				log['log'][-1][login][0]['recebidos'].append(var2)
				self.meuboletim.addItem('\t\tNota 3: ' + str(x['nota_etapa_3']['nota']) +'\t\t\tNota 4: ' + str(x['nota_etapa_4']['nota']))
				var3 = 'Nota 3: ' + str(x['nota_etapa_3']['nota']) +'        Nota 4: ' + str(x['nota_etapa_4']['nota']) + ' --> ' + str(hora.now())
				log['log'][-1][login][0]['recebidos'].append(var3)
				self.meuboletim.addItem('\t\tMédia Final: '+ str(x['media_final_disciplina']))
				var4 = 'Média Final: '+ str(x['media_final_disciplina']) + ' --> ' + str(hora.now())
				log['log'][-1][login][0]['recebidos'].append(var4)
	def close(self):
		json.dump(log,arq,indent=4)
		arq.close()
		sys.exit()

	def voltar(self):
		t=SUAP(self)
		t.activateWindow()
		self.hide()
		t.exec_()

class mails(QDialog):
	def __init__ (self,parent=None):
		super(mails,self).__init__(parent)
		uic.loadUi('tela4.ui',self)
		global ano, per
		self.back.clicked.connect(self.voltar)
		self.end.clicked.connect(self.close)
		self.meuscontatos.addItem('Período: ' + ano + '.' + per)
		link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per) + ' --> ' + str(hora.now())
		log['log'][-1][login][0]['enviados'].append(link)
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			notas = resp.json()
			for x in notas:
				cod=str(x['codigo_diario'])
				link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/%s/'%cod + ' --> ' + str(hora.now())
				log['log'][-1][login][0]['enviados'].append(link)
				resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/%s/'%cod, auth=(login,senha))
				if resp.status_code == 200:
					turma = resp.json()
					for x in turma['professores']:
						self.meuscontatos.addItem('Nome: ' + x['nome'] + '\nEmail: ' + x['email'] + '\n')
						var = 'Nome: ' + x['nome'] + '\nEmail: ' + x['email'] + '\n' + ' --> ' + str(hora.now())
						log['log'][-1][login][0]['recebidos'].append(var)

	def close(self):
		json.dump(log,arq,indent=4)
		arq.close()
		sys.exit()


	def voltar(self):
		t=SUAP(self)
		t.activateWindow()
		self.hide()
		t.exec_()


class SUAP(QDialog):
	def __init__(self,parent=None):
		super(SUAP, self).__init__(parent)
		uic.loadUi('tela1.ui',self)
		self.func1.clicked.connect(self.getMat)
		self.func2.clicked.connect(self.notas)
		self.func3.clicked.connect(self.emails)
		self.func4.clicked.connect(self.close)

	def notas(self):
		global ano, per, login, senha, notas
		ano = self.ano.text()
		per = self.periodo.text()
		link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per) + ' --> ' + str(hora.now())
		log['log'][-1][login][0]['enviados'].append(link)
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			e=boletim()
			e.activateWindow()
			self.hide()
			e.exec_()
		else:
			self.mensagem.setText('Erro, tente novamente')

	def emails(self):
		global ano, per, login, senha, notas
		ano = self.ano.text()
		per = self.periodo.text()
		link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per) + ' --> ' + str(hora.now())
		log['log'][-1][login][0]['enviados'].append(link)
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			e=mails()
			e.activateWindow()
			self.hide()
			e.exec_()
		else:
			self.mensagem.setText('Erro, tente novamente')

	def close(self):
		json.dump(log,arq,indent=4)
		arq.close()
		sys.exit()

	def getNot(self):
		global ano, per, login, senha, notas
		ano = self.ano.text()
		per = self.periodo.text()
		link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per) + ' --> ' + str(hora.now())
		log['log'][-1][login][0]['enviados'].append(link)
		resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(ano,per), auth=(login,senha))
		if resp.status_code == 200:
			notas = resp.json()
		else:
			self.mensagem.setText('Erro, tente novamente')
			notas = resp.json()
		return notas

	def getMat(self):
		global login,senha
		notas = self.getNot()
		for x in notas:
			if x!='detail':
				cod=str(x['codigo_diario'])
				link = 'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/%s/'%cod + ' --> ' + str(hora.now())
				log['log'][-1][login][0]['enviados'].append(link)
				resp = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/%s/'%cod, auth=(login,senha))
				if resp.status_code == 200:
					turma = resp.json()
					diretorio = x['disciplina'].replace('/','-').split(' ')
					diretorio = '_'.join(diretorio)
					system ('mkdir -p %s-%s/'%(ano,per) + diretorio )
					for x in turma['materiais_de_aula']:
						if x['url'][0]=='/':
							link = 'https://suap.ifrn.edu.br' +(x['url'])
							link2 = 'https://suap.ifrn.edu.br' +(x['url']) + ' --> ' + str(hora.now())
							log['log'][-1][login][0]['recebidos'].append(link)
							system ('wget -N -P ' + '%s-%s/'%(ano,per)+ diretorio + ' ' + link)
						else:
							link = x['url']
							link2 =  x['url'] + ' --> ' + str(hora.now())
							log['log'][-1][login][0]['recebidos'].append(link2)
							system ('echo ' + link + ' > %s-%s/'%(ano,per) + diretorio + '/Link de materiais')
					self.mensagem.setText('Download realizado')
				elif resp.status_code == 404:
					self.mensagem.setText('Erro, tente novamente')
		return

class Main(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		uic.loadUi('tela2.ui',self)
		self.auten.clicked.connect(self.autenticacao)

	def autenticacao(self):
		global login, senha
		login = self.matricula.text()
		log['log'].append({login:[{'recebidos':[],'enviados':[]}]})
		senha = self.senha.text()
		link = 'https://suap.ifrn.edu.br/api/v2/autenticacao/token/?format=json' + ' --> ' + str(hora.now())
		log['log'][-1][login][0]['enviados'].append(link)
		resp = requests.post('https://suap.ifrn.edu.br/api/v2/autenticacao/token/?format=json',json={'username': login, 'password': senha})

		if resp.status_code == 200:
			t=SUAP(self)
			t.activateWindow()
			self.hide()
			t.exec_()
		else:
			self.mensagem.setText('Usuario/senha invalido(a), tente novamente!')

if __name__ == '__main__':
	root = QApplication(sys.argv)
	app = Main()
	app.show()
	root.exec_()
