import random
import matplotlib.pyplot as plt

# 変数宣言
FIRST_POPULATION = 100
MALE_BIRTH_PROB = 0.51
BASE_BIRTH_RATE = 0.15
MALE_DEATH_RISK = 1.2
MORTALITY_RATES = {
    0: 0.005, 10: 0.001, 30: 0.002, 50: 0.005,
    60: 0.01, 70: 0.03, 80: 0.10, 90: 0.20, 100: 0.50 
}

individual_list = []

def Flooring(num):
    temp = 0.5
    for key in sorted(MORTALITY_RATES.keys()):
        if num >= key:
            temp = MORTALITY_RATES[key]
        else:
            break
    return temp

def Initialization(age):
    # 性別決定
    gender = "M" if random.random() <= MALE_BIRTH_PROB else "W"
    
    # 死亡率取得
    death_prob = Flooring(age)
    if gender == "M":
        death_prob *= MALE_DEATH_RISK
    if random.random() >= death_prob:
        individual_list.append([gender, age])

def run_one_year():
    global individual_list
    
    new_babies = []
    survivors = []
    for person in individual_list:
        gender = person[0]
        age = person[1]
        
        # --- A. 今年の死亡判定 ---
        death_prob = Flooring(age)
        if gender == "M":
            death_prob *= MALE_DEATH_RISK
        
        if random.random() < death_prob:
            continue
    
        # 生き残ったので生存者リストに追加
        survivors.append(person)
        
        # --- B. 出産判定 (女性のみ) ---
        if gender == "W" and 18 <= age <= 45:
            if random.random() < BASE_BIRTH_RATE:
                baby_gender = "M" if random.random() <= MALE_BIRTH_PROB else "W"
                baby_death_prob = Flooring(0)
                if baby_gender == "M": 
                    baby_death_prob *= MALE_DEATH_RISK
                
                if random.random() >= baby_death_prob:
                    new_babies.append([baby_gender, 0])
    
    # 生き残った人は1歳年をとる
    for person in survivors:
        person[1] += 1
    
    # 赤ちゃんと合体して更新
    individual_list = survivors + new_babies
    
    # 集計
    sum_m = sum(1 for p in individual_list if p[0] == "M")
    sum_w = sum(1 for p in individual_list if p[0] == "W")
    return sum_m, sum_w

def main_loop():
    # 1. 初期人口生成
    for _ in range(FIRST_POPULATION):
        Initialization(age=random.randint(0, 80))
    
    history_m = []
    history_w = []
    
    print(f"初期人口: {len(individual_list)}人")
    
    # 2. メインループ（何年回すか）
    years = 100
    for year in range(1, years + 1):
        m, w = run_one_year()
        history_m.append(m)
        history_w.append(w)
        print(f"{year}年目: 計{m+w}人 (男:{m} 女:{w})")
    
    plt.figure(figsize=(10, 6))
    plt.plot(history_m, label='Male', color='blue', linestyle='-')
    plt.plot(history_w, label='Female', color='red', linestyle='-')
    plt.title('Population Simulation')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.legend()
    plt.grid(True)
    
    plt.show()

main_loop()
