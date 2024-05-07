import datetime, math

# Função para converter uma string para um objeto datetime
def parse_datetime(date_time_str):
    return datetime.datetime.strptime(date_time_str.strip(), "%d/%m/%Y %H:%M:%S")

def format_time(decimal_hours):
    hours = int(decimal_hours)
    # Calcular a parte fracionada para os minutos
    decimal_remainder = decimal_hours - hours
    minutes = int(decimal_remainder * 60)
    # Calcular os segundos a partir do restante
    seconds = int((decimal_remainder * 60 - minutes) * 60)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return formatted_time

# Lê o arquivo de datas
with open("data.txt", "r") as file:
    lines = file.readlines()

total_sum = datetime.timedelta(0)
differences = []
for i in range(0, len(lines), 2):
    date1_str = lines[i].strip()  # Remova espaços extras
    date2_str = lines[i + 1].strip()
    # Converte as strings para objetos datetime
    date1 = parse_datetime(date1_str)
    date2 = parse_datetime(date2_str)
    # Calcula a diferença entre as duas datas
    difference = date1 - date2
    differences.append(difference)
    total_sum += difference

# Conversão para segundos e depois para horas
total_seconds = total_sum.total_seconds()
total_hours = total_seconds / 3600

print('Sujestão de dias:',int(len(lines)/4))
# Calcula os dias úteis no mês e verifica se está devendo ou se tem horas extras trabalhadas
working_days_in_month = int(input('Informe quantos dias foram trabalhados nesse mês: '))
hours_per_day = 8
hours_in_month = working_days_in_month * hours_per_day
extra_hours = total_hours - hours_in_month
formatted_extra_hours = format_time(extra_hours)

print("\nDiferenças individuais:")
for i, difference in enumerate(differences, 1):
    print(f"Diferença {i}: {difference}")

print("\nSoma total de todas as diferenças ou dias perdidos trabalhando:", total_sum, "\nTotal de horas:", math.floor(total_hours),"Obs: arredonda para baixo", "\nHoras a mais (extras):", formatted_extra_hours)
