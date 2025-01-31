# state.py

class GameState:
    _instance = None

    def __new__(cls, initial_state="Human Playing"):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, initial_state="Human Playing"):
      if self.__initialized:
          return
      self.__initialized = True
      
      self.state = initial_state
      self.possible_states = ["AI Playing", "Human Playing"]
      if self.state not in self.possible_states:
          raise ValueError(f"Invalid initial state '{initial_state}'. Must be one of: {self.possible_states}")

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        if new_state not in self.possible_states:
            raise ValueError(f"Invalid state '{new_state}'.  Must be one of: {self.possible_states}")
        self.state = new_state

