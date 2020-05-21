# Koray Amico Kulbay, network API

# Package network provides a network data structure supporting matchmaking methods.
#
# A network can be used to structure and place members of network in corresponding order relative to each other.
# This structure can provide efficient methods to correlate the members fitting different criteria.
# An example is a placing order based on matchmaking from external data.
#
# Compared to storing data in a simple array a network provides a mathematical background through graph theory.
# The network is based on an array, where each member has neighbours which are other members in the network.
# What differs this network package from other ones is its built in compatibility with matchmaking of external data.
# By using a three step process any matchmaking problem based on survey results can be converted to a network.
# Where the neighbours of a source member is placed further away from it the worse a match is.
# The process is as follows:
# 1. Create an instance of the SurveyRes class for each respondent (to be member in the network) from the raw data.
# 2. Create an instance of the MatchMake class where a source survey is compared to one or more other target surveys
#   (both source and target survey is instances of SurveyRes).
# 3. By using the match_fill method of network class this MatchMake result of source survey compared to one or more
#   target surveys can be converted to a network, where efficient network methods now can be used.

from queue import Queue
from SurvMatch import MatchMake  # SurveyRes,

class _Node:
    """Creates an instance of a node/member belonging to graph/network"""
    def __init__(self,name,neigh_list=None,weight=None):
        self.alias = name
        # self.id = None # TODO(): create random id's
        self.neighbours = neigh_list
        #self.match = match_value
        self.weight = weight
        self.visited = False
        self.displayed = False
        self.rel_pos = None  # Position relative to other node, will be used in later methods

