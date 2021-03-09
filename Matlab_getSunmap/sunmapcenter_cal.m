% POLARPLOTSOLARPATH plots the sun path (azimuth and elevation) in a polar plot
% Created by JY Wong 30.04.2018

function [azimLArr, elevLArr, azimP, elevP] = ...
    sunmapcenter_cal(year,month,day,hour,mins,lat,lon)
format long 

%{
year = 2018;
month = 12;
day = 1;
hour = 12;
mins = 45;
GMTOffset = 10; %Ê±Çø
lat = 40;
lon = 135;
%}

daynum=[31,28,31,30,31,30,31,31,30,31,30,31];
monthRange = 1:1:12;
count = 1;
hourRange = 0:0.5:23;
hourinterval = 0.02;
r = 163;
hourcount = 1/hourinterval;
centerid = ones(12,6).*-1;
for month=monthRange
        % evaluate the point on the solar path line
    for hours = hourRange
        % Preallocating size to improve performance
        hoursArr = ones(1, 5*numel(hourRange)).*-1;
        hidx=1;
        idx = 1;
        elevLArr = ones(1, daynum(month)*hourcount).*-1;
        azimLArr = ones(1, daynum(month)*hourcount).*-1;
        xArr = ones(1,daynum(month)*hourcount).*-1;
        yArr = ones(1,daynum(month)*hourcount).*-1;
        for day = 1:1:daynum(month)
            % Extend range by plus minus 24 
            % To accomodate for the placement of wrongly set GMTOffset
            for perhours = hours:hourinterval:hours+0.5-hourinterval
                %display(perhours)
                [elevL, azimL] = calcSolarPath(year,month,day,perhours,0,lat,lon);
                if elevL >= 0 && elevL <= 90
                    elevLArr(idx) = elevL;
                    azimLArr(idx) = azimL;
                    hoursArr(hidx) = perhours;                    
                    % polarplot(deg2rad(azimL),90-elevL,'x') % Plot individual points
                    % hold on
                    % Spherical Coordinates to Cartesian Coordinates
                    % x=rsin?cos?    y=rsin?sin?    z=rcos?
                    thita = 90 - elevL;
                    x = -r*sind(thita)*cosd(azimL+90);  %x_zhijiao
                    y = r*sind(thita)*sind(azimL+90);   %y_zhijiao
                    xArr(idx) = x+r;    %x_img
                    yArr(idx) = 2*r-(y+r);  %y_img
                    idx = idx + 1;
                    hidx = hidx+1;
                end
            end                
            if elevLArr
                azimLArrpp = deg2rad(azimLArr);   %edit
                elevLArrpp = 90 - elevLArr;
                %display(elevLArrpp)
                %display(azimLArrpp)
                polar(azimLArrpp,elevLArrpp)
                hold on
            end
        end
            elevLArr(elevLArr == -1) = [];
            azimLArr(azimLArr == -1) = [];
            xArr(xArr == -1) = [];
            yArr(yArr == -1) = [];
            if elevLArr
                centerid(count,1) = month;
                centerid(count,2) = hours;
                centerid(count,3) = mean(elevLArr); %elev=90-thita
                centerid(count,4) = mean(azimLArr); %azimuth
                centerid(count,5) = mean(xArr);
                centerid(count,6) = mean(yArr);
                count = count+1;
            end 
    end
end

outpath='/Users/lzy/Documents/MATLAB/'; % !!!!******edit******!!!! ?????????
outpathec='sunmapcenter.csv';
filepath = strcat(outpath,num2str(lat),'_',num2str(lon),outpathec);
csvwrite(filepath,centerid);

%[elevP, azimP] = calcSolarPath(year,month,day,hour,mins,lat,lon);

% Adjustment to be placed in polar plot
% Note: 1) In polarplot, theta is in radians
% 2) "elevation (or altitude) angle is calculated from the horizontal"
% the polar plot we want is zero at the outside (rho) and increasing
% towards the centre, MATLAB polarplot does not have this feature, so we
% cheat by inverting the value (minus 90) and changing the rho labels


%azimPpp = deg2rad(azimP);

%elevPpp = 90 - elevP;

% Polar plot
% figure

title('Solar Path')

%polar(azimPpp,elevPpp,'x')
%rlim([0 90])
hold off


%  pax = gca;
%  pax.ThetaZeroLocation = 'top';
%  pax.ThetaDir = 'clockwise';
%  pax.RTick = [0 10 20 30 40 50 60 70 80 90];
%  pax.RTickLabel = {'90';'';'';'60';'';'';'30';'';'';'0'};

% Cartesian Plot for troubleshooting
% figure
% plot(azimLArr,elevLArr)

%{
% For troubleshootinh
figure
plot(hoursArr,azimLArr)
hold on
plot(hoursArr,elevLArr)
pltax = gca;
pltax.XTick = 0:2:24;
title('Daily variation of the solar angles')
legend('azim','elev')
xlabel('hours')
ylabel('degree')
hold off
%}
end