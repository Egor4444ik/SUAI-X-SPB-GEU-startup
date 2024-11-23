import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('dano_xakaton_filled.csv')

original_data = data.copy()

le_region = LabelEncoder()
le_bundle = LabelEncoder()
le_service = LabelEncoder()
le_sex = LabelEncoder()

data['region'] = le_region.fit_transform(data['region'].astype(str))
data['bundle'] = le_bundle.fit_transform(data['bundle'].astype(str))
data['service'] = le_service.fit_transform(data['service'].astype(str))
data['sex'] = le_sex.fit_transform(data['sex'].astype(str))

def fill_missing_with_model(data, target_column):
    data_known = data[data[target_column].notna()]
    data_unknown = data[data[target_column].isna()]

    if data_unknown.empty:
        print(f"Нет пропусков в {target_column}")
        return data

    X = data_known.drop(['user_id', 'order_date', target_column], axis=1)
    y = data_known[target_column]

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    regressor = RandomForestRegressor()
    regressor.fit(x_train, y_train)

    X_unknown = data_unknown.drop(['user_id', 'order_date', target_column], axis=1)
    predicted_values = regressor.predict(X_unknown)

    data.loc[data[target_column].isna(), target_column] = np.round(predicted_values).astype(int)
    print(f"Пропуски в '{target_column}' заполнены.")
    return data

# Заполнение пропусков
data = fill_missing_with_model(data, 'num_sessions')
data = fill_missing_with_model(data, 'avg_session')

data['region'] = original_data['region']
data['bundle'] = original_data['bundle']
data['service'] = original_data['service']
data['sex'] = original_data['sex']

data.to_csv('dano_xakaton_filled_sessions_original.csv', index=False)