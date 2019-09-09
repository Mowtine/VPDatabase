import os

# This is a data structure for the directory tree.
# Each node represents a folder and has children which have their own children
# moving deeper into the filetree.
# Each node (or folder) has a list of files within it, it's current
# directory location, the folders name and it's children.
# Note that if you want to see all the folders contents that would be both
# files and children lists added together.

class DirTree:

    def __init__(self, name, filelist, currentDirectory, children):

        self.filelist = filelist
        self.currentDir = currentDirectory
        self.children = children
        self.name = name

        # Debugging
        # print("Created "+ self.name + " located in " + self.currentDir)

    def getCurrentFilepath(self):
        return self.currentDir

    # Print the file tree and all children with the correct indent
    def printAll(self, level = 0):

        indent = " "*level

        for child in self.children:
            child.printAll(level+1)

        print(indent + "Files in " + self.name + ":")
        for file in self.filelist:
            print(indent + file)

    # Print this file.
    def printThis(self):
        print(name + " located in " + currentDir)

    # Recursive function which gets the maximum files with a htm or html filetype
    # within one folder (or node).
    def getMaxPages(self):
        maxPages = 0

        # Checks which files are htm/html files
        for fileName in self.filelist:
            # Splitting the file name
            fileSplit = fileName.split(".")
            if len(fileSplit) > 2:
                fileEnd = fileSplit[-1]
                fileTitle = fileSplit[0]
                for i in range(len(fileSplit) - 2):
                    fileTitle = "." + fileSplit[i+1]
            else:
                [fileTitle, fileEnd] = fileSplit

            # checking if it is contains htm in its name
            if "htm" in fileEnd:
                maxPages += 1

        # Checks if there is a larger maxPages in it's children
        for child in self.children:
            newMax = child.getMaxPages()
            if newMax > maxPages:
                maxPages = newMax

        # returns the maximum pages in it and its children
        return maxPages
