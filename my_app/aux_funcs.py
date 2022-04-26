
from datetime import datetime
from .models import Transactions

def validate_transactions(f, dates):
    '''
    Função para avaliar as transações do arquivo.
    Recebe: Arquivo e lista de datas já utilizadas
    Retorna: Transações válidas; Data das transações; Mensagens de erro.
    '''
    new_transactions = []
    msg = []

    # Verificar se arquivo possui dados
    f.seek(0)
    one_char = f.read(1)
    if not one_char:
        msg.append('Arquivo vazio')
        return None, None, msg
    
    # Percorrer todas as linhas do arquivo
    first = True
    invalid_dates = 0
    duplicated_dates = 0
    missing_fields = 0
    for line in f.readlines():
        
        # Separar campos da linha
        campos = line.decode('ascii').strip('\n').split(',')
        
        # Verificar se possui informações em todos os campos
        complete = False if '' in campos else True
        if not complete:
            missing_fields += 1
            continue

        # Analisar consistencia da data
        data_hora = campos[-1]
        try:
            data = data_hora[:10]
            data_hora = datetime.strptime(data_hora, '%Y-%m-%dT%H:%M:%S')
        except:
            invalid_dates += 1
            continue

        # Armazenar data da primeira linha válida
        if first:
            first_date = data
            first = False

            # Verificar se já existem registros para a data da primeira transação válida
            if first_date in dates:
                msg.append(f'Já existem registros para {first_date}')
                return None, None, msg

        # Armazenar transações válidas
        if data == first_date:
            t = Transactions(banco_origem = campos[0],
            agencia_origem = campos[1],
            conta_origem = campos[2],
            banco_destino = campos[3],
            agencia_destino = campos[4],
            conta_destino = campos[5],
            valor = float(campos[6]),
            data_hora = data_hora,
            date_transactions = first_date)
            
            new_transactions.append(t)
        else:
            duplicated_dates += 1
            continue

    # Contabilizar possíveis erros
    if invalid_dates > 0:
        msg.append(f'{invalid_dates} transações não foram incluídas devido a erro no campo de data')
    if duplicated_dates > 0:
        msg.append(f'{duplicated_dates} transações não foram incluídas pois não são de {first_date}')
    if missing_fields > 0:
        msg.append(f'{missing_fields} transações não foram incluídas pois possuem dados ausentes')

    # Retornar transações válidas, data das transações e mensagens de erro
    return new_transactions, first_date, msg