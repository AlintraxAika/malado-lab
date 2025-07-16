#import streamlit as st
import tkinter as tk
from tkinter import ttk
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
			string += " | HB: " + pattern.group(1)
			pattern = re.search(r'LEUCOCITOS.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | LEUCO: " + pattern.group(1)
			pattern = re.search(r'PLAQUETAS.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | PLAQ: " + pattern.group(1)
		elif exam_name == "GRUPO SANGUÍNEO":
			string = "GS: "
			pattern = re.search(r'GRUPO SANGUINEO.*?:\s*([A-Z]+)', txt, re.IGNORECASE)
			string += pattern.group(1) + " "
			pattern = re.search(r'FATOR\s+RH\s*\(.*?\).*?:\s*([A-Z]+)', txt, re.IGNORECASE)
			string += pattern.group(1)
		elif exam_name == "DESIDROGENASE LÁCTICA":
			exam_name = "DHL: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
			string = string.replace("  ", " ")
		elif exam_name == "UREIA":
			exam_name = "UR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "CREATININA":
			exam_name = "CR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "BILIRRUBINA TOTAL E FRAÇÕES":
			string = "BT: "
			pattern = re.search(r'BILIRRUBINA\s+TOTAL.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += pattern.group(1)
			pattern = re.search(r'BILIRRUBINA\s+DIRETA.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | BD: " + pattern.group(1)
			pattern = re.search(r'BILIRRUBINA\s+INDIRETA.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | BI: " + pattern.group(1)
		elif exam_name == "TRANSAMINASE OXALACÉTICA (TGO/AST)":
			exam_name = "AST: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "TRANSAMINASE PIRÚVICA (TGP/ALT)":
			exam_name = "ALT: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "RAZAO PROTEINA/CREATININA - URINA":
			exam_name = "PROT/CR: "
			pattern = re.search(r'RELACAO PROTEINA/CREATININA:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "PROTEINURIA 24H":
			string = "PROT/24H: "
			pattern = re.search(r'RESULTADO:\s*([\d.,]+)\s', txt, re.IGNORECASE)
			string += pattern.group(1) + " MG (VOL: "
			pattern = re.search(r'VOLUME\s+URINARIO:\s*([\d.,]+)', txt, re.IGNORECASE)
			string += pattern.group(1) + " ML)"
		elif exam_name == "ÁCIDO ÚRICO":
			exam_name = "AC. UR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "SÓDIO":
			exam_name = "NA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "POTÁSSIO":
			exam_name = "K: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "PROTEINA C REATIVA":
			exam_name = "PCR: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "TEMPO DE PROTROMBINA":
			string = "TP: "
			pattern = re.search(r'PROTROMBINA.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += pattern.group(1)
			pattern = re.search(r'ENZIMÁTICA.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | ATIV. ENZ.: " + pattern.group(1)
			pattern = re.search(r'I.N.R.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | INR: " + pattern.group(1)
		elif exam_name == "PROTEÍNAS TOTAIS E FRAÇÕES":
			string = "PT: "
			pattern = re.search(r'PROTEINAS TOTAIS.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += pattern.group(1)
			pattern = re.search(r'ALBUMINA.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | ALB: " + pattern.group(1)
			pattern = re.search(r'GLOBULINAS.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += " | GLOB: " + pattern.group(1)
		elif exam_name == "TEMPO DE TROMBOPLASTINA P. ATIVADA":
			string = "TTPA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string += pattern.group(1)
		elif exam_name == "CÁLCIO":
			exam_name = "CA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "CLORETOS":
			exam_name = "CL: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "ALBUMINA":
			exam_name = "ALBUMINA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "MAGNÉSIO":
			exam_name = "MG: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "AMILASE":
			exam_name = "AMILASE: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "LIPASE":
			exam_name = "LIPASE: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "FERRITINA":
			exam_name = "FERRITINA: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "FERRO SERICO":
			exam_name = "FERRO SERICO: "
			pattern = re.search(r'RESULTADO.*?:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1)
		elif exam_name == "RETICULOCITOS":
			exam_name = "RETICULOCITOS: "
			pattern = re.search(r'PERCENTUAL:\s*(\d+(?:[.,]\d+)?)', txt, re.IGNORECASE)
			string = exam_name + pattern.group(1) + " %"
		else:
			#return f"{nl}" + txt.replace("\n"," ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
			return exam_name + ": [[EXAME NAO ABARCADO PELO PROGRAMA ATUALMENTE]]"
	except AttributeError:
		#return f"{nl}" + txt.replace("\n"," ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
		return exam_name + ": [[EXAME NAO ABARCADO PELO PROGRAMA ATUALMENTE]]"
	
	return string

def labRetriever(name, date):
	with sync_playwright() as p:
		text = ""
		if date:
			s = date.split("/")
			date_limit = datetime.datetime(int(s[2]),int(s[1]),int(s[0]))
		#browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=False, args=["--ignore-certificate-errors"])
		browser = p.chromium.launch(headless=False, args=["--ignore-certificate-errors"])
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
		page.wait_for_selector('#preloader-vue', state='hidden', timeout=20000)
		page.fill('input[name="vf__nompac"]', name)
		page.keyboard.press('Enter')
		
		# Extract exams
		page.wait_for_selector('#preloader-vue', state='hidden', timeout=20000)
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
			try:
				text += f"{row_name}:{nl}({row_date}): ".replace("/20", "/")
			except UnboundLocalError:
				return "Paciente sem exames."
			if link:
				link.click()
				links = page.query_selector_all('a[title*="Pronto"]')
				for li in links:
					li.click()
					card_body = page.wait_for_selector('div.card-body[style=""]')
					text += text_cleaner(card_body.inner_text())
					text += f" | "
				page.locator('button:has-text("Fechar")').click()
			text = text[:-3]
			text += f"{nl}{nl}"

		browser.close()
		
		return text

def extract_lab():
    name = name_entry.get()
    if include_date_var.get():
        date_str = date_entry.get()
        result = labRetriever(name, date_str).upper()
    else:
        result = labRetriever(name, False).upper()
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, result)

# TKINTER GUI
root = tk.Tk()
root.title("🧪 LABORATÓRIO DOM MALAN")

frame = ttk.Frame(root, padding=20)
frame.pack()

ttk.Label(frame, text="O programa extrai os últimos exames com nome fornecido (no máximo 10).\nSe extração falhar, clique no botão novamente.").pack(pady=5)

ttk.Label(frame, text="NOME:").pack(anchor="w")
name_entry = ttk.Entry(frame, width=50)
name_entry.pack()

include_date_var = tk.BooleanVar()
date_check = ttk.Checkbutton(frame, text="INCLUIR DATA LIMITE", variable=include_date_var)
date_check.pack(anchor="w", pady=(10, 0))

ttk.Label(frame, text="DATA (formato dd/mm/aaaa):").pack(anchor="w")
date_entry = ttk.Entry(frame, width=20)
date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
date_entry.pack(anchor="w")

ttk.Button(frame, text="EXTRAIR", command=extract_lab).pack(pady=10)

ttk.Label(frame, text="LABORATÓRIO:").pack(anchor="w")
result_text = tk.Text(frame, height=50, width=200)
result_text.pack()

root.mainloop()

#NO GRAPHICAL INTERFACE
#print("NOME:", end=" ")
#nn = input()
#print("DATA LIMITE [(dd/mm/aaaa) ou (x)]:", end=" ")
#dt = input()
#dt = dt.upper()
#if dt == "X":
#	with open("laboratorios.txt", "w") as f:
#		f.write(labRetriever(nn, False).upper())
#else:
#	with open("laboratorios.txt", "w") as f:
#		f.write(labRetriever(nn, dt).upper())

#STREAMLIT UI
#lab = ""
#st.header("🧪LABORATÓRIO DOM MALAN")
#st.write("O programa extrai os últimos exames com nome fornecido (no máximo 10). Se extração falhar clique no botão novamente.")
#nome_paciente = st.text_input("NOME:")
#date_true = st.checkbox("INCLUIR DATA LIMITE")
#if date_true:
#	st.write("Incluir somente os exames feitos após a data (escrever no formato dd/mm/aaaa):")
#	c1, c2 = st.columns([2,8])
#	with c1:
#		data = st.text_input("DATA:", value=date.today().strftime("%d/%m/%Y"))
#if st.button("EXTRAIR"):
#	if date_true:
#		lab = labRetriever(nome_paciente, data).upper()
#	else:
#		lab = labRetriever(nome_paciente, False).upper()
#st.text_area("LABORATÓRIO:", height=300, value=lab)
