from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

def abrir_chrome(url):
    chrome = webdriver.Chrome()
    chrome.get(url)
    sleep(1)
    return chrome

def buscar_meli(produto):
    chrome = abrir_chrome('https://www.mercadolivre.com.br/')
    try:
        buscar = chrome.find_element(By.XPATH, '//input[@id="cb1-edit"]')
    except:
        print('Elemento de busca não encontrado, tente novamente mais tarde')
        return
    buscar.send_keys(produto)
    buscar.send_keys(Keys.ENTER)
    sleep(1)

    try:
        produtos = chrome.find_elements(By.XPATH, '//div[@class="ui-search-result__wrapper"]')
    except:
        print('Produtos não encontrado, tente novamente mais tarde')
        return
    dados = []
    for index, produto in enumerate(produtos):
        if index == 3:
            break
        
        try:
            link = produto.find_element(By.XPATH, './/a[@class="ui-search-item__group__element ui-search-link__title-card ui-search-link"]').get_attribute('href')
        except:
            print('Link não encontrado, tente novamente mais tarde')
            return
        
        try:
            titulo = produto.find_element(By.TAG_NAME, 'h2').text
        except:
            print('Titulo não encontrado, tente novamente mais tarde')
            return
        
        try:
            preco = produto.find_element(By.XPATH, './/span[@class="andes-money-amount__fraction"]').text
        except:
            print('Preço não encontrado, tente novamente mais tarde')
            return
        
        dados.append({'Titulo': titulo, 'Preço': preco, 'Link': link})

    return dados

def salvar_dados(dados):
    with open('produtos.csv', mode='w', newline='') as meu_csv:
        cabecalho = ['Titulo', 'Preço', 'Link']
        writer = csv.DictWriter(meu_csv, delimiter=';', fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(dados)

produto = 's21'

dados = buscar_meli(produto)
salvar_dados(dados)