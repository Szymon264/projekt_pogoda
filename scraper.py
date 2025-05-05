#-*- coding: utf-8 -*-

import requests
from lxml import html
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import locale
import chardet

print("Podaj nazwę miasta, dla którego chcesz sprawdzić pogodę(bez polskich znaków):")
city = input()
print(f"Sprawdzam pogodę dla {city}...")

#POGODA
# Aktualna pogoda
url=f"https://www.timeanddate.com/weather/poland/{city.lower()}"
response=requests.get(url)
tree=html.fromstring(response.content)
temp=tree.xpath('//*[@id="qlook"]/div[@class="h2"]/text()')[0].replace('\xa0', '')
desc=tree.xpath('//*[@id="qlook"]/p[1]/text()')
odczuwalna=tree.xpath('//*[@id="qlook"]/p[2]/text()[1]')[0].replace('\xa0', '')
wind=tree.xpath('//*[@id="qlook"]/p[2]/text()[2]')
wind_dir=tree.xpath('//*[@id="qlook"]/p[2]/text()[3]')
print(f"Pogoda dla miasta {city}:")
print(f"Temperatura: {temp}")
print(f"Opis: {desc[0]}")
print(f"Odczuwalna: {odczuwalna}")
print(f"Wiatr: {wind[0]}")
print(f"Kierunek wiatru: {wind_dir[0]}")

