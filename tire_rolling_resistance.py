import math


class CalcCrr:

    def __init__(self):
        self.rider_mass_kg = 94
        self.rear_mass_percent = 60
        self.dia_wheel_cm = 655
        self.dia_drum_cm = 10
        self.hours = 56
        self.minutes = 0
        self.seconds = 0
        self.distance_km = 40
        self.roller_distance = 20
        self.p_drum_watts = 281

    def calc_mass_eff(self):

        mass_front = self.rider_mass_kg * ((100 - self.rear_mass_percent) / 100)
        mass_rear = self.rider_mass_kg - mass_front
        mass_eff = mass_front + (mass_rear / math.cos(
            math.asin(self.roller_distance / (self.dia_wheel_cm + self.dia_drum_cm))
            ))
        return mass_eff

    def calc_crr(self):
        g = 9.81  # meters per second

        mass_eff_kg = self.calc_mass_eff()

        distance_m = self.distance_km * 1000
        seconds_total = (((self.hours * 60) + self.minutes) * 60) + self.seconds

        v_drum_ms = distance_m / seconds_total
        crr = (
            (self.p_drum_watts / (v_drum_ms * mass_eff_kg * g))
            * math.pow((1 / (1 + self.dia_wheel_cm / self.dia_drum_cm)), 0.7)
        )
        return crr

def main():
    print("Calc Crr")
    c = CalcCrr();
    crr = c.calc_crr()
    print(f"Crr is {crr}")



if __name__ == "__main__":
    main()
