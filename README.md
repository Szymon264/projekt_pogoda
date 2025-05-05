# Aplikacja Pogodowa

## Opis
Aplikacja służy do sprawdzania prognozy pogody dla miast w Polsce. Pokazuje aktualną pogodę, prognozę godzinową, prognozę na 14 dni oraz generuje wykresy temperatur. Dodatkowo zbiera najnowsze wiadomości z wybranego miasta.

## Funkcjonalności
- Sprawdzanie aktualnej pogody dla dowolnego miasta w Polsce
- Prognoza godzinowa
- Prognoza na 14 dni z wykresem temperatur i opadów
- Pobieranie lokalnych wiadomości
- Obsługa polskich znaków w nazwach miast
- Porównywanie pogody w dwóch miastach (nowa funkcja!)

## Instrukcja instalacji

### Krok 1: Instalacja Pythona
1. Wejdź na stronę [Python.org](https://www.python.org/downloads/)
2. Kliknij duży przycisk "Download Python" (pobierz najnowszą wersję)
3. Po pobraniu uruchom instalator
4. **WAŻNE**: Zaznacz opcję "Add Python to PATH" podczas instalacji
5. Kliknij "Install Now"

### Krok 2: Pobranie programu
1. Kliknij zielony przycisk "Code" na górze tej strony
2. Wybierz "Download ZIP"
3. Rozpakuj pobrany plik w wybranym miejscu na komputerze

### Krok 3: Instalacja wymaganych bibliotek
1. Otwórz Command Prompt (cmd):
   - Naciśnij klawisz Windows + R
   - Wpisz "cmd" i naciśnij Enter
2. Przejdź do folderu z programem:
   - Wpisz `cd` i ścieżkę do folderu, gdzie rozpakowałeś/aś program
3. Zainstaluj wymagane biblioteki:
   - Wpisz komendę: `pip install -r requirements.txt`
   - Poczekaj aż wszystkie biblioteki się zainstalują

### Krok 4: Uruchomienie programu
1. W tym samym oknie Command Prompt wpisz:
   `python scraper.py`
2. Program się uruchomi i poprosi o podanie nazwy miasta
3. Wpisz nazwę miasta (bez polskich znaków) i naciśnij Enter

## Jak używać

### Podstawowe sprawdzanie pogody
1. Uruchom program komendą:
   `python scraper.py`
2. Wpisz nazwę miasta (możesz użyć polskich znaków, np. "Kraków", "Gdańsk")
3. Program pokaże:
   - Aktualną pogodę
   - Prognozę godzinową
   - Prognozę na 14 dni
   - Wykres temperatur
   - Lokalne wiadomości z miasta

### Porównywanie pogody w dwóch miastach
1. Uruchom program porównywania komendą:
   `python weather_compare.py`
2. Wpisz nazwy dwóch miast, które chcesz porównać
3. Program pokaże:
   - Wykres porównujący temperatury w obu miastach
   - Statystyki temperatur dla każdego miasta
   - Różnice temperatur między miastami

## Rozwiązywanie problemów
- Jeśli pojawi się błąd z bibliotekami, spróbuj ponownie wykonać krok 3
- Upewnij się, że nazwa miasta jest wpisana bez polskich znaków
- W razie problemów z uruchomieniem, upewnij się że Python jest dodany do PATH

## Wymagania systemowe
- Windows 7 lub nowszy
- Połączenie z internetem
- Minimum 500MB wolnego miejsca na dysku