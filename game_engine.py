import random
from datetime import datetime
from typing import List



'''
This is where most of the backend and game logic will be managed

=== sanity checks === 
    - cant run two games at once, and only Game Masters are allowed to start and stop games 
    - players should be allowed to forfiet the game 
    - need a way to add and remove players mid game 
    - Need a way to pause the timer for the last two players

    - Game and Player follow a Linked List and Node structure, there are other functionalities that need to be addressed but that is the general flow 
    - When there are two players left, they both have an hour to kill eachother lol 
    - every time someone dies, It says that they have been eliminated (have to do this in the correct channel) 
    
    - Jhon Wick Mode

=== functions ===

new_game(.txt file) - starts a brand new game with the text files of all the players in the game
                      the function then generates a list with player objects, assigns contracts, 
                      and dm's each player who their targets are
'''


class Player():
    '''
    Representation of a Assasin Player.

    === Attributes === 
    
    _id: the id used by discord to identify a user
    username: The Discord username used by a player, it is in the form of Username#0000
    net_worth: how much money the player has accumulated during the game
    secret: is given to the contractor if you are unalived, must remain a secret!
    target: the person you have to unalive to survive!

    === types === 
    _id: int
    username: string
    net_worth: int
    secret: int
    target: Player
    '''

    def __init__(self, id:int, name:str, disc:str) -> None:
        '''
        <id> Discord id, <name> Discord username before #, <disc> the Discriminator i.e numbers after #
        This function instantiates a new Player object
        '''
        self._id = int(id)
        self.username = f"{name}#{disc}"
        self.net_worth = 0 
        self.secret = random.randint(100, 999)
        self.target = None

    def __str__(self) -> str:
        '''Returns the string reprsentation of this Player'''
        return f"{self.username} | {self.secret}"

    def __repr__(self) -> str:
        '''Returns the string reprsentation of this Player'''
        return f"{self.username} | {self.secret}"

    def __eq__(self, other) -> bool: 
        ''' returns true if this Player == Other'''
        return self._id == other._id

    def getId(self) -> int:
        ''' Returns the _id attribute to send to the bot to fetch the user '''
        return self._id
    
    def getSecret(self) -> int: 
        return self.secret
    
    def assignTarget(self, other) -> None: 
        '''Assigns <other> as the target for this player'''
        self.target = other
    
    def getTarget(self):
        '''Returns the Player object who is the target for this PLayer'''
        return self.target 

    def deactivate(self) -> None: 
        ''' "Kills" the player, removing them from the game'''
        self.target = None

    def isEmpty(self) -> bool:
        '''returns True if player is Player(0, "Empty", "0000")'''
        return self._id == 0
        pass

class Game(): 
    '''
    Represents a game of Assasin

    === Attributes === 
    players: list of all the active players in the game

    '''

    def __init__(self, players:list[Player]) -> None:
        '''Initalizes all the variables needed for the game to run'''
        self.players = players
        self.manifest = 'path/to/csvfile'
        self.active = len(players)
        self.ded = 0
        self.start = datetime.now()
        self.winner = Player

    def __str__(self) -> str:
        '''
        A string representation of the game, looks something like this: 

        Game start: 2022-10-03 10:24:13.694413
        Players: [Ténèbres#4025, Katote#0006, Alpha Swine#8938, ScoobyDoo-Lunchables#0095, NotPerryThePlatypus#2520, Exia#3417]
        Active Agents: 10
        Fallen Agents: 3
        ''' 
        return f"Game start: {self.start}\nPlayers: {self.players}\nActive Agents: {self.active}\nFallen Agents: {self.ded}"
    
    def __repr__(self) -> str: 
        return f"Game start: {self.start}\nPlayers: {self.players}\nActive Agents: {self.active}\nFallen Agents: {self.ded}"

    def _contracts(self) -> str: 
        '''returns a string representation of all the contracts in the game'''
        cons = ''
        for p in self.players:
            cons += f"{p} → {p.target}\n"
        
        return cons


    def addPlayer(self) -> None: 
        pass
    
    def removePlayer(self) -> None: 
        pass
    
    def returnById(self, id) -> Player or None:
        for p in self.players: 
            if p.getId() == id: 
                return p 
        return None

    def completeContract(self, pid:int, secret:str) -> List[Player] or None: 
        ''' 
        This function finds the player with the secret <Player.secret> and transfers their target
        to player with the id <pid>
        
        Returns [Assasin w/new target, Old Target] if contract was a success
        Returns [Empty Player, Assassin] if contract was a success and Assassin is the last player left
        Returns None if contract was unsucessful
        
        '''

        assassin = self.returnById(pid)
        target = assassin.getTarget()

        if int(secret) == target.secret: 
            assassin.assignTarget(target.getTarget())
            target.deactivate()
            self.active -=1 
            self.ded += 1

            if self.active == 1: 
                return [Player(0, "Empty", "0000"), assassin] #returns an "empty" player
            
            return [assassin, target]
            
        else:
            if self.active == 1: 
                self.winner = assassin # Assign the winner as the assassin and return an empty player
                return [Player(0, "Empty", "0000"), assassin]
            
            return None

        

        '''
        need to dm the target that they have died, message in the main chat, that there are n-1 players left, 
        need to announce the winner and also 
        '''

    def saveGame(self) -> None: 
        pass

    def getWinner(self) -> Player: 
        return str(self.winner)
    
    def assignContracts(self) -> None: 
        ''' assign's contracts the derangement way'''
        
        random.shuffle(self.players)

        for i in range(len(self.players)-1):
            self.players[i].assignTarget(self.players[i+1])
        
        self.players[-1].assignTarget(self.players[0])
        
        return self.players

