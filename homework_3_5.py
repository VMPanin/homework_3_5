import osa
import math


def convert_temps(path):
    list_temps = []
    with open(path) as f:
        for line in f:
            list_temps.append(int(line[0:2]))
    average_temp_f = sum(list_temps) / len(list_temps)

    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    average_temp_C = client.service.ConvertTemp(
        Temperature=average_temp_f,
        FromUnit='degreeFahrenheit',
        ToUnit='degreeCelsius'
    )
    return round(average_temp_C, 1)


def convert_currencies(path):
    dict_currencies = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            dict_currencies[line[len(line)-3:len(line)]] = line[line.find(': ')+2:len(line)-4]

    total_amount = 0
    for k, v in dict_currencies.items():
        client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
        amount = client.service.ConvertToNum(
            fromCurrency=k,
            toCurrency='RUB',
            amount=v,
            rounding=False
        )
        total_amount += amount
    return math.ceil(total_amount)


def convert_travel(path):
    list_travel = []
    with open(path) as f:
        for line in f:
            line = line.replace(',', '').strip()
            list_travel.append(float(line[line.find(': ')+2:len(line)-3]))

    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    amount = client.service.ChangeLengthUnit(
        LengthValue=sum(list_travel),
        fromLengthUnit='Miles',
        toLengthUnit='Kilometers'
    )
    return round(amount, 2)


# Перевод температуры с помощью калькулятора (на всякий случай, как альтернатива)
def convert_temps_calculator():
    list_temps = []
    with open('temps.txt') as f:
        for line in f:
            list_temps.append(int(line[0:2]))

    client = osa.Client('http://www.dneonline.com/calculator.asmx?WSDL')
    average_temp_f = client.service.Divide(intA=sum(list_temps), intB=len(list_temps))
    average_temp_1 = client.service.Subtract(intA=average_temp_f, intB=32)
    average_temp_2 = client.service.Multiply(intA=average_temp_1, intB=5)
    average_temp_c = client.service.Divide(intA=average_temp_2, intB=9)
    return average_temp_c


def get_path():
    path = input('Введи полный путь к файлу:')
    return path

def main():
    path = get_path()
    if 'temps' in path:
        print(convert_temps(path))
    if 'currencies' in path:
        print(convert_currencies(path))
    if 'travel' in path:
        print(convert_travel(path))

main()
