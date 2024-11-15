from osgeo import gdal, osr
import numpy as np

# 저장할 TIF 파일 경로
output_tif = 'C:/dem/output_file.tif'  # 결과 파일 저장 경로

# EPSG:4326 좌표 영역 (xmin, xmax, ymin, ymax)
xmin, xmax, ymin, ymax = 128.702522986, 128.703674849, 36.554714377, 36.555630347

# 픽셀 해상도 설정 (WGS 84 기준 약 10m 해상도)
pixel_size = 0.001  # 픽셀 크기 (x 및 y 방향)

# 래스터 크기 계산
x_res = int((xmax - xmin) / pixel_size)
y_res = int((ymax - ymin) / pixel_size)

# GeoTIFF 드라이버 생성
driver = gdal.GetDriverByName('GTiff')

# 빈 래스터 데이터 생성
output_raster = driver.Create(output_tif, x_res, y_res, 1, gdal.GDT_Float32)  # DEM 데이터는 Float32로 생성

# GeoTransform 정의 (좌표계 변환)
geotransform = (xmin, pixel_size, 0, ymax, 0, -pixel_size)
output_raster.SetGeoTransform(geotransform)

# 좌표계 설정 (EPSG:4326 - WGS 84)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)
output_raster.SetProjection(srs.ExportToWkt())

# DEM 데이터 생성 (예: 선형 증가)
dem_data = np.linspace(100, 200, x_res * y_res).reshape(y_res, x_res)  # 100m에서 200m 사이 값 생성

# DEM 데이터를 래스터에 작성
band = output_raster.GetRasterBand(1)
band.WriteArray(dem_data)

# 메타데이터 설정 (선택 사항)
band.SetDescription("Digital Elevation Model")
band.SetNoDataValue(-9999)  # NoData 값 설정

# 저장 후 파일 닫기
output_raster.FlushCache()
output_raster = None

print(f"DEM 데이터가 포함된 GeoTIFF 파일이 생성되었습니다: {output_tif}")
