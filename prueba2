# Evaluaci-n-N-2-CDI0101
import requests

FUEL_CONSUMPTION_LITERS_PER_100KM = 8.0

def geocode_city(api_key, city):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": city,
        "locale": "es",
        "limit": 1,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "hits" in data and data["hits"]:
        lat = data["hits"][0]["point"]["lat"]
        lng = data["hits"][0]["point"]["lng"]
        return f"{lat},{lng}"
    else:
        return None

def get_route(api_key, from_coords, to_coords):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [from_coords, to_coords],
        "vehicle": "car",
        "locale": "es",
        "calc_points": "true",
        "instructions": "true",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def format_duration(sec):
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    seconds = int(sec % 60)
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

def main():
    print("==== Evaluación N°2 CDI0101 ====")
    api_key = input("Ingrese su GraphHopper API Key: ").strip()
    while True:
        print("\nEscriba 'q' o 'Quit' para salir.")
        from_city = input("Ciudad de Origen: ").strip()
        if from_city.lower() in ['q', 'quit']:
            break
        to_city = input("Ciudad de Destino: ").strip()
        if to_city.lower() in ['q', 'quit']:
            break

        from_coords = geocode_city(api_key, from_city)
        to_coords = geocode_city(api_key, to_city)

        if not from_coords or not to_coords:
            print("No se pudieron encontrar las coordenadas de una o ambas ciudades. Intente con nombres más específicos.")
            continue

        data = get_route(api_key, from_coords, to_coords)
        if "paths" not in data or not data["paths"]:
            print("Error en la consulta. Verifique las ciudades y el API Key.")
            continue

        path = data["paths"][0]
        distance = path["distance"] / 1000  # metros a km
        time_sec = path["time"] / 1000      # ms a seg
        fuel_required = (distance * FUEL_CONSUMPTION_LITERS_PER_100KM) / 100

        print(f"\nDistancia: {distance:.2f} km")
        print(f"Duración: {format_duration(time_sec)}")
        print(f"Combustible requerido: {fuel_required:.2f} litros")
        print("\nNarrativa del viaje:\n")
        for instr in path["instructions"]:
            print(f"- {instr['text']}")
        print("\n---")

if __name__ == "__main__":
    main()
