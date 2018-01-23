import math

class PriorityQueue:
  """Array-based priority queue implementation."""
  def __init__(self):
      """Initially empty priority queue."""
      self.queue = []
      self.min_index = None
  
  def __len__(self):
      # Number of elements in the queue.
      return len(self.queue)
  
  def append(self, key):
      """Inserts an element in the priority queue."""
      if key is None:
          raise ValueError('Cannot insert None in the queue')
      self.queue.append(key)
      self.swapKeys(len(self.queue) - 1)
      self.min_index = None

  def swapKeys(self, index):
      p = self.parent(index)
      while self.queue[p] >= self.queue[index] and index > 0:
        temp = self.queue[p]
        self.queue[p] = self.queue[index]
        self.queue[index] = temp
        index = p
        p = self.parent(index)
  
  def min(self):
      """The smallest element in the queue."""
      if len(self.queue) == 0:
          return None
      self._find_min()
      return self.queue[self.min_index]
  
  def pop(self):
      """Removes the minimum element in the queue.
  
      Returns:
          The value of the removed element.
      """
      temp = self.queue[len(self.queue) - 1]
      self.queue[len(self.queue) - 1] = self.queue[0]
      self.queue[0] = temp
      returnValue = self.queue.pop()
      self.minHeapify(0)
      return returnValue

      
  def left(self, index):
      if index == 0:
          return 2
      return (2 * index) + 1

  def right(self, index):
      if index == 0 :
          return 1
      return (2 * index) + 2

  def parent(self, index):
      if index == 0:
          return 0
      if index == 1:
          return 0
      if index == 2:
          return 0
      return int(math.floor((index - 1) / 2))

  def minHeapify(self, index):
      l = self.left(index)
      r = self.right(index)
      i = index
      if(l < len(self.queue) and self.queue[l] < self.queue[i]):
          i = l
      if(r < len(self.queue) and self.queue[r] < self.queue[i]):
          i = r
      if(i != index):
          temp = self.queue[i]
          self.queue[i] = self.queue[index]
          self.queue[index] = temp
          self.minHeapify(i)
          
  def buildMinHeap(self):
    for x in reversed(range(0, int(math.floor(len(self.queue) - 1 / 2)))):
      self.minHeapify(x)
  
  def printHeap(self):
    for i in xrange(0, len(self.queue)):
      print(self.queue[i])
      
  
  def _find_min(self):
      # Computes the index of the minimum element in the queue.
      #
      # This method may crash if called when the queue is empty.
      if self.min_index is not None:
          return
      self.min_index = 0

queue = PriorityQueue()
queue.append(15)
queue.append(13)
queue.append(12)
queue.append(10)
queue.append(8)
queue.append(9)
queue.append(5)
queue.append(4)
#queue.minHeapify(3)
#queue.minHeapify(2)
#queue.minHeapify(1)
#queue.minHeapify(0)
#queue.buildMinHeap()
#print("x is ",x)
queue.printHeap()