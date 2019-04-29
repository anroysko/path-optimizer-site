# User Stories
[x] As a user, I want to make a new map
[x] As a user, I want to edit the information of a map
[ ] As a user, I want to delete a map (Implemented, currently has no HTML front)
[x] As a user, I want to edit the hex grid of a map
[x] As a user, I want to be able to clear all roads from the hex grid with a single button press
[ ] As a user, I want to be able to optimize the roads in a certain maps hex grid
[x] As a user, I want to share maps by giving out its URL
[x] As a user, I want to register
[x] As a user, I want to log in
[x} As a logged in user, I want to log out
[x] As a logged in user, I want to see all maps I've created
[x] As a logged in user, I want to share my maps so that only certain users can view / edit them
[x] As a logged in user, When viewing one of my maps, I want to see which users I have shared the map to
[x] As a logged in user, I want to see all maps that have been shared to me

## Related queries
### As a user, I want to make a new map
This query is handled by SQLAlchemy. If you add a map with name "test", width 5, and height 3, The produced query is:
`INSERT INTO map (date_created, date_modified, name, width, height) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)`
With values `('test', 5, 3)`.

Note that creating a new map also creates two new entries in the perm-table, one of which is the default permissions for unregisted users,
and the other of which is the permissions of the maps creator on the map. SQLALchemy handles these, and the produced query is:
`INSERT INTO perm (date_created, date_modified, account_id, map_id, view_perm, edit_perm, owner_perm) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)`
If the maps creators user ID is 2, and the new maps ID is 7, when the values are `(None, 7, 1, 0, 0)` and `(2, 7, 1, 1, 1)` respectively for the two queries.

### As a user, I want to edit the information of a map
This query too is handled by SQLAlchemy. If we modify the map with ID 7, changing its name to "test2", width to 1,
and height to 20, then the produced query is
`UPDATE map SET date_modified=CURRENT_TIMESTAMP, name=?, width=?, height=? WHERE map.id = ?`
With values `('test2', 1, 20, 7)`

### As a user, I want to edit the hex grid of a map
The editing happens client-side. When the user saves the edits, All existing hexes on the map are cleared, and the new hexes are placed to replace the old ones.
Both of these two functions are handled by SQLAlchemy. To delete all existing hexes in the map, the command
`DELETE FROM hex WHERE map_id=?`
is used, with values `(7)` if we are again working with map index 7. The new hexes are added by SQLAlchemy one-by-one with the query
`INSERT INTO hex (date_created, date_modified, x, y, hex_type, map_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)`
with values `(1, 2, 1, 7)` for a city at location `(1, 2)`.

### As a user, I want to be able to clear all roads from the hex grid with a single button press
A purely client-side functionality. As such, there are no related SQL-commands

### As a user, I want to share maps by giving out its URL
A purely client-side functionality.

### As a user, I want to register
Here two commands are executed, one of them by SQLAlchemy. First, we need to check that no user with the given username exists. That is done with the query
`SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.username AS account_username, account._password AS account__password FROM account WHERE account.username = ? LIMIT ? OFFSET ?`
With values `('user', 1, 0)` for a new user with the username 'user'. Then, if the username is unique, the new user is inserted into the table with the command
`INSERT INTO account (date_created, date_modified, username, _password) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)`
with values `('user', pass)`, where pass is the user's encrypted password.

### As a user, I want to log in
This is done with the exact same command as the first one when registering.

### As a user, I want to log out
A purely python functionality.

### As a logged in user, I want to see all maps I've created
This is done with the command
`SELECT Map.* FROM MAP LEFT JOIN PERM ON Perm.map_id = Map.id WHERE (Perm.owner_perm AND Perm.account_id = ?) GROUP BY Map.id HAVING COUNT(Perm.id) > 0")`
with value `(2)` if the current user has account id 2.

### As a logged in user, I want to share my maps so that only certain users can view / edit them
This query either creates or modfies a perm. If SQLAlchemy creates a perm, it does it with the command
`INSERT INTO perm (date_created, date_modified, account_id, map_id, view_perm, edit_perm, owner_perm) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)`
With values `(2, 7, 1, 1, 0)` if you are giving view and edit permissions to user with ID 2, on map with id 7.
If SQLAlchemy modifies a perm, it does it with the command
`UPDATE perm SET date_modified=CURRENT_TIMESTAMP, view_perm=? WHERE perm.id = ?`
With values `(0, 10)` when removing view permissions on perm with ID 10. SQLAlchemy only updates the necessary fields, this query is longer if more fields need to change.

### As a logged in user, When viewing one of my maps, I want to see which users I have shared the map to
This is done by calling the same query twice with different parameters. The query is:
`SELECT Account.* FROM ACCOUNT LEFT JOIN PERM ON Perm.account_id = Account.id WHERE (Perm.view_perm = :i AND Perm.edit_perm = :j AND Perm.owner_perm = :k AND Perm.map_id = :mi) GROUP BY Account.id HAVING COUNT(Perm.id) > 0"`
With values `(1, 0, 0, 7)` and `(1, 1, 0, 7)` respectively for the two calls, for a map with id 7.

### As a logged in user, I want to see all maps that have been shared to me
This is done with the command
`SELECT Map.* FROM MAP LEFT JOIN PERM ON Perm.map_id = Map.id WHERE (Perm.view_perm AND NOT Perm.owner_perm AND Perm.account_id = ?) GROUP BY Map.id HAVING COUNT(Perm.id) > 0")`
With value `(2)` if the current user has account id 2.
