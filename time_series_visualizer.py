import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
main = pd.read_csv('fcc-forum-pageviews.csv')

main['date'] = pd.to_datetime(main['date'])

df = pd.DataFrame(main['value'])
df.index = main['date']

# Clean data
df_top = df['value'].quantile(0.025)
df_bot = df['value'].quantile(0.975)

df = df[(df['value'] >= df_top) & (df['value'] <= df_bot)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))  # Create a Figure and Axes
    plt.figure(figsize=(15,5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    fig.tight_layout()
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    
    # reshapes DataFrame
    df_bar['year']  = df.index.year
    df_bar['month'] = df.index.month
    df_bar = df_bar.groupby(['year','month'])['value'].mean().unstack()
    
    # Draw bar plot
    fig, ax2 = plt.subplots(figsize=(6,6))
    df_bar.plot(kind='bar', ax=ax2, width=0.8)

    # customize the plot
    ax2.set_xlabel("Years")
    ax2.set_ylabel("Average Page Views")
    ax2.legend(title='Months', labels=[
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
                ])
    
    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Use string format for month names

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], color="lightblue")
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], color='pink', order=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Adjust layout
    fig.tight_layout()

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig