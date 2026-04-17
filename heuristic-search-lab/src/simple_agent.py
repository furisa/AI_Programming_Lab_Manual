from src.agents import Agent

class SimplePaperAgent(Agent):
    def __init__(self):
        self.spent = 0; self.buy_history = []; self.last_price = None

    def select_action(self, percept):
        price = percept['price']; instock = percept['instock']; self.last_price = price
        if instock < 10: tobuy = 20
        elif instock < 20: tobuy = 10
        elif price < 200: tobuy = 5
        else: tobuy = 0
        self.spent += tobuy * price; self.buy_history.append(tobuy)
        return {'buy': tobuy}