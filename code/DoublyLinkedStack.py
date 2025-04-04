class Node:
    """
    Node class, where each node has a data attribute as well as stores
    references to the previous and next nodes
    """
    def __init__(self, data):
        self.data = data
        self.last = None
        self.next = None

class DoublyLinkedStack:
    def __init__(self):
        # self.head will always reference the most recently added node of the stack
        self.head = None

    def push(self, data): 
        # adds an item to the top of the stack
        if self.head == None:
            # if the stack is empty, create a new node and set it as top of the stack
            new_node = Node(data)
            self.head = new_node
        else:
            # create a new node to be the top of the stack
            new_node = Node(data)
            # create a link between the previous head and the current new node
            # 'save' a copy of the old self.head by letting new_nodes next node reference self.head
            self.head.last = new_node
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        # remove the most recently added item and return it 
        if self.head == None:
            return None
        elif self.head.next == None:
            top_element = self.head.data
            self.head = None
            return top_element
        else:
            top_element = self.head.data
            next_head = self.head.next
            next_head.last = None
            self.head = next_head
            return top_element
        
    def top(self): 
        # return the top element, none if list is empty
        if self.head == None:
            return None
        return self.head.data
        
    def isEmpty(self):
        # return true if stack is empty
        return self.num_items == 0
    
if __name__ == "__main__":
    doubly_linked_stack_test = DoublyLinkedStack()
    doubly_linked_stack_test.push(1)
    doubly_linked_stack_test.push(2)
    doubly_linked_stack_test.pop()
    doubly_linked_stack_test.pop()
    doubly_linked_stack_test.pop()
    doubly_linked_stack_test.pop()
    doubly_linked_stack_test.pop()
    doubly_linked_stack_test.pop()
    doubly_linked_stack_test.push(1)
    doubly_linked_stack_test.push(2)
    doubly_linked_stack_test.push(3)
    doubly_linked_stack_test.push(4)
    doubly_linked_stack_test.push(5)
    doubly_linked_stack_test.push(6)
    print(doubly_linked_stack_test.top())

