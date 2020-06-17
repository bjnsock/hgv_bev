# hgv_bev
This is a simple model to estimate the CO2 savings and cost of operating a HGV battery electric vehicle. The purpose is to see how feasible such a thing would be given available information.

This is based on the figures announced by Tesla for their forth coming Semi, which have still to be confirmed.

It assumes a 1 million mile life time for the BEV rig with a 500 mile range and compares it against an equivalant ICE diesel rig over the same distance.

Only the carbon cost of the following have been factored in, 
   - to initially make the battery in the BEV,
   - the emissions from the electricity needed to recharge the BEV,
   - the tailpipe emissions for the ICE rig,
   - the 'well to tank' emissions for creating the fuel for the ICE rig.
   
All other carbon costs in the manfacture and maintenance of either vehicle have not been factored in.

The sources for all figures are referenced via links in the comments. 

The main figure that has yet to be verified is the efficiency of the BEV, I've taken a low value to be the orginally stated 1.8kWh per mile for a 80,000lb rig, I've also added in a high figure that is twice that, assuming real world figires are somewhat out.

I have also put a low and high estimate in for the CO2 cost to create the batteries, both sourced from the study referenced in the comments.

The energy generation mix,  the price of diesel and the price of electricity are UK based figures for June 2020.

Running the model as is gives the following results, showing high and low ranges.
   - battery size 900 <-> 1,800 kWh
   - battery mass 4,348 <-> 8,696 kg
   - CO2 emitted to make battery 54,900 <-> 190,800kg
   - kms that a diesel truck would drive to emit a battery's worth of CO2 34,870 <-> 121,189 km
   - co2 emissions for BEV truck, battery + electricity 564,300 <-> 1,209,600kg
   - diesel only emissions for same distance 2,519,040kg
   - CO2 savings 78 <-> 52%
   - Fuel cost saving 69 <-> 37 %
