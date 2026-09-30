import datetime
import math
import sys

DATA_FILE = "data.txt"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
DATE_EXAMPLE = "07/05/2024 11:41:31"


def parse_datetime(date_time_str):
    return datetime.datetime.strptime(date_time_str.strip(), DATE_FORMAT)


def format_time(decimal_hours):
    hours = int(decimal_hours)
    decimal_remainder = decimal_hours - hours
    minutes = int(decimal_remainder * 60)
    seconds = int((decimal_remainder * 60 - minutes) * 60)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return formatted_time


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_punches(path):
    try:
        with open(path, "r") as file:
            raw_lines = file.readlines()
    except FileNotFoundError:
        fail(
            f"Não encontrei o arquivo '{path}' na pasta em que o programa foi executado.\n"
            f"Crie esse arquivo e coloque um horário por linha, no formato {DATE_EXAMPLE}."
        )

    punches = []
    invalid = []
    for line_number, raw in enumerate(raw_lines, start=1):
        text = raw.strip()
        if not text:
            continue
        try:
            moment = parse_datetime(text)
        except ValueError:
            invalid.append((line_number, text))
        else:
            punches.append((line_number, text, moment))

    if invalid:
        fail(invalid_lines_message(path, invalid))

    if not punches:
        fail(
            f"O arquivo '{path}' não tem nenhum horário.\n"
            f"Coloque um horário por linha, no formato {DATE_EXAMPLE}."
        )

    odd_days = odd_punch_days(punches)
    if odd_days:
        fail(odd_days_message(path, odd_days))

    return punches


def odd_punch_days(punches):
    grouped = {}
    order = []
    for line_number, text, moment in punches:
        day = moment.date()
        if day not in grouped:
            grouped[day] = []
            order.append(day)
        grouped[day].append((line_number, text))
    return [(day, grouped[day]) for day in order if len(grouped[day]) % 2 != 0]


def invalid_lines_message(path, invalid):
    details = "\n".join(f"  linha {number}: {text}" for number, text in invalid)
    return (
        f"Não deu para calcular as horas de '{path}'.\n"
        "\n"
        "Estas linhas não estão no formato dia/mês/ano hora:minuto:segundo,\n"
        "então não dá para montar os pares de entrada e saída:\n"
        "\n"
        f"{details}\n"
        "\n"
        f"Ajuste cada uma para o formato {DATE_EXAMPLE} e rode de novo."
    )


def odd_days_message(path, odd_days):
    blocks = []
    for day, entries in odd_days:
        shown = "\n".join(f"    linha {number}: {text}" for number, text in entries)
        first = entries[0][0]
        last = entries[-1][0]
        if first == last:
            where = f"na linha {first}"
        else:
            where = f"nas linhas {first} a {last}"
        blocks.append(
            f"  {day.strftime('%d/%m/%Y')} tem {len(entries)} horários (ímpar), {where}:\n"
            f"{shown}"
        )

    listed = "\n\n".join(blocks)
    if len(odd_days) == 1:
        heading = "Este dia não fecha. É aí que está o problema:"
    else:
        heading = "Estes dias não fecham. É aí que está o problema:"

    return (
        f"Não deu para calcular as horas de '{path}'.\n"
        "\n"
        "Os horários são lidos de dois em dois: um período só existe com o horário\n"
        "de saída e o de entrada. Cada dia precisa de uma quantidade par de registros.\n"
        "Um dia completo costuma ter 4 linhas: entrada, saída para o almoço, volta e saída.\n"
        "\n"
        f"{heading}\n"
        "\n"
        f"{listed}\n"
        "\n"
        "Como ajustar: compare essas linhas com o espelho de ponto. Inclua o horário\n"
        f"que falta ou apague o que estiver sobrando. O formato é {DATE_EXAMPLE}."
    )


def main():
    punches = load_punches(DATA_FILE)

    total_sum = datetime.timedelta(0)
    differences = []
    for i in range(0, len(punches), 2):
        date1 = punches[i][2]
        date2 = punches[i + 1][2]
        difference = date1 - date2
        differences.append(difference)
        total_sum += difference

    total_seconds = total_sum.total_seconds()
    total_hours = total_seconds / 3600

    print("Sujestão de dias:", int(len(punches) / 4))
    working_days_in_month = int(input("Informe quantos dias foram trabalhados nesse mês: "))
    hours_per_day = 8
    hours_in_month = working_days_in_month * hours_per_day
    extra_hours = total_hours - hours_in_month
    formatted_extra_hours = format_time(extra_hours)

    print("\nDiferenças individuais:")
    for i, difference in enumerate(differences, 1):
        print(f"Diferença {i}: {difference}")

    print(
        "\nSoma total de todas as diferenças ou dias perdidos trabalhando:",
        total_sum,
        "\nTotal de horas:",
        math.floor(total_hours),
        "Obs: arredonda para baixo",
        "\nHoras a mais (extras):",
        formatted_extra_hours,
    )


if __name__ == "__main__":
    main()
