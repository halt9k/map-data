# Map data
Idea of this script was to map world population change during last 20 years in leading countries.  

Currently it plots pair of histograms and pair of improved maps.  
It's also easy to modify for any similar table->regional map plotting needs.  

- Used data tables were partially found and fuzzy merged manually, partially downloaded from fluent places like [Our World In Data]( https://ourworldindata.org).  

- Maps use Mercurial projection, one of maps utilizes two layers (=regions). GeoPandas makes both layers and projections very easy to use.

- Info labels were overlapping over EU, which standard SO solution still kept. Used custom lens approach to solve this.

<p float="left">
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/test/output_examples/en/map_world_leaders.png" width="400" align="Center"/>
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/test/output_examples/ru/map_world_leaders_ru.png" width="400" align="Center"/>
</p>  

Other intermediate outputs related to scale choices and to pre-process:

<p float="left"; vertical-align="top">
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/test/output_examples/en/map_world.png" width="250" align="center"/>
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/test/output_examples/en/hist_world.png" width="250" align="top"/>
  <img src="https://raw.githubusercontent.com/halt9k/map-data/master/test/output_examples/en/hist_leaders.png" width="250" align="top"/> 
</p>
</div>
