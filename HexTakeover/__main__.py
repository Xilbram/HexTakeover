import logging
from HexTakeover.game_logic.playerinterface import PlayerInterface

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("__main__.py").info("Project has run")
    #Add your logic here
    PlayerInterface()
    
