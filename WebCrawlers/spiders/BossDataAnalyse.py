import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


def data_analyse(csv, column, title, x_label, y_label):
    # 读取CSV文件
    data = pd.read_csv(csv)
    # 计数，并按升序排列
    value_counts = data[column].value_counts(ascending=True).sort_index(ascending=True)
    # 绘制柱状图
    value_counts.plot(kind='bar')

    # 在每个柱子顶部添加数字
    for i, val in enumerate(value_counts):
        plt.text(i, val, int(val), ha='center', va='bottom')

    # 设置标题
    plt.title(title)
    # 设置X轴标签
    plt.xlabel(x_label)
    # 设置Y轴标签
    plt.ylabel(y_label)
    # 自动调整子图参数，使之填充整个图表区域，边距不足时可能报错，但不会影响程序执行
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    data_analyse('BossData.csv', 'salary', '薪资统计', '范围', '数量')
    data_analyse('BossData.csv', 'experience', '经验统计', '经验', '数量')
    data_analyse('BossData.csv', 'education', '学历统计', '学历', '数量')
