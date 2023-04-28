from pokerPlayer import pokerPlayer
from learningPlayer import learningPlayer
from pokerGame import pokerGame

def main():
    #state = np.array([2500, 250, 50])
    state_size = 625000

    #action space range is [0, 1]
    action_size = 1

    #def __init__(self, name, state_size, action_size, learning_rate, tau):
    #learningPlayer("DDPG nerd", state_size, action_size, .002, 0.005)
    list = [pokerPlayer("Player1"),
            pokerPlayer("Player2"),
            pokerPlayer("Player3"),
            pokerPlayer("Player4"),
            pokerPlayer("Player5"),
            pokerPlayer("Player6"),
            pokerPlayer("Player7"),
            pokerPlayer("Player8"),
            pokerPlayer("Player9")]

    game = pokerGame(list, 100, 20)
    game.play()

if __name__ == "__main__":
    main()
