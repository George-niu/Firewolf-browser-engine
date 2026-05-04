from data_structures.array_list import ArrayList
from data_structures.array_sorted_list import ArraySortedList

class Account:
    def __init__(self, website, username):
        self.website = website
        self.username = username
        # Store all passwords that have been used by this account
        self.password_history = ArrayList()
        # Store all PINs used by this account
        self.pin_history = ArrayList()

    def __eq__(self, other):
        if not isinstance(other, Account):
            return False
        return self.website == other.website and self.username == other.username

    def __lt__(self, other):
        # Used for sorting logic
        if self.website != other.website:
            return self.website < other.website
        return self.username < other.username
    

class PasswordManager:
    def __init__(self, max_passwords_per_account):
        self.max_hist = max_passwords_per_account
        # Use an ordered list to store all accounts
        self.accounts = ArraySortedList()
        


    def set_password(self, website, username, password):
        """
        Time complexity analysis goes here.
        - Worst case: O(N + max_passwords_per_account)
          Reason: N is the total number of accounts. First, locate the account using binary search (O(log N)).
          If the account does not exist, inserting a new account into the ArraySortedList requires shifting elements (O(N)).
          Then, iterate through the account's password history to check for duplicates (O(max_passwords_per_account))
        - Best case: O(log N + M) 
        Reason: When the account already exists, looking up the account requires O(log N). 
        Then it is necessary to traverse the account's existing M old passwords(M <= Max_passwords_per_account ) 
        to ensure the new password is not repeated. Since there is no need to move array elements, this is the fastest scenario for this method.
        """
        temp_acc = Account(website, username)
        actual_acc = None

        try:
            # Try to find an existing account
            idx = self.accounts.index(temp_acc)
            actual_acc = self.accounts[idx]

        except ValueError:
            # Creat and add
            actual_acc = temp_acc
            self.accounts.add(actual_acc)

        # Check if the new password has been used before
        for i in range(len(actual_acc.password_history)):
            if actual_acc.password_history[i] == password:
                raise ValueError("Password has been used before for this account")

        # The latest password
        actual_acc.password_history.append(password)



    def set_pin(self, website, username, pin):
        """
       - Worst case: O(N + P) (N is the total number of accounts, P is the number of historical PINs for the account)
        Reason: First, use binary search to locate the account (O(log N)). If the account does not exist, 
        inserting a new account into the ArraySortedList requires shifting subsequent elements, which takes O(N) time. 
        Then, iterate through the account's pin_history to ensure the new PIN has not been used, which takes O(P) time.
       - Best case: O(log N + P)
         Reason: When the account already exists, searching only takes O(log N), with no need for O(N) expansion.
         Checking the history for duplicates takes O(P). 
        """
        temp_acc = Account(website, username)
        actual_acc = None

        try:
            # Try to find an existing account
            idx = self.accounts.index(temp_acc)
            actual_acc = self.accounts[idx]
        except ValueError:
            # The account does not exist, create and add
            actual_acc = temp_acc
            self.accounts.add(actual_acc)

        # Check if the new PIN has been used before 
        for i in range(len(actual_acc.pin_history)):
            if actual_acc.pin_history[i] == pin:
                raise ValueError("PIN has been used before for this account")

        actual_acc.pin_history.append(pin)


    def get_password(self, website, username):
        """
        Time complexity analysis goes here.
        - Worst case: O(log N)
          Reason: Using binary search to locate the account in an ArraySortedList.
        - Best case: O(1) 
          Reason: If the account to be queried happens to be 
          in the middle position of the ArraySortedList's underlying array, 
          the binary search can find the target in the first comparison, 
          at which point the complexity is constant time.
        """
        temp_acc = Account(website, username)
        try:
            idx = self.accounts.index(temp_acc)
            acc = self.accounts[idx]

            # Return the most recently successfully set password
            hist_len = len(acc.password_history)
            if hist_len == 0:
                raise ValueError("No password set for this account")
            return acc.password_history[hist_len - 1]
        
        except ValueError:
            # Account does not exist
            raise ValueError("Account not found")

    
    def get_pin(self, website, username):
        """
        - Worst case: O(log N)
          Reason: Using binary search in ArraySortedList to locate the account, 
          at worst it requires log N comparisons.
        - Best case: O(1)
          Reason: If the target account happens to be in the middle position of the binary search, 
          it can be found with the first comparison, which means the complexity is constant time.
        """
        temp_acc = Account(website, username)
        try:
            idx = self.accounts.index(temp_acc)
            acc = self.accounts[idx]

            # Return the most recently successfully set PIN
            hist_len = len(acc.pin_history)
            if hist_len == 0:
                raise ValueError("No PIN set for this account")
            return acc.pin_history[hist_len - 1]
        
        except ValueError:
            # Account does not exist
            raise ValueError("Account not found")


if __name__ == "__main__":
    """
    Write tests for your code here...
    """
    pm = PasswordManager(max_passwords_per_account=5)
    
    # Test PIN set and get
    pm.set_pin("monash.edu", "student1", 1234)
    pm.set_pin("monash.edu", "student2", 4321000)
    assert pm.get_pin("monash.edu", "student1") == 1234
    
    # Test PIN update
    pm.set_pin("monash.edu", "student1", 9999)
    assert pm.get_pin("monash.edu", "student1") == 9999
    
    # Test repeat PIN
    try:
        pm.set_pin("monash.edu", "student1", 1234)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("Repeat PIN interception successful!")