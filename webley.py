import csv
import sys
import pathlib


class Solution:

    def __init__(self):
        self.result = []
        self.target_price = None
        self.menu = []

    def handle_file_error(self):
        print('Please provide a valid csv file in the following format. (python webley.py example.csv)')
        print("""
        Target price, $14.55

        mixed fruit,$2.15
        french fries,$2.75
        side salad,$3.35
        hot wings,$3.45
        mozzarella sticks,$4.20
        sampler plate,$5.80
                    """)

    def get_price(self, raw_price):
        """
        convert raw price to float
        :param raw_price: raw price in string format
        :return: price in float format
        """
        try:
            price = float(raw_price.split('$')[-1])
        except ValueError:
            print("Invalid price")
            sys.exit()
        return price

    def parse_csv(self, csv_file):
        """
        parse the csv file
        :param csv_file: csv file name
        :return: True when file is successfully parsed
        """
        current_dir = pathlib.Path.cwd()
        file = pathlib.Path(current_dir, csv_file)
        if file.exists():
            with open(file, mode='r') as f:
                csv_reader = csv.reader(f)
                first_row = next(csv_reader, None)
                if not first_row:
                    self.handle_file_error()
                    return False

                if 'Target price' in first_row:
                    self.target_price = self.get_price(first_row[1])

                for row in csv_reader:
                    if row:
                        menu_item, menu_price = row[0], self.get_price(row[1])
                        self.menu.append((menu_item, menu_price))

                # sort the menu by price for fast lookup
                self.menu.sort(key=lambda x: x[1])

                return True
        self.handle_file_error()
        return False

    def find_combination(self, target, index, current):
        """
        a recursive function to find the right combination
        :param target: the target price
        :param index: current index
        :param current: current combination
        :return:
        """
        if target == 0.0:
            # hard copy the current combination
            self.result = list(current)
            return True

        for i in range(index, len(self.menu)):
            if target < self.menu[i][1]:
                break
            current.append(i)
            found = self.find_combination(target-self.menu[i][1], i, current)
            if found:
                return True
            else:
                current.pop()

    def solution(self):
        args = sys.argv
        if len(args) < 2:
            self.handle_file_error()
        else:
            parse_result = self.parse_csv(str(args[1]))
            if parse_result:
                self.find_combination(self.target_price, 0, [])
                if self.result:
                    print("We can order the following dishes given the target price $%f:" % self.target_price)
                    for i in self.result:
                        print(self.menu[i][0], ''.join(['$', str(self.menu[i][1])]))
                else:
                    print("There is no combination of dishes that is equal to the target price")


s = Solution()
s.solution()
