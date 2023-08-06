import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_math_statistics(folder = r'E:\Python project 2020\amy_study\M_report',width=0.5):
    mypath = folder
    datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # print(onlyfiles)
    t_,wrong_counts,right_counts,in_time_count,out_time_count = [],[],[],[],[]
    for filename in onlyfiles:
        datetime_object = datetime.strptime(filename[:-4], '%Y%m%d_%H%M%S')
        # print(datetime_object)
        t_.append(datetime_object)
        p = pd.read_csv(join(mypath,filename))
        # a = p['correct'].value_counts(normalize=True)
        counts_correct = p['correct'].value_counts()
        if 0 in counts_correct.index:
            wrong_count = counts_correct[0]
        else:
            wrong_count = 0
        wrong_counts.append(wrong_count)

        if 1 in counts_correct.index:
            right_count = counts_correct[1]
        else:
            right_count = 0
        right_counts.append(right_count)
        time_count = p['time']
        count1 = time_count[time_count > 20].count()
        count2 = time_count[time_count <= 20].count()
        in_time_count.append(count2)
        out_time_count.append(count1)

    plt.figure()
    ax1 = plt.subplot(211)

    # ax1 = plt.gca()
    formatter = mdates.DateFormatter("%Y%m%d")
    ax1.xaxis.set_major_formatter(formatter)
    # locator = mdates.DayLocator()
    # ax.xaxis.set_major_locator(locator)

    # delta = t_[-1] - t_[0]
    # print(delta.days)
    # xlabels = [datetime.strftime(t_[-1]-timedelta(days=_), "%Y/%m/%d") for _ in range(int(delta.days/2))]
    # print(len(xlabels))
    # ax.set_xticklabels(xlabels, rotation=45, ha='right')
    # ax1 = plt.subplot(211)
    plt.xticks(rotation = 45)
    plt.bar(t_,wrong_counts, color='#f9bc86', edgecolor='black', width=width)
    plt.bar(t_,right_counts, bottom=wrong_counts, color='#b5ffb9', edgecolor='black',
            width = width)
    plt.legend(['Wrong problem count','Right problem count'],loc=2)
    ax2 = plt.subplot(212)
    formatter = mdates.DateFormatter("%Y%m%d")
    ax2.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation = 45)
    plt.bar(t_,out_time_count, color='#f9bc86', edgecolor='black', width=width)
    plt.bar(t_,in_time_count, bottom=out_time_count, color='#b5ffb9', edgecolor='black',
            width = width)
    plt.legend(['Problems spend >20s','Problems spend <20s'],loc=2)
    plt.tight_layout()
    plt.show()

def main():
    plot_math_statistics()
if __name__ == '__main__':
    main()
