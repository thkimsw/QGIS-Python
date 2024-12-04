from qgis.utils import iface
from qgis.core import QgsPointXY

target_point = QgsPointXY(128.706701,36.558550)

# 지도 이동
iface.mapCanvas().setCenter(target_point)
iface.mapCanvas().zoomScale(5000)  # 줌 스케일 설정 (숫자를 변경 가능)