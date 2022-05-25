import argparse

class Car:
    def __init__(self, plate_number, age_of_driver):
        self.plate_number = plate_number
        self.age_of_driver = age_of_driver


class ParkingLot:
    def __init__(self):
        self.capacity = 0
        self.slot_id = 0
        self.slots_used = 0

    def create_parking_space(self, capacity):
        self.slots = [-1] * capacity
        self.capacity = capacity
        return self.capacity

    def get_empty_slot(self):
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                return i

    def park(self, plate_number, age):
        if self.slots_used < self.capacity:
            slot_id = self.get_empty_slot()
            self.slots[slot_id] = Car(plate_number, age)
            self.slot_id += 1
            self.slots_used += 1
            return slot_id+1
        else:
            return -1

    def leave(self, slot_id):
        if self.slots_used > 0 and self.slots[slot_id - 1] != -1:
            self.slots[slot_id-1] = -1
            self.slots_used -= 1
            return True
        else:
            return False

    def status(self):
        print("Slot_id\tPlate_number\tAge_of_driver")
        for i in range(len(self.slots)):
            if self.slots[i] != -1:
                print(str(i+1) + '\t' + str(self.slots[i].plate_number) + '\t' + str(self.slots[i].age_of_driver))

    def get_slot_from_plate(self, plate_number):
        for slot in self.slots:
            if slot.plate_number == plate_number:
                return self.slots.index(slot)+1
        return -1

    def get_slot_from_age(self, age):
        slot_list = []
        for slot in self.slots:
            if slot == -1:
                continue
            if slot.age_of_driver == age:
                slot_list.append(str(self.slots.index(slot)+1))
        return slot_list

    def get_plate_from_age(self, age):
        slot_list = []
        for slot in self.slots:
            if slot == -1:
                continue
            if slot.age_of_driver == age:
                slot_list.append(str(slot.plate_number))
        return slot_list

    def get_data(self, command):
        if command.startswith('Create_parking_lot'):
            n = int(command.split(' ')[1])
            result = self.create_parking_space(n)
            print(f"Created parking lot of {n} slots")

        elif command.startswith('Park'):
            plate_number = command.split(' ')[1]
            age = command.split(' ')[3]
            result = self.park(plate_number, age)
            print(f'Car with vehicle registration number "{plate_number}" has been parked at slot number {result}')

        elif command.startswith('Slot_numbers_for_driver_of_age'):
            age = command.split(' ')[1]
            slots = self.get_slot_from_age(age)
            print(', '.join(slots))

        elif command.startswith('Slot_number_for_car_with_number'):
            plate_number = command.split(' ')[1]
            slot = self.get_slot_from_plate(plate_number)
            print(slot)

        elif command.startswith('Vehicle_registration_number_for_driver_of_age'):
            age = command.split(' ')[1]
            slot = self.get_plate_from_age(age)
            if not slot:
                print('\n')
            else:
                for i in slot:
                    print(i)

        elif command.startswith('Leave'):
            leave_slot_id = int(command.split(' ')[1])
            vehicle = self.slots[leave_slot_id-1]
            response = self.leave(leave_slot_id)
            if response:
                print(f'Slot number {leave_slot_id} vacated, the car with vehicle registration number "{vehicle.plate_number}" left the space, the driver of the car was of age {vehicle.age_of_driver}')

        elif command.startswith('status'):
            self.status()

        elif command.startswith('exit'):
            exit(0)


def cli():
    parking_lot = ParkingLot()
    parser_class = argparse.ArgumentParser()
    parser_class.add_argument('-i', action='store', required=False, dest='src_file', help="input test file")
    args = parser_class.parse_args()

    if args.src_file:
        with open(args.src_file) as file:
            for command in file:
                command = command.strip('\n')
                parking_lot.get_data(command)
    else:
        while True:
            command = input(">")
            parking_lot.get_data(command)


if __name__ == '__main__':
    cli()
