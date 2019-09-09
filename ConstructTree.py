import os
from DirTree import DirTree


# Node construction founction.
# This is a recursive function which will create a tree of
# DirTree nodes for each folder and each file within that folder.
def constructTree(name, path):


    # Get the directory contents
    try:
        totalnames = os.listdir(path)
    except:
        return None

    # Set up variables
    files = []
    folders = []
    children = []

    # Seperate into files and directories
    for item in totalnames:
        if "." in item:
            files.append(item)
        else:
            folders.append(item)

    # For each folder recur the fuction
    for folder in folders:
        filepath = extFilepath(path, folder)
        node = constructTree(folder, filepath)
        if node != None:
            children.append(constructTree(folder, filepath))

    # Base case, create current node and return
    newNode = DirTree(name, files, path, children)
    return newNode

# Writes the correct filepath
def extFilepath(path, folder):
    if path == ".":
        return folder
    else:
        return path + "\\" + folder
