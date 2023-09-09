import requests
from datetime import datetime
import os
from tabulate import tabulate

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        # Substitua 'SuaChaveAPI' pela sua chave de API aqui
        url = f"URL_DO_SEU_ENDPOINT/weather?q={city}&appid={self.api_key}&units=metric&lang=pt_br"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Erro ao obter dados de previsão do tempo.")
            return None

    def get_weekly_weather(self, city):
        # Substitua 'SuaChaveAPI' pela sua chave de API aqui
        url = f"URL_DO_SEU_ENDPOINT/forecast?q={city}&appid={self.api_key}&units=metric&lang=pt_br"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Erro ao obter dados de previsão do tempo.")
            return None

class WeatherApp:
    def __init__(self, api_key):
        self.api = WeatherAPI(api_key)

    def run(self):
        while True:
            self.clear_screen()
            print("\n------------ MENU ------------------")
            print("1 - Previsão do tempo atual")
            print("2 - Previsão semanal")
            print("3 - Previsão de um dia específico")
            print("4 - Dados adicionais de previsão")
            print("\n0 - Sair")
            print("------------------------------------")

            try:
                choice = int(input("Digite o número da opção desejada: "))
                if choice == 1:
                    self.clear_screen()
                    self.get_current_weather()
                elif choice == 2:
                    self.clear_screen()
                    self.get_weekly_weather()
                elif choice == 3:
                    self.clear_screen()
                    self.get_specific_day_weather()
                elif choice == 4:
                    self.clear_screen()
                    self.additional_forecast_data()
                elif choice == 0:
                    self.clear_screen()
                    print("Saindo do programa...")
                    break
                else:
                    print("Opção inválida! Digite um número válido.")
            except ValueError:
                print("Por favor, digite um número.")
            input("\nPressione Enter para continuar...")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_current_weather(self):
        city = input("Digite o nome da cidade para ver a previsão do tempo: ")
        data = self.api.get_weather(city)

        if data:
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            print(f"\nPrevisão do tempo para {city}:")
            print(f"Descrição: {description}")
            print(f"Temperatura: {temp}°C")

    def get_weekly_weather(self):
        city = input("Digite o nome da cidade para ver a previsão semanal: ")
        data = self.api.get_weekly_weather(city)

        if data:
            table_data = []
            for forecast in data['list']:
                date_str = forecast['dt_txt']
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                day = date.strftime('%d/%m/%Y')
                description = forecast['weather'][0]['description']
                temp = forecast['main']['temp']
                table_data.append([day, description, f"{temp}°C"])

            print(f"\nPrevisão semanal para {city}:")
            headers = ["Data", "Descrição", "Temperatura"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
    def get_specific_day_weather(self):
        city = input("Digite o nome da cidade: ")
        date_str = input("Digite a data (formato: AAAA-MM-DD): ")
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            data = self.api.get_weekly_weather(city)
            if data:
                print(f"\nPrevisão para {city} no dia {date_str}:")
                for forecast in data['list']:
                    forecast_date_str = forecast['dt_txt'].split()[0]
                    forecast_date = datetime.strptime(forecast_date_str, '%Y-%m-%d')
                    if forecast_date == date:
                        description = forecast['weather'][0]['description']
                        temp = forecast['main']['temp']
                        print(f"Descrição: {description.capitalize()}")
                        print(f"Temperatura: {temp}°C")
                        break
                else:
                    print(f"Previsão não encontrada para {city} no dia {date_str}.")
        except ValueError:
            print("Data inválida! Certifique-se de usar o formato correto (AAAA-MM-DD).")

    def additional_forecast_data(self):
        city = input("Digite o nome da cidade para ver os dados adicionais de previsão: ")
        data = self.api.get_weekly_weather(city)

        if data:
            print(f"\nDados adicionais de previsão para {city}:")
            previous_date = None
            for forecast in data['list']:
                date_str = forecast['dt_txt']
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                day = date.strftime('%d/%m/%Y')
                time = date.strftime('%H:%M')
                description = forecast['weather'][0]['description']
                temp = forecast['main']['temp']

                if previous_date != day:
                    print(f"\nData: {day}")
                    print(f"Horário: {time}")
                    print(f"Descrição: {description}")
                    print(f"Temperatura: {temp}°C")
                    previous_date = day

            input("\nPressione Enter para continuar...")

# Substitua 'SuaChaveAPI' pela sua chave de API aqui
if __name__ == "__main__":
    api_key = 'SuaChaveAPI'
    app = WeatherApp(api_key)
    app.run()
