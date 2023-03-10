import math
import argparse
import csv
from os.path import exists


class CalcCrr:
    def __init__(
        self,
        rider_mass_kg,
        rear_mass_percent,
        dia_wheel_mm,
        dia_drum_mm,
        hours,
        minutes,
        seconds,
        distance_meters,
        roller_spread_mm,
        avg_watts,
    ):
        super().__init__()
        self.rider_mass_kg = rider_mass_kg
        self.rear_mass_percent = rear_mass_percent
        self.dia_wheel_mm = dia_wheel_mm
        self.dia_drum_mm = dia_drum_mm
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.distance_meters = distance_meters
        self.roller_spread_mm = roller_spread_mm
        self.avg_watts = avg_watts

    def calc_mass_eff(self):
        mass_rear = self.rider_mass_kg * (self.rear_mass_percent / 100)
        mass_front = self.rider_mass_kg - mass_rear
        mass_eff = mass_front + (
            mass_rear
            / math.cos(
                math.asin(
                    self.roller_spread_mm / (self.dia_wheel_mm + self.dia_drum_mm)
                )
            )
        )
        print(f"mass eff {mass_eff}")
        return mass_eff

    def calc_crr(self):
        g = 9.81  # meters per second

        mass_eff_kg = self.calc_mass_eff()

        seconds_total = (((self.hours * 60) + self.minutes) * 60) + self.seconds
        print(f"seconds total {seconds_total}")

        v_drum_ms = self.distance_meters / seconds_total
        print(f"v_drum_ms {v_drum_ms}")
        crr = (self.avg_watts / (v_drum_ms * mass_eff_kg * g)) * math.pow(
            (1 / (1 + self.dia_wheel_mm / self.dia_drum_mm)), 0.7
        )
        return crr


def add_to_csv(tire_file_name, a_row):

    header_row = [
        "rider_mass_kg",
        "rear_mass_percent",
        "dia_wheel_mm",
        "dia_drum_mm",
        "hours",
        "minutes",
        "seconds",
        "distance_meters",
        "roller_spread_mm",
        "avg_watts",
        "tire_pressure_psi",
        "tire_name",
        "Crr",
    ]
    add_header = False
    if not exists(tire_file_name):
        add_header = True
    with open(tire_file_name, "a") as csvfile:
        tire_writer = csv.writer(csvfile)
        if add_header:
            tire_writer.writerow(header_row)
        tire_writer.writerow(a_row)


def main():

    parser = argparse.ArgumentParser(
        description="Calculate Crr from roller, power, and distance"
    )
    parser.add_argument(
        "--roller_spread_mm",
        type=int,
        help="Distance center to center of the rear rollers. Default 257",
        default=257,
        required=False,
    )
    parser.add_argument(
        "--rider_mass_kg",
        type=int,
        help="Weight of rider + bike + etc in kilograms. Default 103.",
        default=103,
        required=False,
    )
    parser.add_argument(
        "--rear_mass_percent",
        type=int,
        help="Percentage of weight on rear wheel. Default 60",
        default=60,
        required=False,
    )
    parser.add_argument(
        "--dia_wheel_mm",
        type=int,
        help="Diameter of the wheel in millimeters to outside of tire. Default =  689 (700c with 38mm tire)",
        default=689,
        required=False,
    )
    parser.add_argument(
        "--dia_drum_mm",
        type=int,
        help="Diameter of the roller drums in mm. Default 85 (Travel Track Alloy)",
        default=85,
        required=False,
    )
    parser.add_argument(
        "--hms",
        help="Hours minutes and seconds of ride time in hh:mm:ss format.",
        required=True,
    )
    parser.add_argument(
        "--distance_meters",
        type=int,
        help="Distance traveled in meters.  Wheel circumference x revolutions.",
        required=True,
    )
    parser.add_argument(
        "--avg_watts", type=int, help="Average wattage for duration.", required=True
    )
    parser.add_argument(
        "--tire_pressure_psi",
        type=int,
        help="Tire pressure in psi...for recording purposes only",
        required=True,
    )
    parser.add_argument(
        "--tire_name",
        help="Name of tire with size. Eg Challenge Strada Bianca 700x36",
        required=True,
    )
    args = parser.parse_args()

    roller_spread_mm = args.roller_spread_mm
    rider_mass_kg = args.rider_mass_kg
    rear_mass_percent = args.rear_mass_percent
    dia_wheel_mm = args.dia_wheel_mm
    dia_drum_mm = args.dia_drum_mm
    hms = args.hms
    (hours_str, minutes_str, seconds_str) = hms.split(":")
    hours = int(hours_str)
    minutes = int(minutes_str)
    seconds = int(seconds_str)
    distance_meters = args.distance_meters
    avg_watts = args.avg_watts
    tire_pressure_psi = args.tire_pressure_psi
    tire_name = args.tire_name

    c = CalcCrr(
        rider_mass_kg,
        rear_mass_percent,
        dia_wheel_mm,
        dia_drum_mm,
        hours,
        minutes,
        seconds,
        distance_meters,
        roller_spread_mm,
        avg_watts,
    )
    crr = c.calc_crr()
    print(
        f"rider_mass_kg,  rear_mass_percent,  dia_wheel_mm,   dia_drum_mm,  hours,  minutes,  seconds,  distance_meters,  roller_spread_mm,  avg_watts,  tire_pressure_psi,  tire_name,  Crr"
    )
    print(
        f"{rider_mass_kg},{rear_mass_percent},{dia_wheel_mm}, {dia_drum_mm},{hours},{minutes},{seconds},{distance_meters},{roller_spread_mm},{avg_watts},{tire_pressure_psi},{tire_name},{crr}"
    )
    add_to_csv(
        "tire_data.csv",
        [
            rider_mass_kg,
            rear_mass_percent,
            dia_wheel_mm,
            dia_drum_mm,
            hours,
            minutes,
            seconds,
            distance_meters,
            roller_spread_mm,
            avg_watts,
            tire_pressure_psi,
            tire_name,
            crr,
        ],
    )


if __name__ == "__main__":
    main()
