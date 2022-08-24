import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
## you may have to write the full address of the file to be opened
df = pd.read_csv('fcc-forum-pageviews.csv',
    index_col = 0,
    parse_dates = ['date'])

# Clean data
df = df.loc[(df['value'] <= df['value'].quantile(0.975)) & (df['value'] >= df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (20, 10))
    ax.plot(df.index, df['value'], 'r', linewidth=1)

    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')


    # Save image and return fig (don't change this part)
    ## you may have to change the save location of the png, because not all devices save correctly
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
    df_bar['year'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.strftime('%B')
    df_bar2 = df_bar.groupby(['year', 'Months']).mean()
    df_bar2.reset_index(level = 'Months', inplace = True)
    mth = df_bar2.pivot(columns = 'Months', values = 'value')
    mth = mth[['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']]

    # Draw bar plot
    mth.plot.bar(label=months)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(loc='upper left', title="Months", prop = {'size': 7})
    plt.tight_layout()
    fig = plt.gcf()


    # Save image and return fig (don't change this part)
    ## you may have to change the save location of the png, because not all devices save correctly
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace = True)
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['year'] = [d.year for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box.sort_values(by = ['year', 'date'], ascending = [False, True], inplace = True)
    fig, axes = plt.subplots(1, 2, figsize = (20, 10))
    sns.boxplot(x = 'year', y = 'value', data = df_box, ax = axes[0])
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(x = 'month', y = 'value', data = df_box, ax = axes[1])
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    ## you may have to change the save location of the png, because not all devices save correctly
    fig.savefig('box_plot.png')
    return fig