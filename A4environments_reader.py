# Module imports #
import csv
#print(dir(csv))

# Function to read .csv, append data to environments, and then return environments #
def readdata():
    # Sets environments as a list #
    environments = []
    # Opens and reads the a set csv #
    with open('environments1.csv', newline='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        # Reads through the rows #
        for row in reader:
            rowlist = []
            # Reads through the rows inside rows #
            for value in row:
                rowlist.append(value)
            # Appends the values of the csv to the rowlist list #
            environments.append(rowlist)
    # Returns environments which contains the rowlist lists #
    return environments
          