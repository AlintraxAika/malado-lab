import streamlit as st
from playwright.sync_api import sync_playwright
from datetime import date
import datetime
import re

nl = '\n'

def text_cleaner(txt):
	exam_name = txt.strip().split('\n')[0]
	pattern = False
	string = ""
	txt = txt.replace('&nbsp;', ' ').replace('\xa0', ' ').replace('\t', ' ')
	try:
		if exam_name == "HEMOGRAMA COMPLETO":
			string = "HT: "
			pattern = re.search(r'HEMATOCRITO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += pattern.group(1)
			pattern = re.search(r'HEMOGLOBINA.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += "; HB: " + pattern.group(1)
			pattern = re.search(r'LEUCOCITOS.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += "; LCT: " + pattern.group(1)
			pattern = re.search(r'PLAQUETAS.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += "; PLQ: " + pattern.group(1)
		elif exam_name == "GRUPO SANGUÍNEO":
			string = "GS: "
			pattern = re.search(r'GRUPO SANGUINEO.*?:\s*([A-Z]+)', txt, re.IGNORECASE)
			string += pattern.group(1) + " "
			pattern = re.search(r'FATOR\s+RH\s*\(.*?\).*?:\s*([A-Z]+)', txt, re.IGNORECASE)
			string += pattern.group(1)
		elif exam_name == "DESIDROGENASE LÁCTICA":
			exam_name = "DHL: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
			string = string.replace("  ", " ")
		elif exam_name == "UREIA":
			exam_name = "UR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "CREATININA":
			exam_name = "CR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "BILIRRUBINA TOTAL E FRAÇÕES":
			string = "BT: "
			pattern = re.search(r'BILIRRUBINA\s+TOTAL.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string += pattern.group(1)
			pattern = re.search(r'BILIRRUBINA\s+DIRETA.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string += "; BD: " + pattern.group(1)
			pattern = re.search(r'BILIRRUBINA\s+INDIRETA.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string += "; BI: " + pattern.group(1)
		elif exam_name == "TRANSAMINASE OXALACÉTICA (TGO/AST)":
			exam_name = "AST: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "TRANSAMINASE PIRÚVICA (TGP/ALT)":
			exam_name = "ALT: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "RAZAO PROTEINA/CREATININA - URINA":
			exam_name = "PROT/CR: "
			pattern = re.search(r'RESULTADO:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "PROTEINURIA 24H":
			string = "PROT/24H: "
			pattern = re.search(r'RESULTADO:\s*([\d.,]+)\s*\w+/\w+', txt, re.IGNORECASE)
			string += pattern.group(1) + " MG (VOL: "
			pattern = re.search(r'VOLUME\s+URINARIO:\s*([\d.,]+)\s*mL', txt, re.IGNORECASE)
			string += pattern.group(1) + " ML)"
		elif exam_name == "ÁCIDO ÚRICO":
			exam_name = "AC. UR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "SÓDIO":
			exam_name = "NA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "POTÁSSIO":
			exam_name = "K: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "MAGNÉSIO":
			exam_name = "MG: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "AMILASE":
			exam_name = "AMILASE: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "LIPASE":
			exam_name = "LIPASE: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "FERRITINA":
			exam_name = "FERRITINA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "FERRO SERICO":
			exam_name = "FERRO SERICO: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?\s*\w+/\w+)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "RETICULOCITOS":
			exam_name = "RETICULOCITOS: "
			pattern = re.search(r'PERCENTUAL:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1) + " %"
		else:
			return txt
	except AttributeError:
		return txt	
	return string

def labRetriever(name, date):
	with sync_playwright() as p:
		text = ""
		if date:
			s = date.split("/")
			date_limit = datetime.datetime(int(s[2]),int(s[1]),int(s[0]))
		#browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=False, args=["--ignore-certificate-errors"])
		browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
		page = browser.new_page()
		page.goto('https://portal.worklabweb.com.br/resultados-on-line/634')

		# Wait for page to load login inputs
		page.wait_for_selector('input[name="tbCodigo"]', state='visible')

		# Fill in username and password
		page.fill('input[name="tbCodigo"]', 'HDM')
		page.fill('input[name="tbSenha"]', '123456')
		page.select_option('select[name="rdbOpcao"]', 'unidade')

		# Click the login button
		page.locator('button:has-text("Entrar")').click()
		page.wait_for_selector('#preloader-vue', state='hidden', timeout=15000)
		page.fill('input[name="vf__nompac"]', name)
		page.keyboard.press('Enter')
		
		# Extract exams
		page.wait_for_selector('#preloader-vue', state='hidden', timeout=15000)
		rows = page.query_selector_all("tbody tr")
		
		for row in rows:
			status = row.query_selector('a[title="Em análise"]')
			if status:
				continue
			columns = row.query_selector_all('td')
			if len(columns) >= 3:
				row_date = columns[0].inner_text()
				row_name = columns[2].inner_text()
			link = row.query_selector('a[title="Visualizar Exames"]')
			if date:
				s = row_date.split("/")
				exam_date = datetime.datetime(int(s[2]),int(s[1]),int(s[0]))
				if exam_date < date_limit:
					break
			text += f"{row_name}:{nl}({row_date}): "
			if link:
				link.click()
				links = page.query_selector_all('a[title*="Pronto"]')
				for li in links:
					li.click()
					card_body = page.wait_for_selector('div.card-body[style=""]')
					text += text_cleaner(card_body.inner_text())
					text += f"; "
				page.locator('button:has-text("Fechar")').click()
			text += f"{nl}{nl}"

		browser.close()
		
		return text

lab = ""
st.header("🧪LABORATÓRIO DOM MALAN")
st.write("O programa extrai os últimos exames com nome fornecido (no máximo 10). Se extração falhar clique no botão novamente.")
nome_paciente = st.text_input("NOME:")
date_true = st.checkbox("INCLUIR DATA LIMITE")
if date_true:
	st.write("Incluir somente os exames feitos após a data (escrever no formato dd/mm/aaaa):")
	c1, c2 = st.columns([2,8])
	with c1:
		data = st.text_input("DATA:", value=date.today().strftime("%d/%m/%Y"))
if st.button("EXTRAIR"):
	if date_true:
		lab = labRetriever(nome_paciente, data).upper()
	else:
		lab = labRetriever(nome_paciente, False).upper()
st.text_area("LABORATÓRIO:", height=300, value=lab)
