# Folding a Linked LIst 

This is an implementation of the folding of a singly linked list. The idea is that if you start off with a list like 
```
1 -> 2 -> 3 -> 4 -> 5
```
Folding it will return the following list:
```
1 -> 5 -> 2 -> 4 -> 3
```

## Recursion-based solution
It's as if you pivot the list on its midway point, and insert the last item after the first, the second-last after 
the second, etc.

The most efficient solution is recursion based. The recursive function takes as parameter the _parent_ of the node that 
might need moving. It does this because, if the node needs moving then its parents `next` reference will need fixing up.

It calls itself to retrieve the position to move the parameter to, and does the move; it returns the next 
position that a node should be moved to.

## Find the middle, flip the second half, interleave with a loop
The second solution involves finding the middle through a slow pointer / fast point method:
````
node findMiddle(head) {
    slowpointer = head
    fastpointer = head
    while (fastpointer != null) {
        fastpointer =  fastpointer.next
        if (fastpointer != null)
            slowpointer = slowpointer.next
            fastpointer = fastpointer.next
            
        if (fastpointer == null)
            break
    }
    return fastpointer
}
```
