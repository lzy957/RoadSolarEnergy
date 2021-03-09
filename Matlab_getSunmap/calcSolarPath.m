% CALCSOLARPATH contains the algorithm to calculate the solar path --
% change this if other algorithm is used and it will apply to the entire
% program
% Created by JY Wong 12.05.2018

function  [elev, azim, decl, HRA, TC] = calcSolarPath(...
    year,month,day,hour,mins,lat,lon)
    
     [elev, azim, decl, HRA, TC] = approxSolarPath(...
    year,month,day,hour,mins,lat,lon);
end