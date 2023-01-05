import re
import pathlib
import os

def sorted_alphanumeric(data:list):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

class Node: #/ Double linked list.
    def __init__(self,val=None):
        self.val = val
        self.next = None
        self.previous = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self,node):
        new_node = Node(node)
        if self.head == None:
            self.head = new_node
            return
        last = self.head
        while (last.next):
            last = last.next
        last.next = new_node
        new_node.previous = last
    
    def print(self):
        current = self.head #/ Node
        while current != None:
            print(current.val)
            last = current
            current = current.next
        #/ Acá ahora current es el ultimo.
        print('backwards')
        current = last
        while current != None:
            print(current.val)
            current = current.previous

def buildLinkedList(folderpath):
    '''
    Construct the linked list with all the imgs from the filePath.
    '''
    img_list = os.listdir(folderpath)
    sorted = sorted_alphanumeric(img_list)
    linklist = LinkedList()
    for imgName in sorted:
        new_Node = pathlib.Path(folderpath).joinpath(imgName)
        linklist.append(new_Node)
    return linklist,len(img_list)
