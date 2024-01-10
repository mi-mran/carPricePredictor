from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
import csv
from datetime import datetime
import os.path
from typing import Optional

@dataclass
class Car:
    year: int
    make: str
    model: str
    mileage: str
    safety: str
    vin: str
    date_scraped: str
    price: str
    fuel_type: Optional[str] = None
    engine: Optional[str] = None
    body: Optional[str] = None
    drivetrain: Optional[str] = None
    doors: Optional[str] = None
    transmission: Optional[str] = None

def write_to_csv(list_of_cars):
    file_exists = os.path.isfile("cars.csv")
    
    with open("cars.csv", mode="a") as f:
        fieldnames = [
            "year",
            "make",
            "model",
            "body",
            "doors",
            "drivetrain",
            "engine",
            "fuel_type",
            "transmission",
            "mileage",
            "safety",
            "vin",
            "date_scraped",
            "price"
        ]

        writer = csv.DictWriter(f, fieldnames = fieldnames)
        
        if not file_exists:
            writer.writeheader()

        for car in list_of_cars:
            writer.writerow(asdict(car))

list_of_cars = []

for i in range(1, 21):

    with open(f"toyota_html/page{i}.html", encoding="utf-8") as f:
        data = f.read()
        soup = BeautifulSoup(data, 'html.parser')

        cars = soup.find_all('div', attrs={"data-testid": "srp-tile-listing-standard"})
        for car in cars:
            price = car.find('h4', attrs={'data-testid': 'srp-tile-price'})
            #print(price.string)

            dt = [x.text.strip() for x in car.find_all('dt')]
            dd = [x.text.strip() for x in car.find_all('dd')]

            final = dict(zip(dt, dd))

            #print(final)

            list_of_cars.append(Car(
                year = final['Year:'],
                make = final['Make:'],
                model = final['Model:'],
                body = final.get('Body type:'),
                doors = final.get('Doors:'),
                drivetrain = final.get('Drivetrain:'),
                engine = final.get('Engine:'),
                fuel_type = final.get('Fuel type:'),
                transmission = final.get('Transmission:'),
                mileage = final['Mileage:'],
                safety = final['NHTSA overall safety rating:'],
                vin = final['VIN:'],
                date_scraped = datetime.today().strftime('%d-%m-%Y'),
                price = price.string
            ))
    
    write_to_csv(list_of_cars)