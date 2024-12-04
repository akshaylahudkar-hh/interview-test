
# Implementation Details


## Task 3:

I have already implemented the Data Persistence part.

I am storing each node with their parent in the DB in the following structure
```
{
    id: 2,
    label: 'alphanumeric',
    parentId:2
}

parentId is a self referencing foreign key

```
This way I can get all the nodes from the DB and recursively structure them in the 
nested format according to the API contract.
There are other ways in which I could store them for example using Django TreeBeard library in python.

## Task 4:

I have already detailed the routes to get the tree structure according to API contract
and also to add a node
I have also written Unit Tests to test Util methods and routes. 

https://github.com/Hinge-Health-Recruiting/interviews-services_akshaylahudkar/blob/f243caf9c12c13b77aa8aee552629f7ae1ca82ea/javascript/routes/treeRoutes.js#L104
