import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load and preprocess the data
df = pd.read_csv('cleaned_data_nyjobs.csv')
df['Posting Date'] = pd.to_datetime(df['Posting Date'], errors='coerce')

# Page configurations
st.set_page_config(page_title="NYC Job Postings Dashboard", layout="wide", page_icon=":bar_chart:")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5dc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <style>
    .title {{
        height: 150px;
        background-image: url('https://images.ctfassets.net/1aemqu6a6t65/5rPsNLkgpwvZPSmjhE5ChB/9ee0978b3d792515d59fefab5296b832/wall-street-photo-tagger-yancey-iv-nyc-and-company-02-2?w=1200&h=800&q=75');
        background-size: cover;
        color: #000000;
        line-height: 150px;
        text-align: center;
        font-size: 42px;
    }}
    </style>
    <div class="title">NYC Job Postings Dashboard</div>
    """,
    unsafe_allow_html=True,
)


# Initialize navigation
if 'page' not in st.session_state:
    st.session_state.page = 1
    st.sidebar.header("Global Filters")
# Date range selector as a global filter
start_date, end_date = st.sidebar.date_input("Select Date Range", [df['Posting Date'].min(), df['Posting Date'].max()])
df_filtered = df[(df['Posting Date'] >= pd.to_datetime(start_date)) & (df['Posting Date'] <= pd.to_datetime(end_date))]

# Adding Interactive Widgets for filtering
min_salary_filter = st.sidebar.slider('Filter by minimum salary:', int(df['Salary Range From'].min()), int(df['Salary Range From'].max()), int(df['Salary Range From'].min()))
df_filtered = df_filtered[df_filtered['Salary Range From'] >= min_salary_filter]

selected_job_category = st.sidebar.selectbox('Select Job Category:', options=['All'] + list(df_filtered['Job Category'].unique()))
if selected_job_category != 'All':
    df_filtered = df_filtered[df_filtered['Job Category'] == selected_job_category]

# Define functions for each page/section
def page1():
    st.title("Page 1: Overview")
    # Sidebar for global filters
   

    # Visualization 1: Dataset Preview on its own row
    st.subheader('Dataset Preview')
    num_rows = st.slider('Rows to display:', min_value=1, max_value=20, value=5, key='dataset_preview')
    st.dataframe(df_filtered.head(num_rows))

    # Row for visualizations 2 & 3
    cols = st.columns(1)

    with cols[0]:
        # Visualization 3: Salary Range From Distribution
        st.subheader('Salary Range From Distribution')
        salary_bin_size = st.select_slider('Select bin size:', options=[5000, 10000, 20000], key='salary_bin_size')

        # Using Plotly Express to create the histogram with a dynamic bin size and improved aesthetic
        fig_salary = px.histogram(df_filtered, x='Salary Range From', nbins=int(df_filtered['Salary Range From'].max() / salary_bin_size),
                                    title="<b>Salary Range From Distribution</b>",
                                    color_discrete_sequence=['#636EFA'],  # Applying a custom color
                                    template="plotly_white")

        # Customizing layout for better readability and visual appeal
        fig_salary.update_layout(
            xaxis_title="<b>Salary Range From</b>",
            yaxis_title="<b>Count</b>",
            title_font_size=20,
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="DarkSlateBlue"
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            bargap=0.2,  # Gap between bars
        )

        # Enhancing bar appearance
        fig_salary.update_traces(marker=dict(line=dict(width=1,
                                                        color='DarkSlateGrey')),  # Border around bars
                                opacity=0.75)  # Slightly transparent bars for a lighter look

        # Customizing hover data to be more descriptive
        fig_salary.update_traces(hovertemplate='<b>Salary Range From:</b> $%{x}<br><b>Count:</b> %{y}<extra></extra>')

        st.plotly_chart(fig_salary)


def page2():
    st.title("Page 2: Detailed Analysis")
    # Example visualization for Page 2
    # Row for visualizations 4 & 5
    #col4, col5 = st.columns(2)

    #with col4:
        # Visualization 4: Job Category Analysis
    st.subheader("Job Category Analysis")
    job_category_count = df_filtered['Job Category'].value_counts().head(10)
    fig_job_cat = px.bar(job_category_count,
                         title="<b>Top 10 Job Categories</b>",
                         text=job_category_count,
                         color=job_category_count.values,
                         color_continuous_scale=px.colors.sequential.Agsunset,  # Applying a vibrant color scale
                         labels={"value": "Number of Job Postings", "index": "Job Category"})

    # Customizing layout
    fig_job_cat.update_layout(
        xaxis_title="<b>Job Category</b>",
        yaxis_title="<b>Number of Postings</b>",
        title_font_size=22,
        font=dict(
            family="Helvetica, sans-serif",
            size=10,
            color="Navy"
        ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            coloraxis_showscale=False  # Hide color scale bar
    )

    # Enhancing readability
    fig_job_cat.update_traces(texttemplate='%{text}', textposition='outside',
                              marker_line=dict(width=1, color='DarkSlateGrey'))  # Add outlines to bars for definition
    fig_job_cat.update_xaxes(tickangle=45)  # Rotate labels for better readability

    st.plotly_chart(fig_job_cat)


    #with col5:
    # Visualization 5: Full-Time/Part-Time Distribution
    st.subheader("Full-Time/Part-Time Distribution")
    # Replace 'F' and 'P' with 'Full-Time' and 'Part-Time' respectively
    ft_pt_count = df_filtered['Full-Time/Part-Time indicator'].replace({'F': 'Full-Time', 'P': 'Part-Time'}).value_counts()

    # Creating the pie chart with customizations
    fig_ft_pt = px.pie(ft_pt_count,
                        names=ft_pt_count.index,
                        values=ft_pt_count.values,
                        title="<b>Full-Time/Part-Time Distribution</b>",
                        color_discrete_sequence=px.colors.qualitative.Pastel1)  # Using a soft, qualitative color palette for differentiation

    # Customizing the pie chart
    fig_ft_pt.update_traces(textinfo='percent+label', pull=[0.1, 0],  # Slightly 'pull' the largest segment for emphasis
                                marker=dict(line=dict(color='#000000', width=2)))  # Adding a black line around each pie segment for better visual separation
    fig_ft_pt.update_layout(
        title_font_size=22,
        font=dict(
            family="Helvetica, sans-serif",
            size=10,
            color="Navy"
        ),
        legend_title="<b>Employment Type</b>",
        legend=dict(
            orientation="h",  # Horizontal legend for better space utilization
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        showlegend=True
    )

    # Removing the default legend title (if needed)
    fig_ft_pt.update_layout(legend_title_text='')

    st.plotly_chart(fig_ft_pt)
    # Row for visualizations 6 & 7
    #col6, col7 = st.columns(2)

    #with col6:
    # Visualization 6: Career Level Distribution
    st.subheader("Career Level Distribution")
    career_level_count = df_filtered['Career Level'].value_counts().reset_index()
    career_level_count.columns = ['Career Level', 'Count']  # Renaming for clarity

    # Using a horizontal bar chart for better readability of career levels
    fig_career_level = px.bar(career_level_count, y='Career Level', x='Count',
                                orientation='h',
                                title="<b>Career Level Distribution</b>",
                                color='Count',  # Color bars by count for visual distinction
                                color_continuous_scale=px.colors.sequential.Inferno,  # A warm color scale
                                text='Count')  # Show count on each bar for clarity

    # Customizing the layout
    fig_career_level.update_layout(
        xaxis_title="<b>Total Number of Postings</b>",
        yaxis_title=None,  # Removing y-axis label for a cleaner look since the categories are self-explanatory
        title_font_size=22,
        font=dict(
            family="Arial, sans-serif",
            size=8,
            color="Navy"
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        coloraxis_showscale=False,  # Optionally hide the color scale if it feels cluttered
        autosize=True,
        margin=dict(l=0, r=0, t=30, b=0)  # Adjust margins to fit the title properly
    )

    # Enhancing readability and visual appeal
    fig_career_level.update_traces(texttemplate='%{text}', textposition='inside',
                                    marker_line=dict(color='DarkSlateGrey', width=1),
                                    opacity=0.8)  # Slightly transparent bars for a modern look

    # Adjusting the axes for better spacing and readability
    fig_career_level.update_yaxes(categoryorder='total ascending')  # Sort career levels by count

    st.plotly_chart(fig_career_level)

    #with col7:
    # Visualization 7: Top Job Categories by Average Salary
    st.subheader('Top Job Categories by Average Salary')
    avg_salary = df_filtered.groupby('Job Category')['Salary Range From'].mean().nlargest(10).reset_index()
    avg_salary.columns = ['Job Category', 'Average Salary']  # Renaming for clarity

    # Using a horizontal bar chart for better readability
    fig_avg_salary = px.bar(avg_salary, y='Job Category', x='Average Salary',
                            orientation='h',
                            title="<b>Top 10 Job Categories by Average Salary</b>",
                            color='Average Salary',  # Color bars by average salary
                            color_continuous_scale=px.colors.sequential.Viridis,  # A vibrant color scale
                            text='Average Salary')  # Show average salary on each bar for clarity

    # Customizing the layout
    fig_avg_salary.update_layout(
        xaxis_title="<b>Average Salary ($)</b>",
        yaxis_title=None,  # Removing y-axis label for a cleaner look
        title_font_size=22,
        font=dict(
            family="Arial, sans-serif",
            size=8,
            color="Navy"
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        coloraxis_showscale=True,  # Show the color scale for reference
        autosize=True,
        margin=dict(l=0, r=0, t=30, b=0)  # Adjust margins to fit the title properly
    )

    # Enhancing readability and visual appeal
    fig_avg_salary.update_traces(texttemplate='%{text:$,.0f}', textposition='inside',
                                    marker_line=dict(color='DarkSlateGrey', width=1),
                                    opacity=0.8)  # Slightly transparent bars

    # Adjusting the axes for better spacing and readability
    fig_avg_salary.update_yaxes(categoryorder='total ascending')  # Sort job categories by average salary

    st.plotly_chart(fig_avg_salary)
    # Row for visualizations 8 & 9
    #col8, col9 = st.columns(2)
    #with col8:
    # Visualization 8: Distribution of Job Postings Over Time
    st.subheader('Distribution of Job Postings Over Time')
    df_filtered['Year'] = df_filtered['Posting Date'].dt.year
    postings_over_time = df_filtered.groupby('Year').size()

    # Using a line chart with enhanced styling
    fig_time_distribution = px.line(postings_over_time,
                                    title="<b>Number of Job Postings Over Years</b>",
                                    labels={'index': 'Year', 'value': 'Number of Postings'},
                                    color_discrete_sequence=['#FFA07A'])  # Warm color for the line

    # Customizing the layout
    fig_time_distribution.update_layout(
        xaxis_title="<b>Year</b>",
        yaxis_title="<b>Number of Postings</b>",
        title_font_size=22,
        font=dict(
            family="Arial, sans-serif",
            size=10,
            color="Navy"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )


    fig_time_distribution.update_traces(mode='lines+markers',
                                        line=dict(width=3),
                                        marker=dict(size=7, line=dict(width=2, color='DarkSlateGrey')))

    st.plotly_chart(fig_time_distribution)
    #with col9:

    st.subheader('Word Cloud for Job Descriptions')
    wordcloud_text = ' '.join(df_filtered['Job Description'].dropna())

    wordcloud = WordCloud(width=800, height=400,
                            background_color ='white',
                            colormap='viridis',
                            collocations=False).generate(wordcloud_text)

    fig_wordcloud, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    st.pyplot(fig_wordcloud)

    

def page3():
    st.title("Page 3: Additional Insights")
    col10, col11 = st.columns(2)
    with col10:

        st.subheader('Internal or External Job Openings')
        posting_type_count = df_filtered['Posting Type'].value_counts().reset_index()
        posting_type_count.columns = ['Posting Type', 'Count']
        fig_posting_type = px.bar(posting_type_count, x='Posting Type', y='Count',
                                   title='<b>Internal vs. External Job Openings</b>',
                                   color='Count', color_continuous_scale=px.colors.sequential.Viridis)

        fig_posting_type.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title='<b>Posting Type</b>'), yaxis=dict(title='<b>Count</b>'))
        fig_posting_type.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')), opacity=0.8)
        st.plotly_chart(fig_posting_type)
    with col11:

        st.subheader('Most Popular Work Units')
        work_unit_count = df_filtered['Division/Work Unit'].value_counts().reset_index()
        work_unit_count.columns = ['Division/Work Unit', 'Count']

        fig_work_unit_treemap = px.treemap(work_unit_count.head(10), path=['Division/Work Unit'], values='Count',
                                            title='<b>Top 10 Most Popular Work Units</b>',
                                            color='Count', color_continuous_scale='RdYlGn')

        fig_work_unit_treemap.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                        margin=dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(fig_work_unit_treemap)
    
    col12, col13 = st.columns(2)

    # Visualization 10: Average Salary by Career Level
    with col12:
        st.subheader("Average Salary by Career Level")
        avg_salary_career = df_filtered.groupby('Career Level')['Salary Range From'].mean().reset_index()
        fig_avg_salary_career = px.bar(avg_salary_career, x='Career Level', y='Salary Range From',
                                        title="<b>Average Salary by Career Level</b>",
                                        color='Salary Range From', color_continuous_scale='Blues')
        fig_avg_salary_career.update_layout(xaxis_title="<b>Career Level</b>", yaxis_title="<b>Average Salary</b>")
        st.plotly_chart(fig_avg_salary_career)

    # Visualization 11: Number of Positions Available by Job Category
    with col13:
        st.subheader("Number of Positions Available by Job Category")
        positions_job_category = df_filtered['Job Category'].value_counts().reset_index()
        positions_job_category.columns = ['Job Category', 'Number of Positions']
        fig_positions_job_category = px.bar(positions_job_category.head(10), x='Job Category', y='Number of Positions',
                                                title="<b>Top 10 Job Categories by Number of Positions</b>",
                                                color='Number of Positions', color_continuous_scale='Agsunset')
        fig_positions_job_category.update_layout(xaxis_title="<b>Job Category</b>", yaxis_title="<b>Number of Positions</b>")
        st.plotly_chart(fig_positions_job_category)
    col14, col15 = st.columns(2)

    with col14:
        st.subheader("Distribution of Job Postings by Work Location")
        df_filtered['Work Location1'] = df_filtered['Work Location'].apply(lambda x: x.split(',')[0] if pd.notnull(x) else 'Unknown')
        location_counts = df_filtered['Work Location1'].value_counts().head(10)
        fig_location_distribution = px.bar(location_counts, orientation='h', title="<b>Top 10 Work Locations</b>",
                                            color_discrete_sequence=px.colors.qualitative.D3)
        fig_location_distribution.update_layout(xaxis_title="<b>Number of Postings</b>", yaxis_title="<b>Location</b>")
        st.plotly_chart(fig_location_distribution)

    with col15:
        st.subheader("Job Posting Trends by Month")

        # First, ensure 'Posting Date' is in datetime format (it appears you've already done this).
        df_filtered['Month'] = df_filtered['Posting Date'].dt.to_period('M')

        # Now, we aggregate the data by month and count the number of job postings.
        postings_by_month = df_filtered.groupby('Month').size().reset_index(name='Number of Postings')

        # Converting 'Month' back to datetime to plot on a continuous axis
        postings_by_month['Month'] = postings_by_month['Month'].dt.to_timestamp()

        # Creating the plot
        fig_postings_by_month = px.line(postings_by_month, x='Month', y='Number of Postings',
                                        title="<b>Job Posting Trends by Month</b>",
                                        markers=True,  # Adding markers for each data point
                                        line_shape='linear')  # Ensuring the line is linear to accurately represent the time series

        # Customizing the layout
        fig_postings_by_month.update_layout(
            xaxis_title="<b>Month</b>",
            yaxis_title="<b>Number of Postings</b>",
            xaxis=dict(
                tickformat="%b\n%Y"  # Formatting the x-axis labels to show abbreviated month and full year
            ),
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="RebeccaPurple"
            )
        )

        st.plotly_chart(fig_postings_by_month)




# Navigation buttons
col1, col2 = st.columns([1,10])
with col1:
    if st.button("Previous") and st.session_state.page > 1:
        st.session_state.page -= 1
with col2:
    if st.button("Next") and st.session_state.page < 3:
        st.session_state.page += 1

# Display the appropriate page based on navigation state
if st.session_state.page == 1:
    page1()
elif st.session_state.page == 2:
    page2()
elif st.session_state.page == 3:
    page3()
else:
    st.write("There has been an error with the page navigation.")

