import pandas as pd
from matplotlib import pyplot as plt
def plot():
        df = pd.read_csv('answer.csv')
        plt.rc('font', family='Microsoft JhengHei')
        last_row = df.iloc[-1]
        id = last_row[0]
        # a = 學業
        a = (last_row.iloc[2]+last_row.iloc[6]+last_row.iloc[7]+last_row.iloc[9]+last_row.iloc[10]+last_row.iloc[11])*2/3
        # b = 友情
        b = (last_row.iloc[5]+last_row.iloc[8]+last_row.iloc[9]+last_row.iloc[12]+last_row.iloc[14]+last_row.iloc[17])*2/3
        # c = 愛情
        c = (last_row.iloc[3]+last_row.iloc[8]+last_row.iloc[10]+last_row.iloc[13]+last_row.iloc[14]+last_row.iloc[15])*2/3
        # d = 家庭
        d = (last_row.iloc[7]+last_row.iloc[11]+last_row.iloc[13]+last_row.iloc[15]+last_row.iloc[16]+last_row.iloc[17])*2/3
        # e = 個人
        e = (last_row.iloc[1]+last_row.iloc[4]+last_row.iloc[6]+last_row.iloc[12]+last_row.iloc[13]+last_row.iloc[16])*2/3
        # 總分
        total = a+b+c+d+e
        data = {'Category': ['學業', '友情', '愛情', '家庭', '個人'],
                        'Values': [a, b, c, d, e]}
        df = pd.DataFrame(data)

        labels = [f'{cat}\n{val/total*100:.1f}%' for cat, val in zip(df['Category'], df['Values'])]
        max_value = df['Values'].max()
        max_id = df[df['Values'] == max_value]
        max_category = max_id['Category'].values
        
        # 圓餅圖
        explode = [0.1 if cat in max_category else 0.03 for cat in df['Category']]
        #ax = df.plot.pie(y='Values', labels=df['Category'], autopct='', startangle=90, wedgeprops={'width': 0.35}, legend=False, fontsize=14)
        ax = df.plot.pie(y='Values', labels=labels, autopct='', startangle=90, wedgeprops={'width': 0.35}, legend=False, fontsize=14, labeldistance=1.2,explode = explode)
        ax.set_ylabel('') 
        ax.text(0, 0.08, f'{total:.1f}%', ha='center', va='center', fontsize=25, fontweight='bold', color='black')
        ax.text(0, -0.2, f'壓力指數', ha='center', va='center', fontsize=18, fontweight='bold', color='black')

        plt.axis('equal')  # 保持圆形
        plt.title('壓力來源與壓力指數',fontsize=30, fontweight='bold',y=1.08)
        plt.subplots_adjust(top=0.8)
        plt.savefig(f'pic\{id}.png')
        return total,max_category
plot()