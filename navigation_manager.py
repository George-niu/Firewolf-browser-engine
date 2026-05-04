from data_structures.linked_stack import LinkedStack
from data_structures.array_sorted_list import ArraySortedList





class NavigationManager:
    def __init__(self):
        # Initially, the address is None
        self.current_address = None

        # Used for going backward and forward
        self.back_stack = LinkedStack()
        self.forward_stack = LinkedStack()

        # Used to record all explicitly accessed addresses
        self.all_visits = ArraySortedList()

        
    
    def get_current_address(self):
        # Returns the address currently displayed by the browser.
        return self.current_address

    def go_to(self, address):
        """
        Time complexity analysis goes here.
        - Worst case: O(n)
        Because ArraySortedList is used, the add() operation requires moving O(N) elements in the worst case. 
        At the same time, if the underlying array is full, the expansion operation is also O(N).
        
        - Best Case: O(1). 
        When the insertion position is at the end and no expansion is needed, all operations take constant time.

        """
        if self.current_address is not None:
            self.back_stack.push(self.current_address)

        self.current_address = address

        # Visiting a new website will require 
        # clearing the forward history and reinitializing
        self.forward_stack = LinkedStack()

        # Record this explicit visit
        self.all_visits.add(address)

    
    def back_button_pressed(self):
        """
        Time complexity analysis goes here.
        -Worst case: O(1)
         The operations performed by this method include checking if the stack is empty (is_empty), 
         pushing an element onto the forward stack (push), and popping an element from the backward stack (pop). 
         In a LinkedStack (linked list stack), these operations only involve modifying the pointer of the head node 
         and do not depend on the number of elements in the stack. 
         Therefore, regardless of how many records are in the history, its execution time is always constant.
         
         - Best Case: O(1)
        """
        if self.current_address is not None:
            # Save the current page to the forward stack
            self.forward_stack.push(self.current_address)

        if not self.back_stack.is_empty():
            # Take the most recent page from the back stack
            self.current_address = self.back_stack.pop()
        else:
            self.current_address = None

    
    def forward_button_pressed(self):
        """
        Time complexity analysis goes here.
        -Worst case: O(1)
         Similar to the back button, this method only involves basic operations of 
         the LinkedStack: checking if forward_stack is empty, pushing the current address onto back_stack, 
         and popping an element from forward_stack. All these operations are O(1) under the linked list implementation, 
         so the total complexity of this method is constant time.

         - Best Case: O(1)
         """
        if not self.forward_stack.is_empty():
            # If you can go forward, 
            # first save the current page into the back stack
            if self.current_address is not None:
                self.back_stack.push(self.current_address)
            self.current_address = self.forward_stack.pop()

    
    def report_address_prefix_count(self, address_prefix):
        """
        Time complexity analysis goes here.
        -Worst case: O(N) 
        If all stored addresses have this string as a prefix, we still need to traverse these elements. 
        According to the problem's assumption that the comparison operation is O(1),
        the total complexity depends on the number of matches.

        Best case: O(1)
        Due to the ordered nature of ArraySortedList, if the list is empty, or if address_prefix is obviously greater than the maximum value,
        it can immediately return 0. This determination does not grow with N.
        
        """
        count = 0
        n = len(self.all_visits)
        prefix_len = len(address_prefix)

        if n == 0 or self.all_visits[n-1] < address_prefix:
            return 0
     
        for i in range(n):
            visit = self.all_visits[i]
            # Use string slicing to check the prefix, 
            # taking the first len(address_prefix) characters of the visit string for comparison
            if visit[:len(address_prefix)] == address_prefix:
                count += 1
            # Once the current address is greater than the prefix and does not match,
            #  it is impossible to match later as well.
            elif visit > address_prefix:
                break
        
        return count


if __name__ == "__main__":
    nav = NavigationManager()
    nav.go_to("google.com")
    nav.go_to("github.com")
    nav.go_to("monash.edu")
    print(nav.get_current_address())  # monash.edu
    nav.back_button_pressed()
    print(nav.get_current_address())  # github.com
    nav.forward_button_pressed()
    print(nav.get_current_address())  # monash.edu

    # Assertions are a great way of testing your code without checking the print outputs.
    assert nav.get_current_address() == "monash.edu"

    # Continue testing your code...
    nav.go_to("google.com/search")
    nav.go_to("google.com/maps")
    
    # Count the number of visits starting with 'google.com'
    google_count = nav.report_address_prefix_count("google.com")
    print(f"Google prefix count: {google_count}") # 3 (google.com, google.com/search, google.com/maps)
    assert google_count == 3

    # Count non-existent prefixes
    none_count = nav.report_address_prefix_count("bing.com")
    print(f"Bing prefix count: {none_count}") 
    assert none_count == 0