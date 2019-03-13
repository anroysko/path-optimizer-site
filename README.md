# path optimizer site

In the popular game Sid Meier's Civilization V, players settle cities, build roads,
and do a bunch of other stuff not relevant to this project. The game takes place in a hexagonal
grid, and each city or road occupies one hexagonal tile. Connecting cities with roads gives the player
benefits, but since roads cost upkeep, it can be hard to do so while using the minimum amount of
roads possible. If we assume that some roads have already been built and cannot be removed,
it is in fact NP-hard by a reduction very similar to the last one in [this paper](https://www.jstor.org/stable/2100192).

The user can place cities and roads, then have an algorithm connect all cities with minimal number
of roads added. They can also name the map, and share it to others by giving out its ID.

By logging in, the user can log in and save the setup, later loading it, possibly adding or
removing cities and roads. Once a map is unnecessary the user can delete it. This is useful since
the game might last multiple days.

Once logged in, the user can invite other registered users to the map instead of sharing its ID,
and can also decide whether to give them rights to edit it.

Functionality:
* Making a new map
* Placing cities and roads on a map
* Automatically completing road networks with approximate solutions
* Naming maps
* Sharing maps with its ID
* If logged in, saving, editing and deleting saved maps
* If logged in, sharing maps with other registered users
