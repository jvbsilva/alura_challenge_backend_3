
from datetime import datetime
from .models import Transactions, History

def validate_transactions(f, dates):
    new_transactions = []
    msg = []

    f.seek(0)
    one_char = f.read(1)
    if not one_char:
        msg.append('Arquivo vazio')
        return None, None, msg
    
    first = True
    invalid_dates = 0
    duplicated_dates = 0
    missing_fields = 0
    for line in f.readlines():

        campos = line.decode('ascii').strip('\n').split(',')
        
        complete = False if '' in campos else True
        if not complete:
            missing_fields += 1
            continue

        data_hora = campos[-1]
        try:
            data = data_hora[:10]
            data_hora = datetime.strptime(data_hora, '%Y-%m-%dT%H:%M:%S')
        except:
            invalid_dates += 1
            continue

        if first:
            first_date = data
            first = False

            if first_date in dates:
                msg.append(f'Já existem registros para {first_date}')
                return None, None, msg

            h = History(date_transactions = data)

        if data == first_date:
            t = Transactions(banco_origem = campos[0],
            agencia_origem = campos[1],
            conta_origem = campos[2],
            banco_destino = campos[3],
            agencia_destino = campos[4],
            conta_destino = campos[5],
            valor = float(campos[6]),
            data_hora = data_hora)

            new_transactions.append(t)
        else:
            duplicated_dates += 1
    
    if invalid_dates > 0:
        msg.append(f'{invalid_dates} transações não foram incluídas devido a erro no campo de data')
    if duplicated_dates > 0:
        msg.append(f'{duplicated_dates} transações não foram incluídas pois já há registros para essas datas')
    if missing_fields > 0:
        msg.append(f'{missing_fields} transações não foram incluídas pois possuem dados ausentes')

    return new_transactions, h, msg