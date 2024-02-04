import matplotlib.pyplot as plt
from pytrends.request import TrendReq

def fetch_and_plot_google_trends(search_query, time_span, x, y):
    # Initialize pytrends
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Prepare the payload
    pytrends.build_payload([search_query], cat=0, timeframe=time_span, geo='', gprop='')

    # Fetch the interest over time
    interest_over_time_df = pytrends.interest_over_time()

    # Check if the dataframe is empty
    if interest_over_time_df.empty:
        print(f"No data found for the keyword '{search_query}'.")
        return
    else:
        # Plotting
        plt.figure(figsize=(x, y))
        plt.plot(interest_over_time_df.index, interest_over_time_df[search_query], label='Interest over time')
        plt.title(f'Google Trends over time for the keyword "{search_query}"')
        plt.xlabel('Date')
        plt.ylabel('Trend')
        plt.legend()
        plt.grid(True)

        # Save the plot
        filename = f'{search_query.replace(" ", "_")}.png'
        plt.savefig(filename)
        print(f"The chart has been saved as '{filename}'.")