import random
import sys
import requests

def api_fipe():
    print('Iniciando script')
    try:
        # Pega o valor de referencia mais atual para seguir na busca
        reference_month_code = get_reference_month()
        
        # For para realizar as 10 buscas aleatoria
        for i in range(0, 10):
            count = i + 1
            print(f'\nVeiculo: {count}')
            brand_code = get_brand(reference_month_code)
            model_code = get_model(reference_month_code, brand_code)
            year_model = get_year_model(reference_month_code, brand_code, model_code)
            vehicle    = get_vehicle(reference_month_code, brand_code, model_code, year_model.split("-"))

            print('---------------------------------------------------------------------')
    except Exception as e:
        print(f"Ocorreu um erro: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
def get_reference_month():
    """
    Obtém o código do mês de referência mais atual da API da FIPE.
    
    Returns:
        str: O código do mês de referência.
    """
    try:
        reference_month_fipe = connect_fipe('ConsultarTabelaDeReferencia')
        last_reference_month_code = reference_month_fipe[0]['Codigo']
        return last_reference_month_code
    except Exception as e:
        print(f"Erro ao obter mês de referência: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
def get_brand(reference_month_code):
    """
    Obtém a marca do veiculo de forma aleatoria da API da FIPE.
    
    Returns:
        str: Codigo referente a marca do veiculo.
    """
    try:
        payload = {
            "codigoTabelaReferencia": reference_month_code,
            "codigoTipoVeiculo": 1 # Codigo para somente veiculos
        }
        brands = connect_fipe('ConsultarMarcas', payload)
        random_brand = random.choice(brands)
        return random_brand['Value']
    except Exception as e:
        print(f"Erro ao obter marca: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
def get_model(reference_month_code, brand_code):
    """
    Obtém o modelo do veiculo a partir da marca no parametro de forma aleatoria da API da FIPE.
    
    Returns:
        str: Codigo referente ao modelo do veiculo.
    """
    try:
        payload = {
            "codigoTabelaReferencia": reference_month_code,
            "codigoTipoVeiculo": 1, # Codigo para somente veiculos
            "codigoMarca": brand_code
        }
        models = connect_fipe('ConsultarModelos', payload)
        random_model = random.choice(models['Modelos'])
        return random_model['Value']
    except Exception as e:
        print(f"Erro ao obter modelo: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
def get_year_model(reference_month_code, brand_code, model_code):
    """
    Obtém o ano e o modelo referente do veiculo a partir da marca e modelo no parametro de forma aleatoria da API da FIPE.
    
    Returns:
        str: Codigo referente ao Ano/Modelo do veiculo.
    """
    try:
        payload = {
            "codigoTabelaReferencia": reference_month_code,
            "codigoTipoVeiculo": 1, # Codigo para somente veiculos
            "codigoMarca": brand_code,
            "codigoModelo": model_code
        }
        year_models = connect_fipe('ConsultarAnoModelo', payload)
        random_year_models = random.choice(year_models)
        return random_year_models['Value']
    except Exception as e:
        print(f"Erro ao obter ano/modelo: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
def get_vehicle(reference_month_code, brand_code, model_code, year_model):
    """
    Obtém todas as informações do veiculo a partir da marca, modelo e ano modelo nos parametro da API da FIPE.
    
    Returns:
        array: informações do veiculo.
    """
    try:
        payload = {
            "codigoTabelaReferencia": reference_month_code,
            "codigoTipoVeiculo": 1, # Codigo para somente veiculos
            "codigoMarca": brand_code,
            "codigoTipoCombustivel": year_model[1],
            "anoModelo": year_model[0],
            "codigoModelo": model_code,
            "tipoConsulta": "tradicional"
        }
        print('Consultando dados do veiculo na API da Fipe')
        vehicle = connect_fipe('ConsultarValorComTodosParametros', payload)
        print(vehicle)
        return vehicle
    except Exception as e:
        print(f"Erro ao obter dados do veículo: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
def connect_fipe(endpoint, payload=None):
    """
    Conecta-se à API da FIPE e realiza uma requisição POST para o endpoint especificado.
    
    Args:
        endpoint (str): O endpoint específico da API da FIPE.
        payload (dict, optional): Dados a serem enviados na requisição. Padrão é None.
        
    Returns:
        dict: Os dados JSON retornados pela API da FIPE.
    """
    try:
        url = f'http://veiculos.fipe.org.br/api/veiculos/{endpoint}'
        headers = {'Content-Type': 'application/json'}

        # Verifica se há payload; se não, cria um dicionário vazio
        if payload is None:
            payload = {}
            
        # Faz a requisição POST
        response = requests.post(url, headers=headers, json=payload)
        
        # Retorna os dados JSON
        return response.json()
    except Exception as e:
        print(f"Erro na conexão com a API da FIPE: {e} - Linha: {sys.exc_info()[-1].tb_lineno}")
        sys.exit()
api_fipe()