# Prognoza godzinowa
url=f'https://www.timeanddate.com/weather/poland/{city.lower()}/hourly'
response=requests.get(url)
tree=html.fromstring(response.content)
hours=[]
temps1=[]
odcz_temp=[] 
descs1=[]
wind1=[]
wind_dir1=[]
rain_chance=[]
rain=[]
hours.append(str(tree.xpath('///*[@id="wt-hbh"]/tbody/tr[1]/th/text()'))) 
temps1.append( [temp.replace('\xa0', '') for temp in tree.xpath('//*[@id="wt-hbh"]/tbody/tr[1]/td[2]/text()')])
descs1.append(tree.xpath('//*[@id="wt-hbh"]/tbody/tr[1]/td[3]/text()'))
odcz_temp.append(tree.xpath('//*[@id="wt-hbh"]/tbody/tr[1]/td[4]/text()')) 
wind1.append(tree.xpath('//*[@id="wt-hbh"]/tbody/tr[1]/td[5]/text()'))
rain_chance.append(tree.xpath('//*[@id="wt-hbh"]/tbody/tr[1]/td[8]/text()'))
rain.append(tree.xpath('//*[@id="wt-hbh"]/tbody/tr[1]/td[9]/text()'))
for i in range (2,25):
    hours.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/th/text()'))
    temps1.append([temp.replace('\xa0', '') for temp in tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[2]/text()')])
    descs1.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[3]/text()'))
    odcz_temp.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[4]/text()')) 
    wind1.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[5]/text()'))
    rain_chance.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[8]/text()'))
    rain.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[9]/text()'))
print("Prognoza godzinowa:")
print(f"{"Godzina":<10}{"Temperatura":<15}{"Opis":<20}{"Odczuwalna":<15}{"Wiatr":<10}{"Szansa na deszcz":<20}{"Deszcz":<10}")
for i in range(len(hours)):
    print(f"{hours[i][0]:<10}{temps1[i][0]:<15}{descs1[i][0]:<20}{odcz_temp[i][0]:<15}{wind1[i][0]:<10}{rain_chance[i][0]:<20}{rain[i][0]:<10}")

# Prognoza dzienna
url=f"https://www.timeanddate.com/weather/poland/{city.lower()}/ext"
response = requests.get(url)
tree=html.fromstring(response.content)
days=[] 
temps2=[]
descs2=[]
odcz_temp2=[] 
wind2=[] 
rain_chance2=[]
rain2=[]

for i in range (1,16):
    days.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/th/text()'))
    temps2.append([temp.replace('\xa0', '') for temp in tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[2]/text()')])
    descs2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[3]/text()'))
    odcz_temp2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[4] /text()')) 
    wind2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[5]/text()'))
    rain_chance2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[8]/text()'))
    rain2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[9]/text()'))
print("Prognoza na 14 dni:")
print(f"{"Dzień":<10}{"Temperatura":<15}{"Opis":<40}{"Odczuwalna":<15}{"Wiatr":<10}{"Szansa na deszcz":<20}{"Deszcz":<10}")
for i in range(len(days)):
    print(f"{days[i][0]:<10}{temps2[i][0]:<15}{descs2[i][0]:<40}{odcz_temp2[i][0]:<15}{wind2[i][0]:<10}{rain_chance2[i][0]:<20}{rain2[i][0]:<10}")


#Wykres dzienny
plt.figure(figsize=(10, 5))
import locale
locale.setlocale(locale.LC_TIME, "pl_PL.UTF-8")  # Set locale to Polish
days = [datetime.datetime.strptime(day[0], "%d %b") for day in days]
# Dodajemy rok do daty, aby uniknąć problemów z porównywaniem dat
for i in range(len(days)):
    days[i] = days[i].replace(year=datetime.datetime.now().year)        


#Przygotowanie danych do wykresu opadów deszczu
rain2 = [r[0].replace('%', '') for r in rain2]
rain2 = [r[0].replace('mm', '') for r in rain2]
rain2 = [r[0].replace('-', '0') for r in rain2]
rain2 = [float(r) for r in rain2]

# Tworzymy listy temperatur maksymalnych i minimalnych
tmax = [float(temp[0].split('/')[0].replace('°C', '')) for temp in temps2]
tmin = [float(temp[0].split('/')[1].replace('°C', '')) for temp in temps2]

# Tworzenie wykresu
fig, ax1 = plt.subplots(figsize=(10, 5))

# Oś temeperatury
ax1.plot(days, tmax, marker='o', linestyle='-', color='r', label='Max Temp')
ax1.plot(days, tmin, marker='o', linestyle='-', color='b', label='Min Temp')
ax1.set_xlabel("Dzień")
ax1.set_ylabel("Temperatura (°C)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid()

# Druga oś dla opadów deszczu
ax2 = ax1.twinx()
ax2.bar(days, rain2, color='navy', alpha=0.3, label='Opady deszczu')
ax2.set_ylabel("Opady deszczu (mm)", color='navy')
ax2.tick_params(axis='y', labelcolor='navy')

# Formatowanie osi x
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
plt.xticks(rotation=45)

# Dodanie legendy i tytułu
fig.suptitle("Temperatura na najbliższe dni i opady deszczu")
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Wyświetlenie wykresu
plt.show()

#WYDARZENIA 

# Pobierz zawartość strony
info_url = f"https://www.rmf24.pl/regiony/{city.lower()}"
response = requests.get(info_url)

# Automatyczne wykrycie kodowania
raw_content = response.content
detected_encoding = chardet.detect(raw_content)['encoding']

# Dekoduj zawartość strony
decoded_content = raw_content.decode(detected_encoding)

# Przetwórz HTML
tree = html.fromstring(decoded_content)

# Zbierz tytuły wiadomości
events = []
events.append(tree.xpath('//*[@id="l0"]/div[1]/div/div[1]/div/div/div[2]/h2/a/text()'))
events.append(tree.xpath('//*[@id="l0"]/div[2]/div/div[2]/div/div[2]/h3/a/text()'))
events.append(tree.xpath('//*[@id="l0"]/div[3]/div/div[2]/div/div[2]/h3/a/text()'))
events.append(tree.xpath('//*[@id="k3"]/li[1]/div[2]/div[2]/div/h3/a/text()'))
events.append(tree.xpath('//*[@id="k3"]/li[2]/div[2]/div[2]/div/h3/a/text()'))

# Zapisz do pliku tekstowego z poprawnym kodowaniem
with open("wiadomosci.txt", "w", encoding="utf-8") as f:
    for i, tytul in enumerate(events, 1):
        if tytul:
            f.write(f"{i}. {tytul[0]}\n")
        else:
            f.write(f"{i}. Brak informacji\n")

print("✅ Zapisano poprawnie do pliku wiadomosci.txt")



#
