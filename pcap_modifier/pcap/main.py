import os
import subprocess
from procedure_codes import procedure_codes
from protocol_ie_ids import protocol_ie_ids

def modify_file_hex():
    # Function to get the file name
    def get_file_name():
        file_name = input("Enter your pcap file: ")
        return file_name

    # Function to get the user's choice
    def get_choice(choices):
        for key, description in choices.items():
            print(f"{key}. {description}")
        try:
            choice = int(input("Select: "))
            if choice not in choices:
                raise ValueError("Wrong Choice.")
            return choice
        except ValueError:
            print("Wrong Choice.")
            return None

    # Function to get the new value in decimal
    def get_new_value():
        try:
            new_value_decimal = int(input("Enter new value (Decimal): "))
            if not (0 <= new_value_decimal <= 255):
                raise ValueError("Enter a value between 0 and 255.")
            return new_value_decimal
        except ValueError:
            print("Enter a correct decimal value.")
            return None

    # Main loop
    while True:
        print("1. Modify Mode")
        print("2. Attack Mode")
        try:
            mode_choice = int(input("Select Mode: "))
            if mode_choice == 1:
                file_name = get_file_name()
                if not os.path.isfile(file_name):
                    print(f"The file {file_name} does not exist.")
                    continue

                data = None
                with open(file_name, 'rb') as file:
                    data = bytearray(file.read())

                positions = {
                    0: "SAVE",
                    1: "Customization",
                    2: "initial-procedure code",
                    3: "Item 0 - ProtocolIE - id",
                }

                modifications = []

                while True:
                    print("Where do you want to modify:")
                    choice = get_choice(positions)
                    if choice is None:
                        continue

                    if choice == 0:
                        base_name, ext = os.path.splitext(file_name)
                        default_file_name = f"{base_name}_modified{ext}"
                        new_file_name = input(f"Enter the file name to save [{default_file_name}]: ") or default_file_name
                        with open(new_file_name, 'wb') as new_file:
                            new_file.write(data)
                        print(f"File saved as {new_file_name}.")
                        break
                    elif choice == 1:
                        try:
                            position = int(input("Enter where to modify (Decimal) or 0 to go back: "))
                            if position == 0:
                                continue
                            new_value_decimal = get_new_value()
                            if new_value_decimal is None:
                                continue
                            new_value = new_value_decimal.to_bytes(1, 'big')
                            modifications.append((position, new_value))
                            print("!!! Successfully modified !!!")
                        except ValueError:
                            print("Enter correct decimal value.")
                            continue
                    elif choice == 2:
                        while True:
                            print("Select the ProcedureCode you want to modify to:")
                            procedure_codes_with_back = {0: "Previous screen"}
                            procedure_codes_with_back.update(procedure_codes)
                            procedure_choice = get_choice(procedure_codes_with_back)
                            if procedure_choice is None or procedure_choice == 0:
                                break
                            new_value_decimal = procedure_choice
                            position = 103
                            new_value = new_value_decimal.to_bytes(1, 'big')
                            modifications.append((position, new_value))
                            print("!!! Successfully modified !!!")
                            break
                    elif choice == 3:
                        while True:
                            print("Select the ProtocolIE-ID you want to modify to:")
                            protocol_ie_ids_with_back = {0: "Previous screen"}
                            protocol_ie_ids_with_back.update(protocol_ie_ids)
                            protocol_choice = get_choice(protocol_ie_ids_with_back)
                            if protocol_choice is None or protocol_choice == 0:
                                break
                            new_value_decimal = protocol_choice
                            position = 110
                            new_value = new_value_decimal.to_bytes(1, 'big')
                            modifications.append((position, new_value))
                            print("!!! Successfully modified !!!")
                            break
                    else:
                        print("Wrong Choice.")
                        continue

                    for pos, val in modifications:
                        data[pos] = val[0]

            elif mode_choice == 2:
                attack_options = {
                    1: "Replay pcap",
                    2: "Select attack mode (To be implemented)"
                }
                attack_choice = get_choice(attack_options)
                if attack_choice == 1:
                    pcap_file_name = input("Enter your pcap file: ")
                    command = f"sudo ./5greplay replay -t {pcap_file_name}"
                    os.system(command)
                elif attack_choice == 2:
                    print("Select attack mode to be implemented.")
                else:
                    print("Wrong Choice.")
            else:
                print("Wrong Mode Choice.")
        except ValueError:
            print("Wrong Mode Choice.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    modify_file_hex()
