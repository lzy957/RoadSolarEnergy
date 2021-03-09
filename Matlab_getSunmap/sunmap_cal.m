% POLARPLOTSOLARPATH plots the sun path (azimuth and elevation) in a polar plot
% Created by JY Wong 30.04.2018

function [azimLArr, elevLArr, azimP, elevP] = ...
    sunmap_cal(year,month,day,hour,mins,lat,lon)
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
daycount = 1;
hourRange = 0:1:23;
data = ones(365*numel(hourRange),11).*-1;
hourdata = ones(365,5).*-1;
for month=monthRange
    for day = 1:1:daynum(month)
        % Preallocating size to improve performance
        hoursArr = ones(1, 5*numel(hourRange)).*-1;
        hidx=0;
        % evaluate the point on the solar path line
        for hours = hourRange
            idx = 1;
            % Extend range by plus minus 24 
            % To accomodate for the placement of wrongly set GMTOffset
            elevLArr = ones(1, 5).*-1;
            azimLArr = ones(1, 5).*-1;
            for perhours = hours:0.02:hours+0.98
                %display(perhours)
                [elevL, azimL] = calcSolarPath(year,month,day,perhours,0,lat,lon);
                if elevL >= 0 && elevL <= 90
                    elevLArr(idx) = elevL;
                    azimLArr(idx) = azimL;
                    hidx = hidx+1;
                    hoursArr(hidx) = perhours;                    
                    % polarplot(deg2rad(azimL),90-elevL,'x') % Plot individual points
                    % hold on
                    % Spherical Coordinates to Cartesian Coordinates
                    % x=rsin?cos?    y=rsin?sin?    z=rcos?
                    thita = 90 - elevL;
                    r = 163;
                    x = -r*sind(thita)*cosd(azimL+90);
                    y = r*sind(thita)*sind(azimL+90);
                    data(count,1) = month;
                    data(count,2) = day;
                    data(count,3) = hours;
                    data(count,4) = perhours;
                    data(count,5) = elevL;  %90-thita(zenith
                    data(count,6) = azimL;
                    data(count,7) = thita;
                    data(count,8) = azimL + 90; %north
                    data(count,9) = x;  %x_zhijiao
                    data(count,10) = y; % pixel coord y_zhijiao
                    data(count,11) = round(x+r);    %x_img
                    data(count,12) = round(2*r-(y+r));  %y_img
                    idx = idx + 1;
                    
                    count = count+1;
                end
            end    
            elevLArr(elevLArr == -1) = [];
            azimLArr(azimLArr == -1) = [];
            if elevLArr
                azimLArrpp = deg2rad(azimLArr);   %edit
                elevLArrpp = 90 - elevLArr;
                %display(elevLArrpp)
                %display(azimLArrpp)
                polar(azimLArrpp,elevLArrpp)
                hold on
            end
        end
        hoursArr(hoursArr == -1) = [];
        hourdata(daycount,1) = month;
        hourdata(daycount,2) = day;
        hourdata(daycount,3) = hoursArr(1);
        hourdata(daycount,4) = hoursArr(hidx);
        hourdata(daycount,5) = hoursArr(hidx) - hoursArr(1);
        daycount = daycount + 1;
    end
end

%table title
% various={'month','day','hour','time','elev','azimuth','thita','azimuth_plus90_north','x_zhijiao','y_zhijiao','x_img','y_img'};


outpath='/Users/lzy/Documents/MATLAB/'; % !!!!******edit******!!!! ?????????
outpathe='sunmap.csv';
outpathehour = 'hourange.csv';
filepath = strcat(outpath,num2str(lat),'_',num2str(lon),outpathe);
filepath1 = strcat(outpath,num2str(lat),'_',num2str(lon),outpathehour);
csvwrite(filepath,data);
csvwrite(filepath1,hourdata);

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