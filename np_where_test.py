#각각 다른 데이터 프레임의 비교할 리스트 배열을 추출해 배열로 이너 조인
#merge를 사용할 경우 ==만 가능하고 범위 조건을 사용할 수 없어서 이 방법을 사용

import numpy as np
import pandas as pd

_dummy_df_1 = pd.DataFrame()
_dummy_df_2 = pd.DataFrame()
    
_dummy_1_start = _dummy_df_1.end.values
_dummy_1_end = _dummy_df_1.end.values
_dummy_2_start = _dummy_df_2.end.values
_dummy_2_end = _dummy_df_2.end.values

#더미 1의 시작과 종료 범위 안에 더미 2의 시작과 종료 범위가 있는 지 탐색해
#밑에 조건이 성립되는 i - _dummy_1의 인덱스와 j = _dummy_2의 인덱스를 뽑아냄
i, j = np.where((_dummy_1_start[:, None] <= _dummy_2_end) & (_dummy_1_end[:, None] <= _dummy_2_start))

#위에 조건에 해당되는 _dummy_1과 _dummy_df_2를 merge해 데이터 프레임으로 보여줌
_df = pd.DataFrame(np.column_stack([_dummy_df_1.values[i], _dummy_df_2.values[j]]), columns = _dummy_df_1.columns.append( _dummy_df_2.columns))