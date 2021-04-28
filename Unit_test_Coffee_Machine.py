from Coffee_Machine import CoffeeMachine
from Coffee_Machine import NotEnoughSupplyError
import unittest
import collections


class TestCoffeMachine(unittest.TestCase):

    def setUp(self):
        # creation of localhost for testing
        # os.system("python -m smtpd -c DebuggingServer -n localhost:1025")
        self.machine_test = CoffeeMachine()

    def tearDown(self):
        pass

    def test_execute_action(self):
        with self.assertRaises(NotImplementedError):
            self.machine_test.execute_action("Finalize")

    def test_available_check(self):
        self.machine_test.water = 0
        Consumption = collections.namedtuple(
            "Consumption", "water, milk, coffee, cups, money")
        espresso_cons = Consumption(
            water=0.4, milk=0, coffee=0.016, cups=1, money=4)
        consumption = {1: espresso_cons}[1]

        with self.assertRaises(NotEnoughSupplyError):
            self.machine_test.available_check(consumption)

    def test_buy(self):
        self.assertEquals(self.machine_test.buy(default=9), None)

    def test_fill(self):
        self.machine_test.water = 0
        self.machine_test.fill(default=0.9)
        self.assertEquals(self.machine_test.water, 0.9)

    def test_take(self):
        self.machine_test.money = 20
        self.machine_test.take(default=1)
        self.assertEquals(self.machine_test.money, 0)

    def test_show_remaining(self):
        self.machine_test.water = 0
        self.machine_test.milk = 1
        self.machine_test.coffee = 2
        self.machine_test.cups = 3
        self.machine_test.money = 4
        self.assertEquals(self.machine_test.show_remaining(default=1), '''The coffe machine has: \n 
        liters of water: {}\n
        liters of milk: {}\n
        kgs of coffee: {}\n
        cups: {}\n
        $ worth: {}\n'''.format(0, 1, 2, 3, 4))


if __name__ == '__main__':
    unittest.main()
