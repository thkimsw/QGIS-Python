from qgis.core import (
    QgsProject,
    QgsProcessing
)
import os

# 입력 설정
input_layer_names = ["1", "2", "3", "4"]  # 병합할 대상 레이어 이름 리스트
output_path = "C:/Users/thkim/OneDrive/Desktop/result/merged_layer.shp"  # 결과 파일 저장 경로

# QGIS 프로젝트에서 병합할 레이어 가져오기
project = QgsProject.instance()
input_layers = [project.mapLayersByName(name)[0] for name in input_layer_names if project.mapLayersByName(name)]

# 입력 레이어 유효성 확인
if len(input_layers) < len(input_layer_names):
    print("일부 레이어를 찾을 수 없습니다. 이름을 확인하세요.")
    exit()

# 병합 처리
processing_params = {
    "LAYERS": [layer.source() for layer in input_layers],  # 입력 레이어 경로
    "CRS": input_layers[0].crs().toWkt(),  # 첫 번째 레이어의 CRS 사용
    "OUTPUT": output_path
}

result = processing.run("native:mergevectorlayers", processing_params)

# 결과 확인
if result["OUTPUT"]:
    print(f"레이어를 성공적으로 병합했습니다. 결과 파일: {result['OUTPUT']}")
else:
    print("병합 작업에 실패했습니다.")
