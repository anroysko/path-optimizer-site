# path optimizer site

In the popular game Sid Meier's Civilization V, players settle cities, build roads,
and do a bunch of other stuff not relevant to this project. The game takes place in a hexagonal
grid, and each city or road occupies one hexagonal tile. Connecting cities with roads gives the player
benefits, but since roads cost upkeep, it can be hard to do so while using the minimum amount of
roads possible. If we assume that some roads have already been built and cannot be removed,
it is in fact NP-hard by a reduction very similar to the last one in [this classic paper](https://www.jstor.org/stable/2100192).

The user can place cities and roads, then have an algorithm connect all cities with minimal number
of roads added. They can also share the map to others by giving out its ID. If logged in, they can
also share the map to specific other registered users.

## Functionality:
* Creating, editing, deleting and saving maps
* Placing cities and roads on a map
* Searching for maps by ID
* Sharing maps with their ID
* Registering and logging in, with server-side encryption of passwords
* When logged in, Viewing maps you've created and maps shared to you
* (TODO) If logged in, sharing maps with specific registered users
* (TODO) Automatically completing road networks with approximate solutions

## Documentation links
These reflect the current state of the project. More detailed documents will be added later.

[Heroku app](https://infinite-sands-84798.herokuapp.com/)

[User Stories](./doc/user_stories.md)

[Database Diagram](./doc/database_diagram.png)

[Usage](./doc/usage.md)

## Test account credentials
* username - password
* user2 - pass2

Map IDs 1-6 are in use. Maps 3 and 4 are by username, maps 5 and 6 by user2.
