# Module imports #
import random
# Importing various user changable variables from the model.py #
from A4GUImodel import max_age,age_rate,min_move,max_move,eat_val,poo_val

# Defining Agent class #
class Agent:
    
    # This function is called when a object/agent is created to initialise the agent and its assosiated attributes #
    def __init__(self, environments, ia, agents, x, y):
        self.id = ia
        # Assings the agent a starting x, y coordinate position attained from web scraping #
        # if (x == None):
        #     self.x = random.randint(0,100)
        # else:
        #     self.x = x
        # if (x == None):
        #     self.y = random.randint(0,100)
        # else:
        #     self.y = y 
        self.environments = environments
        self.agents = agents
        self.age = 0
        self.store = 10 
        self.x = random.randint(0,299)
        self.y = random.randint(0,299)
        
    # Creating a string by collecting variables per agent #
    def __str__(self):
        return "id=" + str(self.id) + ", x=" + str(self.x) + ", y=" + str(self.y)

    # Function to move the agents around environment or stand still in a more organic manner, Order decsending: E, N, NE, W, S, SW, NW, SE #
    def move(self):
        if random.random() < 0.1:
            # The agents can move anywhere between min_move and max_move which is randomly generated #
            self.x = (self.x + random.randint(min_move,max_move)) %300
        elif random.random() >= 0.1 and random.random() <= 0.2:
            self.y = (self.y + random.randint(min_move,max_move)) %300
        elif random.random() >= 0.2 and random.random() <= 0.3:
            self.x = (self.x + random.randint(min_move,max_move)) %300
            self.y = (self.y + random.randint(min_move,max_move)) %300
        elif random.random() >= 0.3 and random.random() <= 0.4:
            self.x = (self.x - random.randint(min_move,max_move)) %300
        elif random.random() >= 0.4 and random.random() <= 0.5:
            self.y = (self.y - random.randint(min_move,max_move)) %300
        elif random.random() >= 0.5 and random.random() <= 0.6:
            self.x = (self.x - random.randint(min_move,max_move)) %300
            self.y = (self.y - random.randint(min_move,max_move)) %300
        elif random.random() >= 0.6 and random.random() <= 0.7:
            self.x = (self.x - random.randint(min_move,max_move)) %300
            self.y = (self.y + random.randint(min_move,max_move)) %300
        elif random.random() >= 0.7 and random.random() <= 0.8:
            self.x = (self.x + random.randint(min_move,max_move)) %300
            self.y = (self.y - random.randint(min_move,max_move)) %300
        else:
            self.y = (self.y) 
 
    # Function to lower environment store by eat_val if environment > 0 and add eat_val to agent self store if environment < 0 #
    def eat(self):
        if self.environments[self.y][self.x] > 0 and self.age <= max_age:
            self.environments[self.y][self.x] = self.environments[self.y][self.x] - eat_val
            self.store += eat_val
        """ Stops environment from going negative or exceeding 300 due to excessive eating or pooing. 
        This also stops the graph environment colourmap changing colour too drastically """
        if self.environments[self.y][self.x] < 0:
            self.environments[self.y][self.x] = 0
        if self.environments[self.y][self.x] > 300:
            self.environments[self.y][self.x] = 300

    # Function to return poo_val store value to the environment when store => 100 and poo_role > 0 # 
    def poo(self):
        poo_roll = random.random()
        # This is effectivly the inverse of the eat function #
        if self.store > 100 and poo_roll > 0.8:
            self.environments[self.y][self.x] = self.environments[self.y][self.x] + poo_val
            self.store -= poo_val
          
    # Causes nibbler to shrink (by 3 store - linked to plot size) and die once their age >= max_age #      
    def die(self):
        if self.age >= max_age:
            self.store -= 3
            if self.store < 0:
                self.store = 0

    # Reposition dead nibbler to their grave which is off the visable graph #
    def grave(self):
            self.x = -100
            self.y = -100

    # Assigning each agent an age which increases every iteration by age_rate #
    def ageing(self):
        self.age += (age_rate)
        
    # Divides the agents' current store by 2 - used in birthing to avoid births in adjacent frames #
    def store_half(self):
        self.store = (self.store // 2)
        
    # Slowing with age function which is used within the age_slowing_move function to slow agents at higher ages #
    def slowing(self):
        self.y = (self.y)
        self.x = (self.x)

    """When an agent is between set ages they have a random chance of running the slowing function - the chance this will occour 
    increases within 3 age brackets until max_age is reached where slowing is every iteration and the die function runs"""
    def age_slowing_move(self):
        age_roll = random.random()
        if self.age >= (max_age*0.5) and self.age <= (max_age*0.666) and age_roll < 0.1:
            self.slowing()
        elif self.age >= (max_age*0.666) and self.age <= (max_age*0.833) and age_roll < 0.3:
            self.slowing()
        elif self.age >= (max_age*0.833) and self.age <= max_age and age_roll < 0.75:
            self.slowing()
        elif self.age >= max_age and age_roll < 1:
            self.slowing()
        else:
            self.move()
        
    # Function to share store with eachother by adding close proximity agents store together and then store/2 #
    def share_with_neighbours(self, neighbourhood):
       for agent in self.agents:
           dist = self.distance_between(agent)
           if dist <= neighbourhood:
               sum = self.store + agent.store
               ave = sum / 2
               self.store = ave
               agent.store = ave
               ("sharing " + str(dist) + " " + str(ave))
                              
    # Function which returns for an agent to all other agents #
    def distance_between(self, agent):
        return(((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5