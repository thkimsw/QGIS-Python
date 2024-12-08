from qgis.core import (
    QgsProject,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessing
)
from qgis.utils import iface
import os

# 입력 설정
input_layer_names = ["1", "2"]  # 잘라낼 대상 레이어 이름 리스트
polygon_layer_name = "범위"  # 범위를 정의하는 폴리곤 레이어 이름
output_directory = "C:/Users/thkim/OneDrive/Desktop/result/"  # 결과 파일 저장 경로

# QGIS 프로젝트에서 레이어 가져오기
project = QgsProject.instance()
polygon_layer = project.mapLayersByName(polygon_layer_name)[0]  # 범위 폴리곤 레이어

if not polygon_layer:
    print("폴리곤 레이어를 찾을 수 없습니다.")
    exit()

# 처리할 레이어 반복 처리
for layer_name in input_layer_names:
    input_layer = project.mapLayersByName(layer_name)[0]  # 이름으로 대상 레이어 가져오기

    if not input_layer:
        print(f"{layer_name} 레이어를 찾을 수 없습니다. 이름을 확인하세요.")
        continue

    # 임시 파일 경로 설정
    inside_temp_path = os.path.join(output_directory, f"{input_layer.name()}_inside_temp.shp")
    output_path = os.path.join(output_directory, f"{input_layer.name()}_clipped_outside.shp")

    # 1단계: 범위 안쪽 영역 추출 (Intersection)
    print(f"처리 중 (범위 안쪽 데이터 추출): {input_layer.name()}")
    intersection_params = {
        "INPUT": QgsProcessingFeatureSourceDefinition(input_layer.source(), selectedFeaturesOnly=False),
        "OVERLAY": QgsProcessingFeatureSourceDefinition(polygon_layer.source(), selectedFeaturesOnly=False),
        "OUTPUT": inside_temp_path
    }
    intersection_result = processing.run("native:intersection", intersection_params)

    if not intersection_result["OUTPUT"]:
        print(f"{input_layer.name()}의 범위 안쪽 데이터를 추출하는 데 실패했습니다.")
        continue

    # 2단계: 원본 데이터에서 범위 안쪽 영역 제거 (Difference)
    print(f"처리 중 (범위 밖 데이터 추출): {input_layer.name()}")
    difference_params = {
        "INPUT": QgsProcessingFeatureSourceDefinition(input_layer.source(), selectedFeaturesOnly=False),
        "OVERLAY": QgsProcessingFeatureSourceDefinition(intersection_result["OUTPUT"], selectedFeaturesOnly=False),
        "OUTPUT": output_path
    }
    difference_result = processing.run("native:difference", difference_params)

    if difference_result["OUTPUT"]:
        print(f"{input_layer.name()}의 범위 밖 데이터를 성공적으로 잘라냈습니다. 결과 파일: {difference_result['OUTPUT']}")
    else:
        print(f"{input_layer.name()}의 처리에 실패했습니다.")
