# Network 1.0.0 API with complementary SurvMatch 1.0.0 API
![](network_pic.gif)


## Network data structure supporting matchmaking

A network is an efficient data structure to organize 
members that belong to the network. It can consist of disconnected 
sub-networks or a single connected network. From here a number of 
altering methods can be implemented, such as adding and removing members. 
As well as creating a network through matchmaking with raw data from
an external survey.

### How to use built in matchmaking compatibility. 
This is an easy three step process that is based on the assumption that all raw data is given from external surveys.

#### Data needed per survey result to be matched with other survey results:
 - Respondent
 - One or more instance of:
    - Question
    - Answer 
    - Match_value (Value of two surveys matching this specific question)

A possible match is determined in the following manner: If a common question between two different survey results has the same answer a match is found. When that happens the match_value of the question is added to the total score between the two survey results mentioned above. This happens for all questions and a total match score is found. 

#### The three step process is as follows: 

##### 1. SurveyRes
 - Given raw data of survey results as specified above, create an instance of SurveyRes for each survey result i. (Where i is any arbitrary respondent).
    - ```surv_i = SurveyRes(respondent_i)  ```
- Now add question results for each question j in survey results belonging to respondent_i.
    - ```surv_i.add(question_j,answer_j,match_value_j) ```
 - After following the two steps above for all raw data, every raw survey results should be divided into instances of SurveyRes. 

- If something went wrong in the process or a graphical representation is needed for an instance of SurveyRes the following methods can be used: ```add, remove, len, get, clear, display ```
##### 2. MatchMake
- Given survey results of type SurveyRes as created through step 1, create an instance of MatchMake for the matching of k target surveys to a single source survey. 
    - ```match = MatchMake() ```
    - match is now an empty instance of MatchMake
- Create the actual match and choose source survey.
    - ```match.create_match(surv_source,[surv_target_1,..., surv_target_k]) ```
- If a graphical representation is needed for an instance of MatchMake the following methods can be used: ```display``` 

##### 3. Network
- Given a match of type MatchMake as created through step 2, create an instance of Network to create a network consisting of members that answered surveys from step 1. In the network a source member exists, from which a target member is far away if the match is low. 
    - ```matchnet = Network()```
    - matchnet is now an empty instance of Network
- Fill the empty network with members who were matched and represented as an instance of MatchMake as shown in step 2. 
    - ```matchnet.match_fill(match)```
- If something went wrong in the process, a graphical representation is needed or any other data handling is needed for an instance of Network the following methods can be used: ```add, remove, change_member, clear, len, get, clear, match_fill, display, collect ```

## Documentation 
### Type Network
```
def add(self, name, neighbours=None, weight=None):
        """Add single member to network and places it in the right position if it has neighbours.
        Leave second argument empty if none exists.
        Third argument is possible weight of member, leave empty if none."""
```

```
 def remove(self,name):
        """Remove single member from network.
        Very slow, try do avoid. N = len(network), N^N worst case time complexity."""
```

```
 def change_member(self,name,name_ch=None,neighbours_ch=None,weight_ch=None):
        """Change given member 'name' of network. Change name, neighbours or weight."""
```

```
def clear(self):
        """Clears network of all members."""
```

```
def get(self,name):
        """Returns specific member as a list. [name,neighbours,weight]."""
```

```
def len(self):
        """Returns number of members in network."""
```

```
def display(self,source,matched_network=False):
        """Graphical representation of network. Weights displayed as added in network. If parameter 'matched_network' = True, display is adapted to a match_fill network. 
        Weights are then given as percentage of a match corresponding to rules of match_fill. 'matched_network' = False by default. """
```

```
def display(self,source):
        """Graphical representation of network, hierarchal print in terminal."""
```

```
def collect(self, source, distance):
        """Collects and returns a list of all members of network with 'distance' number of steps from member source."""
```



### Type SurveyRes

```
def add(self,question,answer,match_value):
        """Adds result of one question to answer_list in Survey Results."""
```

```
def remove(self,question):
        """Removes result of one question in Survey Results.
        Slow, try do avoid. N = #questions, N worst case time complexity. """
```

```
def len(self):
        """Returns number of question results in survey."""
```

```
def get(self,question):
        """Returns specific question as a list. [question,answer,match_value]."""
```

```
def clear(self):
        """Clears survey of all question results."""
```

```
def display(self):
        """Graphical representation of survey."""
```

### Type MatchMake

```
def create_match(self,source, target_list):
        """Returns a match between a source survey and one or more target surveys.
        Beware, slow! N = #questions, M = #target surveys:  M*N^2 worst case time complexity."""
```

```
def display(self):
        """Graphical representation of match."""
```

## Roadmap
 - The API of this library is frozen.
 - Version numbers adhere to [semantic versioning](https://semver.org/)
 
 The only accepted reason to modify the API of this package is to handle issues 
 that can't be resolved in any other reasonable way.
 
 Koray Amico Kulbay - [GITHUB](https://github.com/kurreman)