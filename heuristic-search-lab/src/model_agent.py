from src.agents import Agent

class ModelBasedPaperAgent(Agent):
    def __init__(self):
        self.spent = 0; self.buy_history = []; self.avg_price = None; self.instock = None

    def select_action(self, percept):
        self.last_price = percept['price']; self.instock = percept['instock']
        if self.avg_price is None: self.avg_price = self.last_price
        else: self.avg_price = self.avg_price + (self.last_price - self.avg_price) * 0.05
        if self.last_price < 0.9 * self.avg_price and self.instock < 60: tobuy = 48
        elif self.instock < 12: tobuy = 12
        else: tobuy = 0
        self.spent += tobuy * self.last_price; self.buy_history.append(tobuy)
        return {'buy': tobuy}