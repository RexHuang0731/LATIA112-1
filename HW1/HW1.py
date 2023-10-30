# HW1

import pandas as pd
import random
import matplotlib.pyplot as plt

plt.rc('font', family='Liberation Sans')

url = '110_school_exchange.csv'
df = pd.read_csv(url, encoding='utf-8') # 讀取資料集檔案
df

# Q1. 110學年度收最多正式修讀學位外國生的前十間學校？
data = df.nlargest(10, '學位生_正式修讀學位外國生')
data['Rank'] = range(1, 11)
result = data[['Rank', '學校名稱', '學位生_正式修讀學位外國生']].to_string(index=False)
print(result)

# Q2. 110學年度收最多非學位外國交換生的前十間學校?
data2 = df.nlargest(10, '非學位生_外國交換生')
data2['Rank'] = range(1, 11)
result2 = data2[['Rank', '學校名稱', '非學位生_外國交換生']].to_string(index=False)
print(result2)

# Q3. 110學年度收最多交換學位生的前十間學校？
sum1 = ['學位生_正式修讀學位外國生', '學位生_僑生(含港澳)', '學位生_正式修讀學位陸生']
df['交換學位生'] = df[sum1].sum(axis=1)
data3 = df.nlargest(10, '交換學位生')
data3['Rank'] = range(1, 11)
result3 = data3[['Rank', '學校名稱', '交換學位生']].to_string(index=False)
print(result3)

# Q4. 110學年度收最多交換非學位生的前十間學校？
sum2 = ['非學位生_外國交換生', '非學位生_外國短期研習及個人選讀', '非學位生_大專附設華語文中心學生',
        '非學位生_大陸研修生', '非學位生_海青班']
df['交換非學位生'] = df[sum2].sum(axis=1)
data4 = df.nlargest(10, '交換非學位生')
data4['Rank'] = range(1, 11)
result4 = data4[['Rank', '學校名稱', '交換非學位生']].to_string(index=False)
print(result4)

# Q5. 110學年度國立大學、私立大學收的交換學位生比較
national_universities = df[df['學校名稱'].str.contains("國立|市立") & df['學校類型'].str.contains("大專校院")]
sum3 = national_universities['交換學位生'].sum()
print("國立的大學的交換學位生總和為:", sum3, '人')

private_universities = df[~df['學校名稱'].str.contains("國立|市立") & df['學校類型'].str.contains("大專校院")]
sum4 = private_universities['交換學位生'].sum()
print("私立的大學的交換學位生總和為:", sum4, '人')

values = [sum3, sum4]

labels = ['exchange degree student at National Universities', 'exchange degree student at Private Universities']

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0) 

plt.figure(figsize=(5, 5))

font = {'size': 12}

plt.subplots_adjust(top=1)

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

plt.title('Exchange degree student at National and Private university comparision', fontsize=15)

plt.axis('equal')

plt.show()

# Q6. 110學年度國立大學、私立大學收的交換非學位生比較
national_universities2 = df[df['學校名稱'].str.contains("國立|市立") & df['學校類型'].str.contains("大專校院")]
sum5 = national_universities2['交換非學位生'].sum()
print("國立的大學的交換非學位生總和為:", sum5, '人')

private_universities2 = df[~df['學校名稱'].str.contains("國立|市立") & df['學校類型'].str.contains("大專校院")]
sum6 = private_universities2['交換非學位生'].sum()
print("私立的大學的交換非學位生總和為:", sum6, '人')

values = [sum5, sum6]

labels = ['non-exchange degree student at National Universities', 'non-exchange degree student at Private Universities']

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0) 

plt.figure(figsize=(5, 5))

font = {'size': 12}

plt.subplots_adjust(top=1)

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

plt.title('Non-Exchange degree student at National and Private university comparision', fontsize=15)

plt.axis('equal')

plt.show()

# Q7. 三大首都交換學位生數量比較
Taipei = ['國立政治大學', '國立臺北教育大學', '國立臺北藝術大學', '國立臺灣大學', '國立臺灣師範大學', '臺北市立大學',
         '國立臺北科技大學', '國立臺北商業大學', '國立臺北護理健康大學', '國立臺灣科技大學', '國立臺灣戲曲學院', '大同大學', 
         '中國科技大學', '中國文化大學', '中華科技大學', '世新大學', '臺北城市科技大學', '東吳大學', '德明財經科技大學',
         '康寧大學','馬偕醫護管理專科學校', '臺北醫學大學', '銘傳大學', '實踐大學', '台灣神學研究學院', '基督教台灣浸會神學院']
Taichung = ['中山醫藥大學', '中國醫藥大學', '亞洲大學', '東海大學', '逢甲大學', '靜宜大學', '中臺科技大學', '弘光科技大學',
            '修平科技大學', '朝陽科技大學', '僑光科技大學', '嶺東科技大學', '國立中興大學', '國立臺中教育大學', 
            '國立臺灣體育運動大學', '國立勤益科技大學', '國立臺中科技大學']
