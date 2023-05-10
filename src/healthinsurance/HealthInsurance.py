import pickle
import pandas as pd

class HealthInsurance():
    def __init__(self):
        self.home_path = ''
        self.age_scaler = pickle.load(open( self.home_path + 'src/features/age_scaler.pkl', 'rb'))
        self.annual_premium_scaler = pickle.load(open( self.home_path + 'src/features/annual_premium_scaler.pkl', 'rb'))
        self.ap_per_age_scaler = pickle.load(open( self.home_path + 'src/features/ap_per_age_scaler.pkl', 'rb'))
        self.ap_per_day_scaler = pickle.load(open( self.home_path + 'src/features/ap_per_day_scaler.pkl', 'rb'))
        self.fe_policy_sales_channel_scaler = pickle.load(open( self.home_path + 'src/features/fe_policy_sales_channel.pkl', 'rb'))
        self.prev_ins_per_age_scaler = pickle.load(open( self.home_path + 'src/features/prev_ins_per_age_scaler.pkl', 'rb'))
        self.prev_ins_per_day_scaler = pickle.load(open( self.home_path + 'src/features/prev_ins_per_day_scaler.pkl', 'rb'))
        self.target_encoder_region_code = pickle.load(open( self.home_path + 'src/features/target_encoder_region_code.pkl', 'rb'))
        self.vintage_scaler = pickle.load(open( self.home_path + 'src/features/vintage_scaler.pkl', 'rb'))
        
    def data_cleaning(self, df1):

        
        df1['region_code'] = df1['region_code'].astype('int64')
        
        # policy channel
        df1['policy_sales_channel'] = df1['policy_sales_channel'].astype('int64')
        
        return df1
        
    def feature_engineering(self, df2):
    
        df2['gender'] = df2['gender'].apply(lambda x: 1 if x == 'Male' else 0)
    
#        # Turn vehicle_damage to numeric variable
        df2['vehicle_damage'] = df2['vehicle_damage'].apply(lambda x: 1 if x == 'Yes' else 0)
  
        
#        df2['vehicle_age']  = df2['vehicle_age'].apply(lambda x: 'over_2_year' if x == '> 2 Years' else 'between_1_2_year' if x == '1-2 Year' else 'below_1_year')
        
        # annual premium per day
        df2['ap_per_day'] = df2['annual_premium'] / df2['vintage']

        # annual premium per age
        df2['ap_per_age'] = df2['annual_premium'] / df2['age']


        # previously insured per day
        df2['prev_ins_per_day'] = df2['previously_insured'] / df2['vintage']

        # previously insured per age
        df2['prev_ins_per_age'] = df2['previously_insured'] / df2['age']

        df2['vintage_per_age'] = df2['vintage'] / df2['age']
   
        return df2
        
    def data_preparation(self, df5):
         
        df5['age'] = self.age_scaler.transform(df5[['age']].values)
        
        df5['annual_premium'] = self.annual_premium_scaler.transform(df5[['annual_premium']].values)

        df5['ap_per_age'] = self.ap_per_age_scaler.transform(df5[['ap_per_age']].values)

        df5['ap_per_day'] = self.ap_per_day_scaler.transform(df5[['ap_per_day']].values)

        df5.loc[:, 'policy_sales_channel'] = df5['policy_sales_channel'].map(self.fe_policy_sales_channel_scaler)
        
        df5['prev_ins_per_age'] = self.ap_per_day_scaler.transform(df5[['ap_per_day']].values)
        
        df5['prev_ins_per_day'] = self.prev_ins_per_day_scaler.transform(df5[['prev_ins_per_day']].values)

        df5['vintage'] = self.vintage_scaler.transform(df5[['vintage']].values)

        df5.loc[:, 'region_code'] = df5['region_code'].map(self.target_encoder_region_code)

 #       df5 = pd.get_dummies(df5, prefix='vehicle_age', columns=['vehicle_age'])  

             
        cols_selected = ['ap_per_day', 'vintage', 'ap_per_age', 'annual_premium', 'age', 'region_code', 'vehicle_damage', 'policy_sales_channel', 'previously_insured']
            
        return df5[cols_selected]
    
    def get_prediction(self, model, original_data, test_data):

        test_data = test_data.fillna(0)

        pred = model.predict_proba(test_data)
        

        original_data['prediction'] = pred[:, 1].tolist()

        return original_data.to_json(orient='records')