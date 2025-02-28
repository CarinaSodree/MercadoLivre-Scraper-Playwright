from playwright.sync_api import sync_playwright  # Importando a API do Playwright para automação de navegação
from openpyxl import Workbook  # Importando a classe Workbook da biblioteca openpyxl para criação e manipulação de arquivos Excel

def scrape_mercadolivre():
    # Iniciando o Playwright para automatizar a navegação no site
    with sync_playwright() as p:
        # Inicializa o navegador Chromium (pode ser o Chromium, Firefox ou Webkit, mas usaremos o Chromium)
        browser = p.chromium.launch(headless=False)  # Defina como True para rodar sem abrir a janela do navegador
        page = browser.new_page()  # Cria uma nova página para navegar

        # URL da página de pesquisa no Mercado Livre para smartphones
        url = "https://lista.mercadolivre.com.br/smartphone#D[A:smartphone]"
        page.goto(url)  # Acessa a URL fornecida

        # Espera o carregamento completo da página e dos preços visíveis na tela
        # O seletor "span.andes-money-amount__fraction" é responsável por exibir o valor inteiro do preço
        print("Aguardando o carregamento completo da página...")
        page.wait_for_selector("span.andes-money-amount__fraction", timeout=10000)  # Espera por até 10 segundos

        # Inicializando listas para armazenar os dados de produtos, preços e links
        produtos = []  # Lista para armazenar os nomes dos produtos
        precos = []  # Lista para armazenar os preços dos produtos
        links = []  # Lista para armazenar os links dos produtos

        # Seleciona todos os elementos que contêm os links para os produtos (a.poly-component__title)
        produtos_elementos = page.query_selector_all("a.poly-component__title")

        # Verifica se foram encontrados produtos, caso contrário, imprime uma mensagem e encerra
        if not produtos_elementos:
            print("Nenhum produto encontrado.")
            return

        # Seleciona todos os elementos que contêm os preços inteiros dos produtos
        precos_elementos = page.query_selector_all("span.andes-money-amount__fraction")
        # Seleciona todos os elementos que contêm os centavos dos preços
        centavos_elementos = page.query_selector_all("span.andes-money-amount__cents")

        # Verifica se foi encontrado algum preço
        if not precos_elementos:
            print("Nenhum preço encontrado.")
            return

        # Inicia a extração das informações dos produtos
        print(f"Encontrados {len(produtos_elementos)} produtos. Extraindo dados...")
        for i in range(len(produtos_elementos)):
            # Extrai o nome do produto
            nome_produto = produtos_elementos[i].text_content()
            # Extrai o link do produto
            link_produto = produtos_elementos[i].get_attribute("href")
            # Extrai o preço inteiro do produto (R$ 859)
            preco_inteiro = precos_elementos[i].text_content().strip() if i < len(precos_elementos) else "Preço não encontrado"
            # Extrai os centavos do preço do produto (10)
            centavos = centavos_elementos[i].text_content().strip() if i < len(centavos_elementos) else "00"
            
            # Combina o valor inteiro com os centavos para formar o preço completo
            preco_produto = f"{preco_inteiro},{centavos}"  # Exemplo: "R$ 859,10"

            # Adiciona os dados extraídos nas listas correspondentes
            produtos.append(nome_produto)
            precos.append(preco_produto)
            links.append(link_produto)

        # Fecha o navegador após a extração dos dados
        browser.close()

        # Cria um novo arquivo Excel e seleciona a planilha ativa
        wb = Workbook()
        ws = wb.active
        ws.title = "Produtos Mercado Livre"  # Define o nome da planilha como "Produtos Mercado Livre"

        # Adiciona o cabeçalho na planilha com os nomes das colunas
        ws.append(["Nome", "Preço", "Link"])

        # Adiciona os dados extraídos na planilha, linha por linha
        for i in range(len(produtos)):
            ws.append([produtos[i], precos[i], links[i]])

        # Salva o arquivo Excel com o nome "produtos_mercadolivre.xlsx"
        wb.save("produtos_mercadolivre.xlsx")
        print("Arquivo Excel gerado com sucesso: produtos_mercadolivre.xlsx")

# Este código será executado quando o script for rodado diretamente
if __name__ == "__main__":
    scrape_mercadolivre()
