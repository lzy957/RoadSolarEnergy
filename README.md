# RoadSolarEnergy
Energy Assessment for Solar Panels Construction for Sustainable City

We propose an assessment system by which the solar energy production and demand of a city can be modeled. This study can promote the solar energy collection and use in urban area. Deep learning techniques like semantic recognition which depend on artificial intelligence (AI) are applied to process multi-source GIS image data including street view images and remote sensing image data.

Our Study based on the foundation of our previous study which published on the Journal of Clean Production -- "Towards feasibility of photovoltaic road for urban traffic-solar energy estimation using street view image" https://www.sciencedirect.com/science/article/pii/S0959652619313538?via%3Dihub.



File ‘getBaidu_Images’ 

Provide the method to get panorama street images and data examples.
Environment: python 3.6


File 'ImageProcessing'  

Provide the methods about image processing including scene parsing and image stitching.
The scene parsing methods is based on Semantic Segmentation on MIT ADE20K dataset in PyTorch: https://github.com/CSAILVision/semantic-segmentation-pytorch.


File ‘Matlab_getSunmap’

Calculate the solar path by given latitude and longitude during every day of one year. the output is the center coordinate of the sun sector of every hour.


File 'Traffic_tomtom'

the traffic data obtained from www.tomtom.com which was applied in our first research.


File 'Traffic_BaiDu'

Acquring Traffic data of chinese cities by Baidu Tilemap. and then the processing of these traffic data.


File 'R_Cal'

Calculation of PV production of each road point with Street View and Traffic coverage.


File 'Data_preProcessing'

the preprocessing of grid data including seleced features and output--PV generation. to getprepared for statistic analysis.


File 'Regression'

the model built to prediction. Also include  some result images of the model.


