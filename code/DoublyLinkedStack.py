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
    """
    Head will always reference the most recently added node (top of the stack)
    """
    def __init__(self):
        self.head = None

    def push(self, data): 
        """
        Add an item to the top of the stack.
        If the stack is empty, create a new node and set it as top of the stack.
        Otherwise, add a new node at the top and adjust the links.
        """
        if self.head == None:
            new_node = Node(data)
            self.head = new_node
        else:
            # If the stack isn't empty, the new node becomes the top
            new_node = Node(data)
            # Set the current head's last pointer to the new node
            self.head.last = new_node
            # Link the new node to the current head
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        """
        Remove the most recently added item from the stack and return it.
        If the stack is empty, return None.
        """
         # Stack is empty
        if self.head == None:
            return None
        
        top_element = self.head.data
        # More than one item in the stack
        if self.head.next == None:
            self.head = None
            return top_element
        
        # Only one item in the stack
        else:
            next_head = self.head.next
            next_head.last = None
            self.head = next_head
            return top_element
        
    def top(self): 
        """
        Return the top item of the stack without removing it.
        Return None if the stack is empty.
        """
        if self.head == None:
            return None
        return self.head.data
        
    def isEmpty(self):
        """
        Check if the stack is empty.
        Return True if empty, False otherwise.
        """
        return self.head == None
    
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

