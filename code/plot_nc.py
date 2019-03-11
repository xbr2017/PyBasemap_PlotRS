# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2019/3/10 21:22'

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmaps

meteo_file = r'D:\data\ECMWF.nc'
ds = Dataset(meteo_file, mode='r')

# 获取每个变量的值
lons = ds.variables['longitude'][:]
lats = ds.variables['latitude'][:]

# surface_air_pressure
sp = ds.variables['sp'][:]
sp_units = ds.variables['sp'].units
scale_factor = ds.variables['sp'].scale_factor
add_offset = ds.variables['sp'].add_offset
sp = scale_factor * sp + add_offset
# 2 metre temperature
t2m = ds.variables['t2m'][:]
t2m_units = ds.variables['t2m'].units
scale_factor = ds.variables['t2m'].scale_factor
add_offset = ds.variables['t2m'].add_offset
t2m = scale_factor * t2m + add_offset
# Total column ozone
tco3 = ds.variables['tco3'][:]
tco3_units = ds.variables['tco3'].units
scale_factor = ds.variables['tco3'].scale_factor
add_offset = ds.variables['tco3'].add_offset
tco3 = scale_factor * tco3 + add_offset

# 经纬度平均值
lon_0 = lons.mean()
lat_0 = lats.mean()

# 画图大小设置
fig = plt.figure(figsize=(16, 9))
plt.rc('font', size=15, weight='bold')
ax = fig.add_subplot(111)

m = Basemap(lat_0=lat_0, lon_0=lon_0)
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)


# 这里数据时间是UTC 00:00，2018年1月的日平均数据，只展示1月1号的数据
sp_01 = sp[0:1, :, :]
t2m_01 = t2m[0:1, :, :]
tco3_01 = tco3[0:1, :, :]

levels = m.pcolor(xi, yi, np.squeeze(tco3_01), cmap=cmaps.GMT_panoply)

# 添加格网与绘制经纬线
m.drawparallels(np.arange(-90., 91., 20.), labels=[1, 0, 0, 0], fontsize=15)
m.drawmeridians(np.arange(-180., 181., 40.), labels=[0, 0, 0, 1], fontsize=15)

# 添加海岸线,省州边界以及国家行政边界
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# 添加colorbar
cbar = m.colorbar(levels, location='bottom', pad="10%")
cbar.set_label(tco3_units, fontsize=15, weight='bold')

# 添加图的标题
plt.title('Total column ozone')
plt.show()

ds.close()
