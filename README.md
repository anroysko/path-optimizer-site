# path optimizer site

In the popular game Sid Meier's Civilization V, players settle cities, build roads,
and do a bunch of other stuff not relevant to this project. The game takes place in a hexagonal
grid, and each city or road occupies one hexagonal tile. Connecting cities with roads gives the player
benefits, but since roads cost upkeep, it can be hard to do so while using the minimum amount of
roads possible. If we assume that some roads have already been built and cannot be removed,
it is in fact NP-hard by a reduction very similar to the last one in [this classic paper](https://www.jstor.org/stable/2100192).

The algorithm used to optimize paths is https://www.jstor.org/stable/3689922. Parameterized on the number of terminals k, its running time is O(3^k n), and it has the same space complexity O(3^k n).


## Functionality:

The user can place cities and roads into a hex grid,
then have an algorithm connect all cities with minimal number of added roads.

An user can also share the map to others by giving out its ID,
or if logged in, they can share the map to specific registered users.

See [User Stories](./doc/user_stories.md) for more functionality.

## Documentation links
[Heroku app](https://infinite-sands-84798.herokuapp.com/)

[User Stories](./doc/user_stories.md)

[Queries](./doc/queries.md)

[Database Diagram](./doc/database_diagram.png)

[Usage](./doc/usage.md)

[Installation](./doc/installation.md)

[Future Development](./doc/future_development.md)

## Test account credentials (in heroku)
* username - password
* user2 - pass2
