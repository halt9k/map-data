# map-data
Idea of this script was to visually overview how world population changed during last 20 years in different world regions.  

There was a number of adjustements, currently it plots pair of historgams and pair of improved maps.  
It's also easy to modify for any similar table->map plotting needs.  

- Used data tables were partially found and fuzzy merged manually, partially downloaded from fluent places like ![Our World In Data:](https://ourworldindata.org/).  

- Maps use Mercurial projection, one of maps urtilizes two layers (=regions). GeoPandas makes both layers and projections very easy to use.

- Properly placing lables on map, howerer, was trickier. There exists SO solution which was not usable, I tried to test lens approach to prevent from Europe being overlapped.

<p float="left">
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/map_world_leaders.png" width="500" align="center"/>
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/ru/map_world_leaders_ru.png" width="500" align="center"/>
</p>  

Other intermediate outputs related to scale choises and to preporcess:

<p float="left"; vertical-align="top">
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/map_world.png" width="300" align="center"/>
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/hist_world.png" width="300" align="top"/>
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/Test/Output_examples/en/hist_leaders.png" width="300" align="top"/> 
</p>
</div>
