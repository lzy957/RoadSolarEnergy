% APPROXSOLARPATH approximate the solar angles with accuracy to about 1 deg
% Created by JY Wong 29.04.2018

function [elev, azim, decl, HRA, TC] = approxSolarPath(...
    year,month,day,hour,mins,lat,lon)
%{
year = 2018;
month = 1;
day = 1;
hour = 14;
mins = 0;
GMTOffset = 10;
lat = -35;
lon = 140;
%}
format long

if abs(rem(lon,15))<= 7.5
    GMTOffset = fix(lon/15);
else
    if lon>0
        GMTOffset = fix(lon/15)+1;
    else
        GMTOffset = fix(lon/15)-1;
    end
end

% Calculate days since 1st Jan
monthDayOffset = [0 31 59 90 120 151 181 212 243 273 304 334];
if mod(year,4) == 0
    for idx = 3:numel(monthDayOffset)
        monthDayOffset(idx) = monthDayOffset(idx) + 1;
    end
end
day = day + monthDayOffset(month);

% Local Standard Time Meridian in degrees
LSTM = 15*GMTOffset;

% Equation of Time (EoT) in minutes
B = 360/365*(day-81);
EoT = 9.87*sind(2*B)-7.53*cosd(B)-1.5*sind(B);

% Time Correction Factor (ToC) in mins
TC = (4*(lon-LSTM) + EoT);

% Local Solar Time (LST) in hours
LT = mins/60 + hour;
LST = LT + TC/60;

% Hour Angle (HRA) in degrees
HRA = 15*(LST-12);

% Declination Angle in degrees
decl = 23.45*sind(360/365*(day-81));

% Elevation Angle in degrees
elev = asind(sind(decl)*sind(lat) + cosd(decl)*cosd(lat)*cosd(HRA));

% Azimuth Angle in degrees
azim = acosd((sind(decl)*cosd(lat) - cosd(decl)*sind(lat)*cosd(HRA))/cosd(elev));

if (HRA < -180) || (HRA > 0 && HRA < 180) 
% instead of only if HRA > 0
% to correct for wrongly set GMTOffset, causing the HRA to go beyond the
% supposed values and cause distortion in the polar plot
    azim = 360 - azim;
end
end