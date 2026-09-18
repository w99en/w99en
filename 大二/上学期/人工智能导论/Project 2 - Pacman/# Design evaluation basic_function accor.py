Recommended_scope = {  
    'cereal': (200, 300),  
    'tubers': (50, 100),  
    'vegetables': (300, 500),  
    'fruits': (200, 350),  
    'meat': (120, 200),  
    'dairy': (300, 500),  
    'nut': (25, 35),  
    'oil': (25, 30),  
    'egg': (1, 1),  
    'aquatic_product': (1, 1)  # 修正了键名，移除了空格  
}  
def Calculate_score(input_data, Recommended_scope):  
    total_score = 0  
    for type, value in input_data.items():  # 修正为 items()  
        MIN, MAX = Recommended_scope[type]  
        if type == "egg":  
            if value >= 1:  
                total_score += 4  
            else:  
                total_score += 3  
        elif type == "aquatic_product":  # 修正了键名，移除了空格  
            if value >= 1:  
                total_score += 4  
            else:  
                total_score += 1 + value  # 这里逻辑可能需要根据实际评价标准调整  
        else:  
            score_per_unit = 11.5  
            if value >= MIN and value <= MAX:  
                total_score += score_per_unit  
            elif value < MIN:  
                total_score += score_per_unit - (MIN - value) / (MAX - MIN) # 修正了分数计算方式  
            else:  
                total_score += score_per_unit - (value - MAX)  / (MAX - MIN)  # 修正了分数计算方式  
    return total_score  
  
input_data1 = {  
    'cereal': 195,  
    'tubers': 0,  
    'vegetables': 150,  
    'fruits': 200,  
    'meat': 145,  
    'dairy': 0,  
    'nut': 0,  
    'oil': 25,  
    'egg': 1,  
    'aquatic_product': 1  # 修正了键名，移除了空格  
}
input_data2={
'cereal':320,
'tubers':0,
'vegetables':430,
'fruits':0,
'meat':215,
'dairy':0,
'nut':60,
'oil':69,
'egg':1,
'aquatic_product':0
}

score1 = Calculate_score(input_data1, Recommended_scope)  
print(score1)
score2 = Calculate_score(input_data2, Recommended_scope)  
print(score2)