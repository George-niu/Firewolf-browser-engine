from data_structures.linked_queue import LinkedQueue
from data_structures.array_list import ArrayList
from data_structures.array_sorted_list import ArraySortedList


PRIORITY_HIGH = 1
PRIORITY_LOW = 0

DOWNLOAD_TIMEOUT_SECONDS = 3
DOWNLOAD_MAX_ATTEMPTS = 3

# Used to store metadata of download tasks
class DownloadTask:
    def __init__(self, identifier, address, submission_time, expiry_time, priority):
        self.identifier = identifier
        self.address = address
        self.submission_time = submission_time
        self.expiry_time = expiry_time
        self.priority = priority
        self.attempts = 0 # Retry Count
        self.last_attempt_time = 0 # The most recent download start time
        self.is_completed = False # Whether Completed
        self.current_delay = None # Record the current delay value corresponding to this task


def get_current_time():
    """
    You may assume the time complexity of this method is always O(1).
    """
    from time import time
    return int(time()) - 1769930097


class DownloadManager:
    def __init__(self):
        # Store a list of all download tasks
        self.all_downloads = ArrayList()
        # Manage new high/low priority requests in the order they are submitted
        self.high_priority_queue = LinkedQueue()
        self.low_priority_queue = LinkedQueue()
        # Managing Tasks That Have Started but May Time Out
        self.active_queue = LinkedQueue()
        # Store all the delay times of downloads that have started
        self.delays = ArraySortedList()

        
    
    def download_requested(self, address, good_for: int, priority: int):
        current_time = get_current_time()
        expiry_time = current_time + good_for

        # Generate a unique numeric identifier
        identifier = len(self.all_downloads)
        # Create a new download task object
        new_task = DownloadTask(identifier, address, current_time, expiry_time, priority)

        self.all_downloads.append(new_task)

        # Add to the corresponding wait queue according to priority
        if priority == PRIORITY_HIGH:
            self.high_priority_queue.append(new_task)
        else:
            self.low_priority_queue.append(new_task)

    def _update_delay_stats(self, task, current_time):

        new_delay = current_time - task.submission_time
        # If it is a retry task, the old delay value needs to be removed first
        if task.current_delay is not None:
            idx = self.delays.index(task.current_delay)
            self.delays.delete_at_index(idx)
        
        # Update the task delay and store it in an ordered list
        task.current_delay = new_delay
        self.delays.add(new_delay)



        
    def get_next_download(self):
        """
        -Best case: O(1). 
        When the first task at the head of the queue is valid (not expired and not completed).
        - Worst case: O(N). 
        N is the total number of requests. When we need to traverse and skip a large number of expired or completed tasks.

        """

        current_time = get_current_time()

        while not self.active_queue.is_empty():
            task = self.active_queue.serve()

            # If the task is completed, discard it directly
            if task.is_completed:
                continue

            # Check if it has timed out
            if(current_time - task.last_attempt_time) >= DOWNLOAD_TIMEOUT_SECONDS:
                # Check retry eligibility: not expired and retry count < 3
                if current_time < task.expiry_time and task.attempts < DOWNLOAD_MAX_ATTEMPTS:
                    self._update_delay_stats(task, current_time)
                    task.attempts += 1
                    task.last_attempt_time = current_time
                    # Rejoin the queue to wait for the next possible timeout
                    self.active_queue.append(task)
                    return (task.identifier, task.address)
                else:
                    continue
            else:
                # Put it back at the head of the queue
                self.active_queue.append(task)
                break

        # High-Priority New Requests
        while not self.high_priority_queue.is_empty():
            task = self.high_priority_queue.serve()
            if not task.is_completed and current_time < task.expiry_time:
                self._update_delay_stats(task, current_time)
                task.attempts += 1
                task.last_attempt_time = current_time
                self.active_queue.append(task)
                return (task.identifier, task.address)
            
        # Low Priority New Request
        while not self.low_priority_queue.is_empty():
            task = self.low_priority_queue.serve()
            if not task.is_completed and current_time < task.expiry_time:
                self._update_delay_stats(task, current_time)
                task.attempts += 1
                task.last_attempt_time = current_time
                self.active_queue.append(task)
                return (task.identifier, task.address)
            
         
         # No downloads available
        return (None, None)   

    
    def download_completed(self, identifier):
        """
        - Worst case: O(1)
        Because the identifier directly corresponds to the index in the ArrayList (all_downloads),
        accessing array elements by index is a constant-time operation. Modifying object properties is also O(1).

        """
        # Use the identifier as an index to directly locate the download task from the global list
        task = self.all_downloads[identifier]
        
        # Mark the task status as completed
        task.is_completed = True

    def get_median_delay(self) -> float:
        n = len(self.delays)
        if n == 0:
            return 0.0 

        mid = n // 2
        if n % 2 == 1:
            # Odd number: take the middle value
            return float(self.delays[mid])
        else:
            # Even number: Take the average of the two middle values
            return (self.delays[mid - 1] + self.delays[mid]) / 2.0


if __name__ == "__main__":
    """
    Write tests for your code here...
    """
    from time import sleep

    dm = DownloadManager()
    
    dm.download_requested("https://example.com/file1", 10, PRIORITY_LOW)
    dm.download_requested("https://example.com/file2", 10, PRIORITY_HIGH)

    # First download should be the high priority one, so a tuple of (id, "https://example.com/file2") is expected
    first_download = dm.get_next_download()
    assert first_download[1] == "https://example.com/file2"

    # If we wait a few seconds without acknowledging the first download as completed, it means it's timed out
    sleep(5)

    # Asking for the next download should give us the same high priority download again
    second_download = dm.get_next_download()
    assert second_download[1] == "https://example.com/file2"
