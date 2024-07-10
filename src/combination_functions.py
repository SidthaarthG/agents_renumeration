import numpy as np

def calculate_commission_reward(premium, cities_type):
    if premium <= 0 and cities_type == 'Non Metro':
        return 0
    elif 0 <= premium < 25000 and cities_type == 'Non Metro':
        return 0.15
    elif 25000 <= premium < 50000 and cities_type == 'Non Metro':
        return 0.20
    elif 50000 <= premium < 100000 and cities_type == 'Non Metro':
        return 0.23
    elif 100000 <= premium < 150000 and cities_type == 'Non Metro':
        return 0.25
    elif 150000 <= premium < 200000 and cities_type == 'Non Metro':
        return 0.27
    elif 200000 <= premium < 250000 and cities_type == 'Non Metro':
        return 0.30
    elif 250000 <= premium < 400000 and cities_type == 'Non Metro':
        return 0.35
    elif 400000 <= premium < 625000 and cities_type == 'Non Metro':
        return 0.40
    elif 625000 <= premium < 800000 and cities_type == 'Non Metro':
        return 0.42
    elif 800000 <= premium < 1100000 and cities_type == 'Non Metro':
        return 0.43
    elif premium > 1100000 and cities_type == 'Non Metro':
        return 0.45
    elif premium <= 0 and cities_type == 'Metro':
        return 0
    elif 0 <= premium < 25000 and cities_type == 'Metro':
        return 0.15
    elif 25000 <= premium < 60000 and cities_type == 'Metro':
        return 0.20
    elif 60000 <= premium < 125000 and cities_type == 'Metro':
        return 0.23
    elif 125000 <= premium < 200000 and cities_type == 'Metro':
        return 0.25
    elif 200000 <= premium < 250000 and cities_type == 'Metro':
        return 0.27
    elif 250000 <= premium < 300000 and cities_type == 'Metro':
        return 0.30
    elif 300000 <= premium < 500000 and cities_type == 'Metro':
        return 0.35
    elif 500000 <= premium < 725000 and cities_type == 'Metro':
        return 0.40
    elif 725000 <= premium < 900000 and cities_type == 'Metro':
        return 0.42
    elif 900000 <= premium < 1200000 and cities_type == 'Metro':
        return 0.43
    elif premium > 1200000 and cities_type == 'Metro':
        return 0.45
      
def cash_reward(premium, cities_type):
    if premium < 75000:
        return 0
    elif 75000 <= premium < 100000 and cities_type == 'Non Metro':
        return 4000
    elif 75000 <= premium < 100000 and cities_type == 'Metro':
        return 0
    elif 100000 <= premium < 150000:
        return 7500
    elif 150000 <= premium < 250000:
        return 15000
    elif 250000 <= premium < 350000:
        return 30000
    else:
        return 50000

def portablity_premium_to_rewards(premium):

    premium_ranges = [
        (5001, 10000, 1200),
        (10001, 15000, 1600),
        (15001, 20000, 2500),
        (20001, 25000, 3200),
        (25001, 30000, 4000),
        (30001, 40000, 4500),
        (40001, 50000, 5000),
        (50001, 75000, 7000),
        (75001, 100000, 12000),
        (100001, 200000, 16000),
        (200001, 300000, 32000),
        (300001, float('inf'), 46000)
    ]
    for i in range(len(premium_ranges)):
        if premium_ranges[i][0] <= premium <= premium_ranges[i][1]:
            return premium_ranges[i][2]          
    return None

def calculate_commission_rate(df, commission_to_earn, city_type):
    commission_lower_range, commission_upper_range = commission_to_earn, commission_to_earn + 1000
    total_premium, renewal_premium, fresh_premium, ported_premium, renewal_premium_commission, fresh_premium_commission, ported_premium_commission = 0, 0, 0, 0, 0, 0, 0
    premiums = []
    for i in df.index:
        if df['POLICY_TYPE'][i] == 'Renewal':
            renewal_premium += df['PREMIUM'][i]
            renewal_premium_commission = renewal_premium * 0.15
            total_premium += df['PREMIUM'][i]
            
        if df['POLICY_TYPE'][i] == 'FRESH' and df['CITY_TYPE'][i] == city_type:
            fresh_premium += df['PREMIUM'][i] 
            fresh_premium_commission = fresh_premium * calculate_commission_reward(fresh_premium, df['CITY_TYPE'][i]) + cash_reward(fresh_premium, 
                                            df['CITY_TYPE'][i])
            total_premium += df['PREMIUM'][i]

        if df['POLICY_TYPE'][i] == 'Ported':
            ported_premium += df['PREMIUM'][i] 
            ported_premium_commission = portablity_premium_to_rewards(ported_premium)
            total_premium += df['PREMIUM'][i]

        total_premium_commission = renewal_premium_commission + fresh_premium_commission + ported_premium_commission

        while True:
            if total_premium_commission >= commission_lower_range and total_premium_commission < commission_upper_range:
                 return total_premium
            elif total_premium_commission > commission_upper_range:
               commission_upper_range += 1000
            else:
               break

def combinations(df, commission_to_earn, city, premium_range, seed=None):
   metro_cities = ['MUMBAI', 'DELHI', 'KOLKATA', 'CHENNAI', 'BANGALORE',
                   'HYDERABAD', 'AHMEDABAD', 'PUNE', 'SURAT', 'JAIPUR', 'KANPUR', 'LUCKNOW', 'NAGPUR', 'GHAZIABAD',
                   'INDORE', 'COIMBATORE', 'KOCHI', 'PATNA', 'KOZHIKODE']
   if city in metro_cities:
       city_type = 'Metro'
   else:
       city_type = 'Non Metro'
   premium_to_sell = calculate_commission_rate(df, commission_to_earn, city_type)
   lower_premium_sum = premium_to_sell
   upper_premium_sum = premium_to_sell + 1500
   np.random.seed(seed)
   indices = []
   result = []
   combination_df = df[(df['CITIES'] == city) & (df['PREMIUM_RANGE'] == premium_range)]
   while True:
       index = np.random.choice(combination_df.index, 1, p=combination_df['POLICY_COUNT_WEIGHTS'])[0]
       indices.append(index)
       total_premium = sum(combination_df.loc[indices]['PREMIUM'])
       if lower_premium_sum < total_premium < upper_premium_sum:
           result.append(indices[:])
           indices = []
       if total_premium > upper_premium_sum:
           indices = []
       if len(result) > 3:
           break
   return combination_df, result


