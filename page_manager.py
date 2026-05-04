from data_structures import ArrayR
from data_structures.linked_queue import LinkedQueue
from data_structures.array_list import ArrayList
from data_structures.linked_stack import LinkedStack

class SemiSortedWordIterator:
    def __init__(self, front_stack: LinkedStack, back_queue: LinkedQueue):
        self.front_stack = front_stack
        self.back_queue = back_queue

    def __iter__(self):
        return self

    def __next__(self):
        # First pop the word at the head
        if not self.front_stack.is_empty():
            return self.front_stack.pop()
        # After the stack is empty, pop the elements in the queue in order
        elif not self.back_queue.is_empty():
            return self.back_queue.serve()
        else:
            raise StopIteration
        

class PageManager:
    def __init__(self, original_page: ArrayR):
        """
        Don't change this method.
        Only implement the other functions.
        """
        self.single_page: ArrayR = self.generate_single_page(original_page)
    
    def generate_single_page(self, page):
        """
        - Worst case: O(N), where N is the total number of elements across all pages.
          Reason: 
          1. We use a queue to perform a Breadth-First Search level-order traversal. 
             Every element in the nested structure is checked, enqueued, and dequeued exactly once, which takes O(N) time overall.
          2. Type checking (type(element) == str) takes O(1) time.
          3. Appending strings to the ArrayList takes amortized O(1) time.
          4. Finally, copying the elements from ArrayList to ArrayR takes O(N) time.
          Therefore, the overall time complexity strictly conforms to O(N).

        - Best case: O(N)
          Reason: Even in the most ideal case, the algorithm still has to traverse every element 
          in the entire array to perform type checking, store it in result_list, and eventually copy it to the new ArrayR. 
          Therefore, the execution time in the best case also grows linearly with the total number of elements N, that is, O(N).

        """
        # Collect all the words read in order
        result_list = ArrayList()

        # Queue is used to traverse 'New Tab'
        queue = LinkedQueue()
        queue.append(page)

        while not queue.is_empty():
            # Take out the tab that is currently being read
            current_array = queue.serve()
            
            for i in range(len(current_array)):
                element = current_array[i]
                
                # If it is a string, directly add it to the result list
                if type(element) == str:
                    result_list.append(element)
                # If it is a new link, put it at the end of the queue.
                else:
                    queue.append(element)

        # Return an ArrayR that contains only strings
        total_words = len(result_list)
        final_page = ArrayR(total_words)

        for i in range(total_words):
            final_page[i] = result_list[i]
            
        return final_page


    def semi_sorted_word_iterator(self, page):
        """
        - Worst case: O(N), where N is the total number of words on the flattened page (not counting the time for generate_single_page).
        Reason:
        1. Retrieving or generating single page data takes O(1) time.
        2. We traverse every word in an array of length N, looping N-2 times.
        3. Inside the loop, computing the length and absolute difference is an O(1) operation.
        4. Based on the comparison results, we push it into a LinkedStack (push) or LinkedQueue (append), both of which are strictly O(1) insert operations based on linked lists.
        5. Therefore, the total time to process N words is O(N).
        6. The returned iterator's __next__ call is also O(1) each time.

        - Best case: O(N), where N is the total number of words on the flattened page (not counting the time for generate_single_page).
        """
        # Decide which page to use
        if page is None:
            flat_page = self.single_page
        else:
            flat_page = self.generate_single_page(page)
            
        n = len(flat_page)
        if n == 0:
            return SemiSortedWordIterator(LinkedStack(), LinkedQueue())
            
        # Initialization: process the first two words
        word1 = flat_page[0]
        word2 = flat_page[1]
        
        # Compare the lengths to determine the initial order
        if len(word1) <= len(word2):
            first_word = word1
            last_word = word2
        else:
            first_word = word2
            last_word = word1
            
        # Use a Stack to store the words to be placed at the head, 
        # and a Queue to store the words to be placed at the tail.
        front_stack = LinkedStack()
        back_queue = LinkedQueue()
        
        front_stack.push(first_word)
        back_queue.append(last_word)
        
        # Traverse the remaining words
        for i in range(2, n):
            current_word = flat_page[i]
            
            # Calculate length difference
            diff_front = abs(len(current_word) - len(first_word))
            diff_back = abs(len(current_word) - len(last_word))
            
            if diff_front < diff_back:
                front_stack.push(current_word)
                first_word = current_word 
            else:
                back_queue.append(current_word)
                last_word = current_word  
                
        return SemiSortedWordIterator(front_stack, back_queue)

    
    def is_page_ai(self, pattern: str):
        """
       - Worst case: O(N * K) where N is the total number of words on the flattened page, and K is the number of words in the pattern. 
        Reason: Manually parsing the pattern takes O(K) time. In the worst-case scenario (which occurs when
        there are multiple wildcards and partial matches causing repeated backtracking), the `s_idx` pointer
        might need to backtrack to the saved `s_tmp_idx`. However, because the literal tokens ("I", "am", "AI")
        only appear once and in a fixed order, the actual backtracking is minimal, bounding the complexity securely within O(N * K).

        - Best case: O(K) or O(1)
        Reason: If the pattern matches immediately at the beginning of the page, after splitting the pattern string into a list of words (O(K)),
        the algorithm only needs to perform one comparison sequence of length K to return.
        In addition, If the pattern is fundamentally invalid or finishes matching very early, it breaks out in near O(1) time.
        """
        pattern_words = ArrayList()
        current_word = ""
        
        # Traverse character by character, and consider a word ended when a space is encountered
        for i in range(len(pattern)):
            char = pattern[i]
            if char == " ":
                if current_word != "":
                    pattern_words.append(current_word)
                    current_word = ""
            else:
                current_word += char
                
        # Include the last word as well
        if current_word != "":
            pattern_words.append(current_word)

        k = len(pattern_words)
        n = len(self.single_page)

        if k == 0:
            return n == 0

        # Pointer to single_page
        s_idx = 0 
        # Pointer to pattern_words     
        p_idx = 0      
        # Record the position of the most recent '*' encountered in the pattern
        star_idx = -1  
        # Record the probe position in single_page when '*' is encountered
        s_tmp_idx = -1 

        while s_idx < n:
            # Exact word match
            if p_idx < k and pattern_words[p_idx] != "*" and pattern_words[p_idx] == self.single_page[s_idx]:
                s_idx += 1
                p_idx += 1
            
            # Encounter '*'
            elif p_idx < k and pattern_words[p_idx] == "*":
                star_idx = p_idx       
                p_idx += 1             
                s_tmp_idx = s_idx      
                
            # Match failed, triggering backtracking
            elif star_idx != -1:
                p_idx = star_idx + 1   
                s_tmp_idx += 1         
                s_idx = s_tmp_idx      
                
            # Match failed, and there is no backtracking point
            else:
                return False

        # Handle extra '*' at the end
        while p_idx < k and pattern_words[p_idx] == "*":
            p_idx += 1

        # If the pattern pointer reaches the end, it indicates a complete match
        return p_idx == k