class Network:
    """A network of members."""
    # Using graph theory based on adjacency list
    def __init__(self):
        self._members = []  # This is a list consisting of _Node elements
        self._size = 0  # Keeps track of #nodes in graph
        self._center = None  # This instance of a specific _Node is used for matchmaking
        self._BFS_collect = None
        self._updated = False  # Methods that alter structure of network changes variable to True

    def add(self, name, neighbours=None, weight=None):
        """Add single member to network and places it in the right position if it has neighbours.
        Leave second argument empty if none exists.
        Third argument is possible weight of member, leave empty if none."""

        if type(neighbours) != list:
            if neighbours:
                raise TypeError("Wrong datatype for neighbours, input needs to be a list.")
        if type(name) == int or type(name) == str or type(name) == float:
             pass
        else:
            raise TypeError("Wrong datatype for name. Only int, float and string accepted.")

        if self._get(name):
            raise NameError("Member already exists!")

        add_member = _Node(name, [], weight)
        self._members.append(add_member)
        self._size += 1
        # Makes sure to add the new member in the neighbours_list of each neighbour
        if neighbours:
            for neigh in neighbours:
                # Check if neighbour is in network first
                node_neigh = self._get(neigh)
                if node_neigh:
                    add_member.neighbours.append(node_neigh)  # neighbour node needs to be added to add_member
                    try:
                        node_neigh.neighbours.append(add_member)  # add_member needs to be added to neighbour node
                        # Possibly double of neigh after recursion
                    except AttributeError:  # Handles the case when neighbour exists, but it doesn't have neighbours
                        node_neigh.neighbours = [add_member]
                elif node_neigh is None:
                    self.add(neigh, [add_member.alias])
        self._updated = True

    def remove(self,name):
        """Remove single member from network.
        Very slow, try do avoid. N = len(network), N^N worst case time complexity."""
        if type(name) == int or type(name) == str or type(name) == float:
            pass
        else:
            raise TypeError("Wrong datatype for name. Only int, float and string accepted.")

        rm_node = self._get(name)
        if rm_node:
            if rm_node.neighbours:
                for neigh in rm_node.neighbours:
                    neigh.neighbours.remove(rm_node)
                    if len(neigh.neighbours) == 0:
                        neigh.neighbours = None
            self._members.remove(rm_node)
            self._size -= 1
        elif rm_node is None:
            raise NameError("No such member exists!")

        self._updated = True

    def change_member(self,name,name_ch=None,neighbours_ch=None,weight_ch=None):
        """Change given member 'name' of network. Change name, neighbours or weight."""
        if type(neighbours_ch) != list:
            if neighbours_ch:
                raise TypeError("Wrong datatype for neighbours change, input needs to be a list.")

        if type(name) == int or type(name) == str or type(name) == float:
            pass
        else:
            raise TypeError("Wrong datatype for name. Only int, float and string accepted.")

        node_to_ch = self._get(name)
        if node_to_ch:
            if name_ch:
                node_to_ch.alias = name_ch
            if weight_ch:
                node_to_ch.weight = weight_ch
            if neighbours_ch:
                if node_to_ch.neighbours:
                    for neigh in node_to_ch.neighbours:
                        # Before doing below we need to remove the node to change from its neighbours
                        neigh.neighbours.remove(node_to_ch)
                        if len(neigh.neighbours) == 0:
                            neigh.neighbours = None
                    # If the the node we want to change has neighbours we need to clear its neighbour list
                    node_to_ch.neighbours.clear()
                else:
                    node_to_ch.neighbours = []

                for neigh_ch in neighbours_ch:
                    node_neigh_ch = self._get(neigh_ch)  # OBS! This is the private get method (_get)!
                    if node_neigh_ch:  # If one of the neighbours we want to change to exists as a node
                        node_to_ch.neighbours.append(node_neigh_ch)
                        if node_neigh_ch.neighbours is None:  #Remember we set it to None above if len is 0
                            node_neigh_ch.neighbours = [node_to_ch]
                        else:
                            node_neigh_ch.neighbours.append(node_to_ch)
                        # Above we re-add the node to change to an old neighbour
                    elif node_neigh_ch is None:
                        self.add(neigh_ch,[name_ch])

        elif node_to_ch is None:
            raise NameError("No such member exists!")

        self._updated = True

    def clear(self):
        """Clears network of all members."""
        self._members = []
        self._size = 0
        self._updated = True
        self._BFS_collect = None
        self._center = None

    def get(self,name):
        """Returns specific member as a list. [name,neighbours,weight]."""
        node = self._get(name)
        if node:
            neighbours_names = node.neighbours
            if node.neighbours:
                neighbours_names = []
                for neigh in node.neighbours:
                    neighbours_names.append(neigh.alias)
            return [node.alias, neighbours_names, node.weight]
        elif node is None:
            raise NameError("No such member exists!")

    def _get(self,name):
        """Private method to return actual node instance of member. If it doesn't exist it returns None."""
        for node in self._members:
            if node.alias == name:
                return node

    def len(self):
        """Returns number of members in network."""
        return self._size

    def match_fill(self,MatchMake_inst):
        """Creates a network based on the results from the MatchMake object given as input."""
        if type(MatchMake_inst) is not MatchMake:
            raise TypeError("Wrong datatype: MatchMake_inst has to be of custom type MatchMake!")

        res_dict = {}
        for match in MatchMake_inst._score_list:
            try:
                res_dict[match.match_score].append(match.match_target)
                
            except KeyError:
                res_dict[match.match_score] = [match.match_target]
                

        self.add(MatchMake_inst._source)  # add source in network
        parent = [MatchMake_inst._source]
        for score in sorted(res_dict.keys(),reverse=True):
            for target in res_dict[score]:
                self.add(target,parent,score)
            parent = res_dict[score]

    def display(self,source,matched_network=False):
        """Graphical representation of network. Weights displayed as added in network. If parameter 'matched_network' = True, display is adapted to a match_fill network. 
        Weights are then given as percentage of a match corresponding to rules of match_fill. 'matched_network' = False by default. """
        
        if len(self._members) == 0:   # matchch
            raise NameError("Network is empty, no such source exists!")
        
        handled_members = 0
        
        for k in range(len(self._members)):
            try:
                depth_k = self.collect(source,k)
                counter = len(depth_k)
                for member in depth_k:
                    curr_node = self._get(member)

                    curr_node.displayed = True  # Marks node as displayed
                    handled_members += 1

                    if matched_network is True:
                        if curr_node.weight is not None:
                            weight_perc = str(round((curr_node.weight*100),2))+"%"+" match!"
                        else:
                            weight_perc = " No weight"
                    else:
                        weight_perc = curr_node.weight

                    if counter != 1:
                        print("-" * (len(curr_node.alias + str(weight_perc)) + 5))
                        print("|", " " * (len(curr_node.alias + str(weight_perc))), " |")
                        print("|", curr_node.alias, str(weight_perc), "|")
                        print("|", " " * (len(curr_node.alias + str(weight_perc))), " |")
                        print("-" * (len(curr_node.alias + str(weight_perc)) + 5))

                        print(" "*(len("SHARED DISTANCE FROM SOURCE")//2),"^"," "*(len("SHARED DISTANCE FROM SOURCE")//2))
                        print(" "*(len("SHARED DISTANCE FROM SOURCE")//2),"|"," "*(len("SHARED DISTANCE FROM SOURCE")//2))
                        print("SHARED DISTANCE FROM SOURCE")
                        print(" "*(len("SHARED DISTANCE FROM SOURCE")//2),"|"," "*(len("SHARED DISTANCE FROM SOURCE")//2))
                        print(" "*(len("SHARED DISTANCE FROM SOURCE")//2),"v"," "*(len("SHARED DISTANCE FROM SOURCE")//2))

                        counter -= 1
                    elif counter == 1:
                        print("-" * (len(curr_node.alias + str(weight_perc)) + 5))
                        print("|", " " * (len(curr_node.alias + str(weight_perc))), " |")
                        print("|", curr_node.alias, str(weight_perc), "|")
                        print("|", " " * (len(curr_node.alias + str(weight_perc))), " |")
                        print("-" * (len(curr_node.alias + str(weight_perc)) + 5))

            except ValueError:
                pass
        
        # Handles disconnected graphs
        for member in self._members:
            if member.displayed == False:
                print("!!DISCONNECTED NETWORK!!")
                if matched_network is True:
                    self.display(source=member.alias,matched_network=True)
                else:
                    self.display(source=member.alias)
            if handled_members == len(self._members):
                member.displayed = False

    def collect(self, source, distance):
        """Collects and returns a list of all members of network with 'distance' number of steps from member source."""
        if type(distance) != int or distance < 0:
            raise TypeError("Distance must be a positive integer")

        source_node = self._get(source)
        #Cache
        if self._center == source_node and self._updated is False:
            collector = self._BFS_collect
            try:
                members_dist = []
                for node in collector[distance]:
                    members_dist.append(node.alias)
                return members_dist
            except KeyError:
                raise ValueError("Distance is out of bounds!")
        
        if source_node is None:
            raise NameError("No such member exists!")

        #BFS
        Q = Queue(maxsize=0)
        source_node.visited = True
        source_node.rel_pos = 0
        Q.put(source_node)

        collector = {}
        while Q.qsize() != 0:
            curr_node = Q.get()
            #Operation
            try:
                collector[curr_node.rel_pos].append(curr_node)
            except KeyError:
                collector[curr_node.rel_pos] = [curr_node]

            if curr_node.neighbours is None:
                pass
            else: 
                for neigh in curr_node.neighbours:
                    if neigh.visited is False:
                        neigh.visited = True
                        neigh.rel_pos = curr_node.rel_pos + 1
                        Q.put(neigh)

        #Handles cache
        self._updated = False
        self._center = source_node
        self._BFS_collect = collector

        for node in self._members:  # Remark nodes as unvisited and no relative position for future use
            node.visited = False
            node.rel_pos = None

        return self.collect(source,distance)