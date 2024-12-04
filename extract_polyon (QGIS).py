from qgis.core import QgsProject

# 현재 활성 레이어 가져오기
layer = QgsProject.instance().mapLayersByName("영역")[0]

# 모든 폴리곤의 좌표를 배열로 가져오기
all_coordinates = []  # 모든 좌표를 저장할 리스트

for feature in layer.getFeatures():
    geom = feature.geometry()  # 폴리곤의 지오메트리 가져오기
    if geom.isMultipart():  # 멀티폴리곤인지 확인
        polygons = geom.asMultiPolygon()
        for polygon in polygons:
            for ring in polygon:
                coordinates = [[point.x(), point.y()] for point in ring]  # 경도(x), 위도(y) 순서로 배열 생성
                all_coordinates.append(coordinates)  # 리스트에 추가
    else:  # 단일 폴리곤 처리
        polygon = geom.asPolygon()
        for ring in polygon:
            coordinates = [[point.x(), point.y()] for point in ring]  # 경도(x), 위도(y) 순서로 배열 생성
            all_coordinates.append(coordinates)  # 리스트에 추가

# 결과 출력
for idx, coords in enumerate(all_coordinates):
    print(f"폴리곤 {idx + 1}의 좌표: {coords}")
