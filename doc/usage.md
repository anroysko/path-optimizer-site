# Usage

## Navigation Bar

The navigation bar, visible on every page, has the options

* log in (Opens the log in page)
* register (Opens the registration page)

if you are not currently logged in, and

* log out

if logged in. By clicking the big "Path Optimizer Site" button, you can return to the index page.

## Index page

On the index-page, there are two spoilers that open forms when clicked.

In the "Make a new map" spoiler, there is a form to make a new map.
You have to specify the name, width and height of the new map. These values may be later changed.

In the "Search for a map" spoiler, you can input the ID of the map you want to search for,
and then click search to search for it. Note that the map you are trying to view might not
exist or be visible to you.

If you are logged in, you can also see two cards, the left one displaying your maps, and the right one displaying maps shared to you.

## Register page
Write in your username and password. You must have a unique username. Passwords are hashed server-side.

## Login page
Login with your username and password here

## View map screen

This page has three tabs:

* Map

* Details

* Share

If you do not have view permission on the particular map, you instead see a large message
"The map doesn't exist, or is private and you do not have permissions to view it."

### Map-tab
The Map-tab is always visible, and displays the map. If you have edit permission, there are three buttons

* Save map

* Optimize

* Clear Paths

And a hex grid. If you do not have edit permission, the three buttons are not visible, and there
is a dark overlay over the hex grid.

In the hex grid, dark grey hexes correspond to cities, and yellow hexes correspond to roads.

You can click on any hex in the grid to switch its state in the cycle empty -> city -> road -> empty.
Clicking "Save Map" saves your changes. "Optimize" adds the minimum number of roads required to
connect all cities. "Clear Paths" clears all paths from the map.

If you edit the grid, but don't save, the page will prompt you about unsaved changes when leaving.

Note that the problem is NP-complete. The algorithm used is parameterized on the number of cities,
in particular, it's running time is `O(3^k n)`, where n is the number of hexes on the map. Therefore
having too many cities can cause the calculation to never finish. About 14 should be the highest feasible amount.

### Details
The Details-tab displays two cards, one displaying the map's properties, and the other allowing you to delete the map.
The delete-card is visible only if you have owner permissions on the map.

If you have edit permissions on the map, the properties-card will appear as a form, where you can edit the values, and then submit.

If you have owner permisions on the map, you can click the "Delete"-button in the second card to permanently delete the map.

### Share-tab
The share tab is only visible if you are the owner of the map.
In the share-tab you can share the map to other registered users, and configure what permissions unregistered users have.
There are three cards

* Users with view permission (but not edit permission)

* Users with edit permission

* Default permissions

In the first card, you can add view permissions to some user. If the user doesn't exist, currently nothing happens. Otherwise,
their permission level is set to view permission. If they previously had edit permission, they lose it. You should see their username
appear in the main body of the card.
To remove view permissions from users, click on the "x" next to their username in the main body

The edit permision card works similarly, except that it modifies whether the user has edit permission (and consequently view permission)
instead of just view permission.

In the default permissions card, you can select what permissions unregistered users have on the map
