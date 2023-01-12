import math
import argparse


class CalcCrr:
    def __init__(
        self, rider_mass_kg, rear_mass_percent, dia_wheel_mm, dia_drum_mm
    ):
        super().__init__()
        self.rider_mass_kg = rider_mass_kg
        self.rear_mass_percent = rear_mass_percent
        self.dia_wheel_mm = dia_wheel_mm
        self.dia_drum_mm = dia_drum_mm
        self.hours = 1
        self.minutes = 0
        self.seconds = 0
        self.distance_km = 40
        self.roller_spread = 20
        self.p_drum_watts = 281

    def calc_mass_eff(self):

        mass_front = self.rider_mass_kg * ((100 - self.rear_mass_percent) / 100)
        mass_rear = self.rider_mass_kg - mass_front
        mass_eff = mass_front + (
            mass_rear
            / math.cos(
                math.asin(self.roller_spread / (self.dia_wheel_mm + self.dia_drum_mm))
            )
        )
        return mass_eff

    def calc_crr(self):
        g = 9.81  # meters per second

        mass_eff_kg = self.calc_mass_eff()

        distance_m = self.distance_km * 1000
        seconds_total = (((self.hours * 60) + self.minutes) * 60) + self.seconds

        v_drum_ms = distance_m / seconds_total
        crr = (self.p_drum_watts / (v_drum_ms * mass_eff_kg * g)) * math.pow(
            (1 / (1 + self.dia_wheel_mm / self.dia_drum_mm)), 0.7
        )
        return crr


def main():
    print("Calc Crr")

    parser = argparse.ArgumentParser(
        description="Calculate Crr from roller, power, and distance"
    )
    parser.add_argument(
        "--roller_spread_mm",
        type=int,
        help="Distance center to center of the rear rollers. Default 40",
        default=40,
        required=False,
    )
    parser.add_argument(
        "--rider_mass_kg",
        type=int,
        help="Weight of rider + bike + etc in kilograms. Default 93.",
        default=93,
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
        help="Diameter of the roller drums in mm. Default 114 (4.5 inch Kreitler)",
        default=114,
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
        "--avg_wattage", type=int, help="Average wattage for duration.", required=True
    )
    args = parser.parse_args()

    roller_spread_mm = args.roller_spread_mm
    print(f"roller spread mm {roller_spread_mm}")
    rider_mass_kg = args.rider_mass_kg
    rear_mass_percent = args.rear_mass_percent
    dia_wheel_mm = args.dia_wheel_mm
    dia_drum_mm = args.dia_drum_mm
    hms = args.hms
    (hours, minutes, seconds) = hms.split(":")
    distance_meters = args.distance_meters
    avg_wattage = args.avg_wattage

    c = CalcCrr(
    crr = c.calc_crr()
    print(f"Crr is {crr}")


if __name__ == "__main__":
    main()
