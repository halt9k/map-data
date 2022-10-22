# map-data
Idea of this script was to visually overview how world population changed during last 20 years in different world regions.  

There was a number of adjustements, currently it plots pair of historgams and pair of improved maps.  
It's also easy to modify for any similar table->map plotting needs.  

- Used data tables were half-prepared manually (including unavoidable fuzzy matching of web sources), half downloaded from fluent places like ![Our World In Data:](https://ourworldindata.org/).  

- This is combined two-layer (two-region) map with Mercurial projection. GeoPandas makes both layers and projections very easy to use.

- Properly placing lables on map, howerer, was trickier. There exists SO solution which was not usable, I tried to test lens approach to prevent from Europe being overlapped.


![MapLead:](https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/map_world_leaders.png)

![HistAll:](https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/hist_world.png)
![HistLead:](https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/hist_leaders.png)
![MapAll:](https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/map_world.png)