Kaohsiung = ['國立中山大學', '國立高雄大學', '國立高雄師範大學', '國立高雄科技大學', '國立高雄餐旅大學', '高雄市立空中大學',
             '高雄醫學大學', '義守大學', '一貫道天皇學院', '文藻外語大學', '正修科技大學', '東方設計大學', '高苑科技大學', 
             '輔英科技大學', '樹德科技大學', '和春技術學院', '育英醫護管理專科學校', '樹人醫護管理專科學校']

N = df[df['學校名稱'].isin(Taipei)]
M = df[df['學校名稱'].isin(Taichung)]
K = df[df['學校名稱'].isin(Kaohsiung)]
total_sum1 = N['交換學位生'].sum()
total_sum2 = M['交換學位生'].sum()
total_sum3 = K['交換學位生'].sum()

print("台北的大學交換學位生共有:", total_sum1, '人')
print("台中的大學交換學位生共有:", total_sum2, '人')
print("高雄的大學交換學位生共有:", total_sum3, '人')

values = [total_sum1, total_sum2, total_sum3]

labels = ['exchange degree student at Taipei university', 'exchange degree student at Taichung university', 'exchange degree student at Kaohsiung university']

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0) 

plt.figure(figsize=(5, 5))

font = {'size': 12}

plt.subplots_adjust(top=1)

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

plt.title('Exchange degree student at three capitals university comparision', fontsize=15)

plt.axis('equal')

plt.show()

# Q8. 三大首都交換非學位生數量比較

N1 = df[df['學校名稱'].isin(Taipei)]
M1 = df[df['學校名稱'].isin(Taichung)]
K1 = df[df['學校名稱'].isin(Kaohsiung)]
total_sum11 = N1['交換非學位生'].sum()
total_sum22 = M1['交換非學位生'].sum()
total_sum33 = K1['交換非學位生'].sum()

print("台北的大學交換非學位生共有:", total_sum11, '人')
print("台中的大學交換非學位生共有:", total_sum22, '人')
print("高雄的大學交換非學位生共有:", total_sum33, '人')

values = [total_sum11, total_sum22, total_sum33]

labels = ['non-exchange degree student at Taipei university', 'non-exchange degree student at Taichung university', 'non-exchange degree student at Kaohsiung university']

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0) 

plt.figure(figsize=(5, 5))

font = {'size': 12}

plt.subplots_adjust(top=1)

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

plt.title('Non-Exchange degree student at three capitals university comparision', fontsize=15)

plt.axis('equal')

plt.show()

# Q9. 頂大與中字輩大學交換學位生比較
top = ['國立臺灣大學', '國立成功大學', '國立清華大學', '國立陽明交通大學', '國立政治大學']
middle = ['國立中興大學', '國立中央大學', '國立中山大學', '國立中正大學']

T = df[df['學校名稱'].isin(top)]
Ch = df[df['學校名稱'].isin(middle)]
total_sum4 = T['交換學位生'].sum()
total_sum5 = Ch['交換學位生'].sum()

print("頂大的大學交換學位生共有:", total_sum4, '人')
print("中字輩的大學交換學位生共有:", total_sum5, '人')

values = [total_sum4, total_sum5]

labels = ['exchange degree student at Top five university', 'exchange degree student at Middle university']

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0) 

plt.figure(figsize=(5, 5))

font = {'size': 12}

plt.subplots_adjust(top=1)

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

plt.title('Exchange degree student at Top five and Middle university comparision', fontsize=15)

plt.axis('equal')

plt.show()

# Q10. 頂大與中字備大學交換非學位生比較
T1 = df[df['學校名稱'].isin(top)]
Ch1 = df[df['學校名稱'].isin(middle)]
total_sum44 = T1['交換非學位生'].sum()
total_sum55 = Ch1['交換非學位生'].sum()

print("頂大的大學交換非學位生共有:", total_sum44, '人')
print("中字輩的大學交換非學位生共有:", total_sum55, '人')

values = [total_sum44, total_sum55]

labels = ['non-exchange degree student at Top five university', 'enon-xchange degree student at Middle university']

colors = ['lightblue', 'lightgreen']

explode = (0.1, 0) 

font = {'size': 12}

plt.figure(figsize=(5, 5))

plt.subplots_adjust(top=1)

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, textprops=font)

plt.title('Non-Exchange degree student at Top five and Middle university comparision', fontsize=15)

plt.axis('equal')
plt.show()

# Check the fonts
'''
from matplotlib import font_manager
font_set = {f.name for f in font_manager.fontManager.ttflist}
for f in font_set:
    print(f)
'''