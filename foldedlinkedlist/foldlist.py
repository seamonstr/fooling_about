class LinkedList:
    root = None

    def __str__(self):
        def node_to_str(val):
            return str(val)

        ret = ""
        n = self.root
        while n:
            if n != self.root:
                ret += ', '
            ret += f"{n.map(node_to_str)}"
            n = n.next_
        return ret

    def __init__(self, items=None):
        if items:
            this = None
            for i in items:
                if not this:
                    this = ListItem(i)
                    self.root = this
                else:
                    this.next_ = ListItem(i)
                    this = this.next_

    @staticmethod
    def move_node(pre_node, insert_after):
        """
        move pre_node.next_ to be after insert_after in the list; fix up all the next references to keep the list
        integral.
        """
        node_to_move = pre_node.next_
        pre_node.next_ = node_to_move.next_

        tmp = insert_after.next_
        insert_after.next_ = node_to_move
        node_to_move.next_ = tmp

    def fold(self):
        self._fold_recurse(None)

    def _fold_recurse(self, pre_node):
        """
        if pre_node.next_ is in the latter half of the list, move it to the correct
        position in the folded list and return the next node to move a node in front of.
        If pre_node.next_ is in the first half of the list, do nothing and return None.
        """
        if pre_node is None:
            node_to_move = self.root
        else:
            node_to_move = pre_node.next_

        # Did we reach the end of the list in the caller?
        if node_to_move is None:
            return self.root

        insert_after = self._fold_recurse(node_to_move)

        # insert_after is moving forward through the list, while node_to_move moves backwards (as the call stack
        # unwinds) If they're equal, we're at the half-way mark and need to stop folding
        if not insert_after or insert_after == node_to_move:
            return None

        self.move_node(pre_node, insert_after)
        return insert_after.next_.next_

    def node_by_index(self, index):
        """
        Get the 1-based indexth node
        """
        if index == 0:
            return None
        
        node = None
        for i in range(0, index):
            if not node:
                node = self.root
            else:
                node = node.next_
            if node is None:
                break
        return node


class ListItem:
    val = None
    next_ = None

    def __str__(self):
        return str(self.val)

    def map(self, f):
        return f(self.val)

    def __init__(self, val):
        self.val = val

    def set_next(self, next_):
        self.next_ = next_