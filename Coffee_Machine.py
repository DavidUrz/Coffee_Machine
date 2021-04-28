import collections
import email_status
import pyautogui


BUY = "Buy"
FILL = "Fill"
TAKE = "Take"
TURN_OFF = "Turn_off"
REMAINING = "Remaining"


Consumption = collections.namedtuple(
    "Consumption", "water, milk, coffee, cups, money")


class CoffeeMachine:
    def __init__(self):
        # quantities of items the coffee machine already had
        #liters, kilograms
        self.water = 25
        self.milk = 10
        self.coffee = 0.2
        self.cups = 10
        self.money = 0
        self.running = True

    def execute_action(self, action):
        if action == BUY:
            self.buy()
        elif action == FILL:
            self.fill()
        elif action == TAKE:
            self.take()
        elif action == TURN_OFF:
            self.running = False
        elif action == REMAINING:
            self.show_remaining()
        else:
            raise NotImplementedError(action)
            

    def available_check(self, consumption):
        if self.water - consumption.water < 0.8:
            raise NotEnoughSupplyError("water")
        elif self.milk - consumption.milk < 0.8:
            raise NotEnoughSupplyError("milk")
        elif self.coffee - consumption.coffee < 0.021:
            raise NotEnoughSupplyError("coffee")
        elif self.cups - consumption.cups < 2:
            raise NotEnoughSupplyError("cups")

    def buy(self, default=None):
        if default is None:
            drink = ask_drink()
        else:
            drink = default
        if drink == 9:
            return
        espresso_cons = Consumption(
            water=0.4, milk=0, coffee=0.016, cups=1, money=4)
        latte_cons = Consumption(
            water=0.75, milk=0.75, coffee=0.020, cups=1, money=7)
        cappuccino_cons = Consumption(
            water=0.35, milk=0.75, coffee=0.012, cups=1, money=6)
        consumption = {1: espresso_cons,
                       2: latte_cons, 3: cappuccino_cons}[drink]
        try:
            self.available_check(consumption)
        except NotEnoughSupplyError as exc:
            print(exc)
        else:
            self.water -= consumption.water
            self.milk -= consumption.milk
            self.coffee -= consumption.coffee
            self.cups -= consumption.cups
            self.money += consumption.money
            pyautogui.alert("Making your coffee")

    def fill(self, default=None):
        """
        Add supplies to the machine
        """
        self.water += ask_quantity(
            "Write how many liters of water do you want to add:", default)
        self.milk += ask_quantity(
            "Write how many liters of milk do you want to add:", default)
        self.coffee += ask_quantity(
            "Write how many kg of coffee do you want to add:", default)
        self.cups += ask_quantity(
            "Write how many disposable cups of coffee do you want to add:", default)

    def take(self, default=None):
        """
        Take the money from the machine
        """
        if default is None:
            pyautogui.alert(f"The machine has ${self.money}")
        self.money = 0

    def show_remaining(self, default=None):
        """
        Display the quantities of supplies in the machine at the moment
        """
        msg = '''The coffe machine has: \n 
        liters of water: {}\n
        liters of milk: {}\n
        kgs of coffee: {}\n
        cups: {}\n
        $ worth: {}\n'''.format(self.water, self.milk, self.coffee, self.cups, self.money)
        if default is None:
            pyautogui.alert(f"Alert suplies: {msg}")
            email_status.send_email("Coffe Machine Status",
                                    msg, "dvd1493@gmail.com")
        return msg


def ask_action(default=None):
    while True:
        if default is None:
            answer = pyautogui.confirm(text="Select action",
                                       title="Election",
                                       buttons=("Buy", "Fill", "Take", "Turn_off", "Remaining"))
        else:
            answer = default
        try:
            return answer
        except ValueError:
            print(f"This answer is not valid: {answer}")


def ask_drink(default=None):
    choices = {"espresso": 1, "latte": 2,
               "cappuccino": 3, "back to main menu": 9}
    while True:
        if default is None:
            answer = pyautogui.confirm(text="Select Coffee",
                                       title="Coffee",
                                       buttons=("espresso", "latte", "cappuccino", "back to main menu"))
        else:
            answer = default
        try:
            value = choices.get(answer)
            return value
        except (KeyError):
            print("Window selection coffee closed")
        except (ValueError):
            print(f"This is not a number: {answer}")



def ask_quantity(msg, default=None):
    while True:
        if default is None:
            answer = pyautogui.prompt(msg)
        else:
            answer = default
        try:
            value = float(answer)
            if value >= 0:
                return value
            print(f"This answer is not valid: {answer}")
        except ValueError:
            print(f"This is not a number: {answer}")


class NotEnoughSupplyError(Exception):
    def __init__(self, supply):
        msg = f"Sorry, not enough {supply}"
        email_status.send_email(
            "Coffe Machine Alert", f"Alert for Suplies {supply}", "dvd1493@gmail.com")
        super(NotEnoughSupplyError, self).__init__(msg)


def main():
    machine = CoffeeMachine()
    while machine.running:
        action = ask_action()
        try:
            machine.execute_action(action)
        except(NotImplementedError):
            print("Window action selection closed")


if __name__ == '__main__':
    main()
