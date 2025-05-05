#-*- coding: utf-8 -*-

import requests
from lxml import html
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.ticker as ticker
import locale
import chardet
import sys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def normalize_city_name(city_name):
    """Konwertuje nazwę miasta na format akceptowany przez timeanddate.com"""
    try:
        geolocator = Nominatim(user_agent="weather_app")
        # Najpierw próbujemy z "Poland" dla lepszych wyników dla polskich miast
        location = geolocator.geocode(f"{city_name}, Poland", language="en")
        
        if location is None:
            # Jeśli nie znaleziono z "Poland", próbujemy bez kraju
            location = geolocator.geocode(city_name, language="en")
            
        if location is None:
            # Jeśli nadal nie znaleziono, spróbuj podstawowej normalizacji
            replacements = {
                'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
                'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
                'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
                'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
                ' ': '-', '.': '', ',': '', "'": '', '"': ''
            }
            normalized = ''.join(replacements.get(c, c) for c in city_name)
            return normalized.lower()
            
        # Wyciągnij nazwę miasta z rezultatu
        address_parts = location.address.split(',')
        # Weź pierwszą część adresu (zazwyczaj nazwa miasta)
        city = address_parts[0].strip()
        
        # Usuń wszelkie dodatkowe oznaczenia
        city = city.replace("City", "").replace("Town", "").strip()
        # Zamień spacje na myślniki i usuń znaki specjalne
        city = city.lower().replace(" ", "-")
        city = ''.join(c for c in city if c.isalnum() or c == '-')
        
        return city
        
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Błąd geolokalizacji: {str(e)}")
        # W przypadku błędu, zwróć podstawową normalizację
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
            ' ': '-', '.': '', ',': '', "'": '', '"': ''
        }
        normalized = ''.join(replacements.get(c, c) for c in city_name)
        return normalized.lower()

print("Podaj nazwę miasta, dla którego chcesz sprawdzić pogodę (możesz użyć polskich znaków):")
city = input()
normalized_city = normalize_city_name(city)
print(f"Sprawdzam pogodę dla {city}...")

# Dodaj dodatkowe sprawdzenie dostępności miasta
test_url = f"https://www.timeanddate.com/weather/poland/{normalized_city}"
test_response = requests.get(test_url)

if test_response.status_code != 200:
    # Jeśli pierwsze podejście nie zadziałało, spróbuj alternatywnej normalizacji
    normalized_city = city.lower().replace(" ", "-").replace("ó", "o").replace("ą", "a").replace("ę", "e").replace("ś", "s").replace("ł", "l").replace("ż", "z").replace("ź", "z").replace("ć", "c").replace("ń", "n")
    test_url = f"https://www.timeanddate.com/weather/poland/{normalized_city}"
    test_response = requests.get(test_url)
    
    if test_response.status_code != 200:
        print(f"Błąd: Nie można znaleźć miasta {city}. Sprawdź, czy nazwa jest poprawna.")
        print(f"Spróbuj wpisać nazwę miasta w formie międzynarodowej (np. 'rzeszow' zamiast 'Rzeszów')")
        sys.exit(1)

try:
    #POGODA
    # Aktualna pogoda
    url=f"https://www.timeanddate.com/weather/poland/{normalized_city.lower()}"
    response=requests.get(url)
    
    if response.status_code != 200:
        print(f"Błąd: Nie można znaleźć miasta {city}. Sprawdź, czy nazwa jest poprawna.")
        sys.exit(1)
        
    tree=html.fromstring(response.content)
    
    # Aktualizacja XPath queries dla aktualnej struktury strony
    temp_elem = tree.xpath('//div[contains(@class, "h2")]/text()')
    if not temp_elem:
        temp_elem = tree.xpath('//div[@class="temp"]/text()')
    temp = temp_elem[0].strip().replace('\xa0', '') if temp_elem else "Brak danych"
    
    desc = tree.xpath('//p[@class="summary"]/text() | //p[@class="ok"]/text()')
    desc = desc[0] if desc else "Brak danych"
    
    feels_like = tree.xpath('//div[contains(text(), "Feels")]/text() | //div[contains(text(), "odczuwalna")]/text()')
    odczuwalna = feels_like[0].replace('\xa0', '') if feels_like else "Brak danych"
    
    wind_data = tree.xpath('//div[contains(@class, "wind")]/text() | //div[contains(text(), "Wind")]/text()')
    wind = wind_data[0] if wind_data else "Brak danych"
    wind_dir = wind_data[1] if len(wind_data) > 1 else ""
    
    print(f"Pogoda dla miasta {city}:")
    print(f"Temperatura: {temp}")
    print(f"Opis: {desc}")
    print(f"Odczuwalna: {odczuwalna}")
    print(f"Wiatr: {wind}")
    if wind_dir:
        print(f"Kierunek wiatru: {wind_dir}")

