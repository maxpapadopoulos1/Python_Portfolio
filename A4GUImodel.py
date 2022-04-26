# Module imports #
import matplotlib.pyplot, matplotlib.animation, matplotlib, tkinter, requests, bs4 
import A4agentframework, A4environments_reader

# Stating the backend TkAgg to use for GUI and rendering of the model #
matplotlib.use('TkAgg')

# Returns all functions and properties of any imported module used within the file #
#print(dir(tkinter)
#print(dir(bs4))
#print(dir(requests))
#print(dir(matplotlib))
#print(dir(matplotlib.animation))
#print(dir(matplotlib.pyplot))

# Error catcher p1 - Allows for handling of exceptions within the model for debugging #
try:

    # requests.get aquires the html code while the parser compiles the html into a python readable format #
    r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
    content = r.text
    soup = bs4.BeautifulSoup(content, 'html.parser')
    # fall_all is then used to collate all of a user stated attribute (i.e all of the class xs)
    td_ys = soup.find_all(attrs={"class" : "y"})
    td_xs = soup.find_all(attrs={"class" : "x"})
    #print(td_ys)
    #print(td_xs) 

    # Defining fixed variables such as agents being within a list #
    agents = []
    num_of_iterations = 1
    birth_count = 0
    death_count = 0

    # User changable variables which the program operator can set to explore the interactions of differnt variables or customise the program #
    title = "Environment w Nibblers"    # Title above the model #
    num_of_agents = 10                  # Number of agents the model starts with (Recommened = 10) #
    max_age = 300                       # Age at which the agents will die (Recommended = 300) #
    age_rate = 1                        # Age value per agent which increases per iteration (Recommended = 1) #
    min_move = 1                        # Minumum distance an agent can randomly move per iteration (Recommended = 1) #
    max_move = 3                        # Maximum distance an agent can randomly move per iteration (Recommended = 3) #
    eat_val = 10                        # The value removed from the environment/added to store when consumed (Recommended = 10) #
    poo_val = 100                       # The value added to the environment/removed from store when excreted (Recommended = 100) #
    neighbourhood = 2                   # Distance at which agents will share food with one another (Recommended = 2) #
    
    # Model functions #
    # add_agent() is used to append another agent to the list of agents#
    def add_agent():
        agents.append(A4agentframework.Agent(environments_create,len(agents),agents,x,y))
    # run() uses funcanimation to animate a widget by repeatdly calling a function which is then displayed using canvas.draw() in the GUI canvas # 
    def run():
        # animation variable is not used until the model begins and runs this function #
        animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=True, frames=num_of_iterations)
        canvas.draw()
    # TkInter function which destroys all widgets and exists the mainloop # 
    def stop():
        root.destroy()
        root.quit()
        
    # Reads in data from the environment reader which reads the .csv, appends the data to environments, and then return environments #
    environments_create = A4environments_reader.readdata()

    # for loop which returns coordinate integers from the web scraping before appending agents created by the __init __ function #      
    for i in range(num_of_agents):
        y = int(td_ys[i].text)*3
        x = int(td_xs[i].text)*3
        agents.append(A4agentframework.Agent(environments_create,i,agents,x,y)) 

    # Prints agents id and position once they have been initiated #
    for i in range(num_of_agents):
        print(agents[i])

    """ This function updates frames by clearing the prior one for the next frame to be displayed. However, it 
    also contains nested all of the actions which take place to effect the agents. This is why it must be 
    cleared each iteration to display just the updated frame """
    def update(frame_number):
        fig.clear()  

        """For loop with nested if/else statments which calls functions, which exectue actions (moving, slowing
        due to age, pooing, dying) or values, which the agents carry out when set requirments are met """
        global birth_count, death_count
        # Actions for when the agents are alive (between 0 and max_age)
        for i in range(len(agents)):
            if agents[i].age >= 0 and agents[i].age <= max_age:
                # Thier movement frequency reduces with age #
                agents[i].age_slowing_move()
                # Removes environment and adds to store #
                agents[i].eat()
                # Removes store and adds to environment #
                agents[i].poo()
                # Value that increases every iteration #
                agents[i].ageing()
                # Adds two close proximities agents store together for each then divides them both by 2 #
                agents[i].share_with_neighbours(neighbourhood)
                # Nested for loop for adding additional agents (kind of like birth) when requirements are met #
                if agents[i].store >= 230 and agents[i].age >= (max_age*0.17) and agents[i].age <= (max_age*0.666):
                    # Halfs agents store to remove ability to birth in consecutive frames #
                    agents[i].store_half()
                    # Adds another agent by initaiting and appending to the agent list #
                    add_agent()
                    # Keeps a count of the number of agents added 'birthed' in that particular run #
                    birth_count += 1
                    print("Birth no =", birth_count)
                    # Single frame change of the agents plot to a large blue circle when the requirements for adding another agent are met for analysis #
                    matplotlib.pyplot.scatter(agents[i].x,agents[i].y, color=(0,0,1), marker='o', s=1000)
            # Actions for when the agents are in a death state to reduce their size to nothing and remove them from the graph #
            else:
                agents[i].die()
            if agents[i].age == max_age:
                # Keeps a count of the number of agents that have 'died' in that particular run #
                death_count += 1
                print("Death no =", death_count)
            if agents[i].store == 0:
                agents[i].grave()
            # Print tests for agent attributes #
            #print(agents[i].store)
            #print(agents[i].distance_between)
            #print(agents[1].age)
    
        # Plotting matplotlib graph and determining various parameters of the graph #
        matplotlib.pyplot.xlim(0, 300)
        matplotlib.pyplot.ylim(0, 300)
        # Graph title can be set in the user variables #
        matplotlib.pyplot.title(title)
        matplotlib.pyplot.xlabel("X axis")
        matplotlib.pyplot.ylabel("Y axis")
        # matplotlib cmap allows for changing of the environments colour to set palletes #
        matplotlib.pyplot.set_cmap('YlGnBu')
        matplotlib.pyplot.imshow(environments_create)
        # for loop used to define and change the plots colour based on their age and size based on their store #
        for i in range(len(agents)):           
            if agents[i].age >= 0 and agents[i].age <= max_age:
                # Normalising age to a RGB format to have agents change color with age #
                a = (agents[i].age - 0)/(max_age - 0)
                b = (agents[i].age - max_age)/(0 - max_age)
                c = 0 
                # Plots the agents colour based on their age which grades up to red 1,0,0 #
                matplotlib.pyplot.scatter(agents[i].x,agents[i].y, color=(a,b,c), marker='o', s=agents[i].store)
            # Sets a plots colour to just red if it has exceeded its max_age #
            else: matplotlib.pyplot.scatter(agents[i].x,agents[i].y, color=(1,0,0), marker='o', s=agents[i].store)
    
    # Defining animation figure #
    fig = matplotlib.pyplot.figure(figsize=(7, 7))
    
    # Creating an instance of the Tk class cakked "root", naming and packing model's tkinter GUI.  #
    root = tkinter.Tk()
    root.wm_title("Model")
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas._tkcanvas.pack() 
    
    # Determining the GUI menu and events to be called when menu buttons clicked #
    menu = tkinter.Menu(root)
    root.config(menu=menu)
    model_menu = tkinter.Menu(menu)
    
    # Removed expanding boxes in favour of a cleaner more user friendly GUI #
    menu.add_cascade(label="Run Model", command=run)
    menu.add_cascade(label="Stop Model", command=stop)
    
    # Sets GUI to waiting for events/commands #
    tkinter.mainloop()

# Error catcher p2 - This displays the error within the console (ex) and a frown or if no errores are caught prints "Complete" and a smiley! #
except Exception as ex:
    print("Error =", (ex))
    print("-- Incomplete :( --")
else:
    print("-- Complete :) --")