if __name__ == "__main__":
    """
    Write tests for your code here...
    """
    raw_page = [
        "Page", "level", "one",
        "link", [
            "Page", "level", "two", "link", ["Page", "level", "three"],
            "more", "of", "level", "two", "another", "link", ["Last", "page!"],
            "and", "end", "of", "page", "two"
        ],
        "end"
    ]

    def build_array_r(lst):
        arr = ArrayR(len(lst))
        for i in range(len(lst)):
            if type(lst[i]) == list:
                arr[i] = build_array_r(lst[i])
            else:
                arr[i] = lst[i]
        return arr

    test_page = build_array_r(raw_page)

    pm = PageManager(test_page)
    # Get the flattened result and convert it to a normal list for easy printing and comparison
    result_array = pm.single_page
    result_python_list = [result_array[i] for i in range(len(result_array))]
    
    print("The page order after flattening is:")
    print(result_python_list)
    
    expected_result = [
        "Page", "level", "one", "link", "end", "Page", "level", "two", "link", 
        "more", "of", "level", "two", "another", "link", "and", "end", "of", 
        "page", "two", "Page", "level", "three", "Last", "page!"
    ]
    assert result_python_list == expected_result
    print("\nTask 4.1 test passed perfectly")


    # 4.2 Test Code
    test_seq = ["short", "words", "and", "long", "words", "it", "doesn't", "fully", "sort"]
    arr_seq = ArrayR(len(test_seq))
    for i in range(len(test_seq)):
        arr_seq[i] = test_seq[i]
        
    pm.single_page = arr_seq
    
    # Get iterator
    iterator = pm.semi_sorted_word_iterator(None)
    
    result_list = []
    for word in iterator:
        result_list.append(word)
        
    expected_order = ["sort", "fully", "doesn't", "words", "short", "words", "and", "long", "it"]
    print("\nPartial sorting result is: ")
    print(result_list)
    assert result_list == expected_order
    print("Task 4.2 Test perfectly passed!")


  

    # 4.3 Test Code -
    
    def test_ai(page_list, pattern, expected):
        arr = ArrayR(len(page_list))
        for i in range(len(page_list)): arr[i] = page_list[i]
        pm.single_page = arr
        assert pm.is_page_ai(pattern) == expected, f"Failed: Page {page_list} with Pattern '{pattern}' expected {expected}"


    test_pattern = "* * I am * AI"
    test_ai(["I", "am", "AI"], test_pattern, True)
    # Single asterisk test
    test_ai(["I", "hehe", "am", "AI"], "* I * am AI", True) 
    test_ai(["I", "am", "not", "AI"], test_pattern, True)
    test_ai(["No,", "I", "am", "not", "AI"], test_pattern, True)
    test_ai(["I", "BREAK", "am", "AI", "I", "am", "not", "AI"], test_pattern, True)
    

    # No wildcards, must match exactly
    test_ai(["I", "am", "not", "AI"], "I am AI", False) 
    test_ai(["Yes,", "I", "am", "AI"], "I am AI", False)
    # There is no '*' between 'I' and 'am', so there cannot be a word
    test_ai(["I", "hehe", "am", "AI"], test_pattern, False)
    # There should be no words after AI
    test_ai(["No,", "I", "am", "not", "AI", "today"], test_pattern, False) 
    
    print("Task 4.3 Test perfectly passed!")