except Exception as e:
    print(f"Wystąpił błąd: {e}")
    sys.exit(1)

try:
    # Prognoza godzinowa
    url=f'https://www.timeanddate.com/weather/poland/{normalized_city.lower()}/hourly'
    response=requests.get(url)
    
    if response.status_code != 200:
        print("Nie można pobrać prognozy godzinowej.")
        raise Exception("Błąd pobierania prognozy godzinowej")
        
    tree=html.fromstring(response.content)
    hours=[]
    temps1=[]
    odcz_temp=[] 
    descs1=[]
    wind1=[]
    wind_dir1=[]
    rain_chance=[]
    rain=[]

    # Poprawione XPath queries dla prognozy godzinowej
    for i in range(1, 25):
        row_data = tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]')
        if row_data:
            hours.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/th/text()') or ["Brak danych"])
            temps1.append([temp.replace('\xa0', '') for temp in (tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[2]/text()') or ["N/A"])])
            descs1.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[3]/text()') or ["Brak danych"])
            odcz_temp.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[4]/text()') or ["Brak danych"])
            wind1.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[5]/text()') or ["Brak danych"])
            rain_chance.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[8]/text()') or ["0%"])
            rain.append(tree.xpath(f'//*[@id="wt-hbh"]/tbody/tr[{i}]/td[9]/text()') or ["0mm"])

    if hours:
        print("\nPrognoza godzinowa:")
        print(f"{"Godzina":<10}{"Temperatura":<15}{"Opis":<20}{"Odczuwalna":<15}{"Wiatr":<10}{"Szansa na deszcz":<20}{"Deszcz":<10}")
        for i in range(len(hours)):
            try:
                print(f"{hours[i][0]:<10}{temps1[i][0]:<15}{descs1[i][0]:<20}{odcz_temp[i][0]:<15}{wind1[i][0]:<10}{rain_chance[i][0]:<20}{rain[i][0]:<10}")
            except (IndexError, KeyError):
                continue
    else:
        print("Brak dostępnych danych godzinowych.")

    # Prognoza dzienna
    url=f"https://www.timeanddate.com/weather/poland/{normalized_city.lower()}/ext"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Nie można pobrać prognozy długoterminowej.")
        raise Exception("Błąd pobierania prognozy długoterminowej")
        
    tree=html.fromstring(response.content)
    days=[] 
    temps2=[]
    descs2=[]
    odcz_temp2=[] 
    wind2=[] 
    rain_chance2=[]
    rain2=[]

    # Poprawione XPath queries dla prognozy dziennej
    for i in range(1, 16):
        row_data = tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]')
        if row_data:
            days.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/th/text()') or ["Brak danych"])
            temps2.append([temp.replace('\xa0', '') for temp in (tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[2]/text()') or ["N/A"])])
            descs2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[3]/text()') or ["Brak danych"])
            odcz_temp2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[4]/text()') or ["Brak danych"])
            wind2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[5]/text()') or ["Brak danych"])
            rain_chance2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[8]/text()') or ["0%"])
            rain2.append(tree.xpath(f'//*[@id="wt-ext"]/tbody/tr[{i}]/td[9]/text()') or ["0mm"])

    if days:
        print("\nPrognoza na 14 dni:")
        print(f"{"Dzień":<10}{"Temperatura":<15}{"Opis":<40}{"Odczuwalna":<15}{"Wiatr":<10}{"Szansa na deszcz":<20}{"Deszcz":<10}")
        for i in range(len(days)):
            try:
                print(f"{days[i][0]:<10}{temps2[i][0]:<15}{descs2[i][0]:<40}{odcz_temp2[i][0]:<15}{wind2[i][0]:<10}{rain_chance2[i][0]:<20}{rain2[i][0]:<10}")
            except (IndexError, KeyError):
                continue

        try:
            #Wykres dzienny
            plt.figure(figsize=(10, 5))
            locale.setlocale(locale.LC_TIME, "pl_PL.UTF-8")
            days_dates = [datetime.datetime.strptime(day[0], "%d %b") for day in days if day[0] != "Brak danych"]
            
            # Dodajemy rok do daty
            for i in range(len(days_dates)):
                days_dates[i] = days_dates[i].replace(year=datetime.datetime.now().year)

            #Przygotowanie danych do wykresu
            rain_values = []
            for r in rain2:
                try:
                    value = r[0].replace('%', '').replace('mm', '').replace('-', '0')
                    rain_values.append(float(value))
                except (ValueError, IndexError):
                    rain_values.append(0.0)

            # Temperatury
            tmax = []
            tmin = []
            for temp in temps2:
                try:
                    max_min = temp[0].split('/')
                    tmax.append(float(max_min[0].replace('°C', '')))
                    tmin.append(float(max_min[1].replace('°C', '')))
                except (ValueError, IndexError):
                    continue

            if tmax and tmin and days_dates:
                # Tworzenie wykresu
                fig, ax1 = plt.subplots(figsize=(10, 5))

                # Oś temperatury
                ax1.plot(days_dates[:len(tmax)], tmax, marker='o', linestyle='-', color='r', label='Max Temp')
                ax1.plot(days_dates[:len(tmin)], tmin, marker='o', linestyle='-', color='b', label='Min Temp')
                ax1.set_xlabel("Dzień")
                ax1.set_ylabel("Temperatura (°C)", color='black')
                ax1.tick_params(axis='y', labelcolor='black')
                ax1.grid()

                # Druga oś dla opadów
                ax2 = ax1.twinx()
                ax2.bar(days_dates[:len(rain_values)], rain_values, color='navy', alpha=0.3, label='Opady deszczu')
                ax2.set_ylabel("Opady deszczu (mm)", color='navy')
                ax2.tick_params(axis='y', labelcolor='navy')

                # Formatowanie osi x
                ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
                plt.xticks(rotation=45)

                # Dodanie legendy i tytułu
                fig.suptitle(f"Prognoza pogody dla miasta {city}")
                fig.tight_layout()
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')

                plt.show()
            else:
                print("Brak wystarczających danych do utworzenia wykresu.")
        except Exception as e:
            print(f"Nie udało się utworzyć wykresu: {str(e)}")
    else:
        print("Brak dostępnych danych długoterminowych.")

except Exception as e:
    print(f"Wystąpił błąd podczas pobierania prognoz: {str(e)}")

try:
    #WYDARZENIA 
    info_url = f"https://www.rmf24.pl/regiony/{normalized_city.lower()}"
    response = requests.get(info_url)

    if response.status_code == 200:
        # Automatyczne wykrycie kodowania
        raw_content = response.content
        detected_encoding = chardet.detect(raw_content)['encoding']

        # Dekoduj zawartość strony
        decoded_content = raw_content.decode(detected_encoding)

        # Przetwórz HTML
        tree = html.fromstring(decoded_content)

        # Zbierz tytuły wiadomości
        events = []
        for xpath in [
            '//*[@id="l0"]/div[1]/div/div[1]/div/div/div[2]/h2/a/text()',
            '//*[@id="l0"]/div[2]/div/div[2]/div/div[2]/h3/a/text()',
            '//*[@id="l0"]/div[3]/div/div[2]/div/div[2]/h3/a/text()',
            '//*[@id="k3"]/li[1]/div[2]/div[2]/div/h3/a/text()',
            '//*[@id="k3"]/li[2]/div[2]/div[2]/div/h3/a/text()'
        ]:
            result = tree.xpath(xpath)
            if result:
                events.append(result)
            else:
                events.append(["Brak informacji"])

        # Zapisz do pliku tekstowego
        with open("wiadomosci.txt", "w", encoding="utf-8") as f:
            for i, tytul in enumerate(events, 1):
                f.write(f"{i}. {tytul[0]}\n")

        print("\n✅ Zapisano wiadomości do pliku wiadomosci.txt")
    else:
        print("\nNie udało się pobrać wiadomości dla tego miasta.")

except Exception as e:
    print(f"\nWystąpił błąd podczas pobierania wiadomości: {str(e)}")
