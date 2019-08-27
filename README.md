# img-val-helper

## 개요

### 배경

- 2019년 7월 10일 수요일
- SatrecI GK215O 과제
- KOSC 출장
- L2 산출물 검증 방법 정리를 위해 제작한 도구

### 목적

1개 자료 파일을 받아 /geophysical_data 하위에 존재하는 Variable 개수만큼 다음 정보를 가진 엑셀 파일 생성

- 이미지 자료 미리보기 (matplotlib 이용하여 plot 이미지 생성)
- 이미지 간단한 통계 (min / max / avg / nan, fill_value 픽셀 비율)

## 설계

### 출력 엑셀 파일 구조

가장 첫 번째 시트는 전체 파일에 대한 개요를 기록한다.

이 시트에는 다음과 같은 정보가 들어간다.

- 파일 이름
- 촬영 시간
- 슬롯 정보
- 알고리즘 프로젝트 이름
- 산출물 이름
- /geophysical_data 하위 Variable 개수
- /geophysical_data 하위 Variable 목록

그 후에는 각 Variable 마다 두 개의 시트를 만들고 다음과 같은 정보를 기록한다.

- 첫 번째 시트 : (Variable 이름)\_개요
  - Variable 이름
  - 자료형
  - Shape
  - Fill value
  - 밴드 정보
  - 데이터 통계
    - Average
    - Min
    - Max
    - NaN ratio
  - 데이터 미리보기 이미지
- 두 번째 시트 : (Variable 이름)
  - 데이터 값
