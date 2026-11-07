# INSTRUCTIONS:
# 1. Open a "Terminal" by: View --> Terminal OR just the "Terminal" through the hamburger menu
# 2. run in terminal with: streamlit run streamlit_app.py
# 3. click the "Open in Browser" link that pops up OR click on "Ports" and copy the URL
# 4. Open a Simple Browswer with View --> Command Palette --> Simple Browser: Show
# 5. use the URL from prior steps as intput into this simple browser

# put streamlit code here as needed
import pandas as pd
import streamlit as st
import altair as alt


st.title('IS 445 Homework 6: Streamlit App for Building Inventory Dataset')
st.text("The URL for this app is: https://is445demo-9a728ykaybb45ed3appdx4i.streamlit.app/")
st.text("The URL for its GitHub repo is: https://github.com/madison01108/is445_demo")

source = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"
df =pd.read_csv(source)
df = df.rename(columns={"Agency Name":"agency",
                        "Year Constructed": "year",
                        "Square Footage":"sqft",
                        "Total Floors":"floors"})
df=df[['agency','year','sqft','floors']]
df = df.dropna()
df = df[(df['year'] > 1800) & (df['sqft'] > 0) & (df['floors'] > 0)]
top5 = df['agency'].value_counts().head(5).index.tolist()
df = df[df['agency'].isin(top5)]
scale = alt.Scale(
    domain=top5
)
color = alt.Color(
    'agency:N', scale=scale, title="Agency",
    legend=alt.Legend(orient="bottom", columns=2, labelLimit=400,
     titleFontSize=16, labelFontSize=13),
)
brush = alt.selection_interval(encodings=['x'])
click=alt.selection_point(encodings=['color'])


points =(alt.Chart()
        .mark_point()
        .encode(alt.X("year:Q", title="Year Made", scale=alt.Scale(domain=[1850, 2025])),
                alt.Y("sqft:Q", title="Square Footage", scale=alt.Scale(type="log")),
                color=alt.condition(brush, color, alt.value("lightgray")),
                size=alt.Size("floors:Q", scale=alt.Scale(range=[10, 200]), title="Total Floors for Building"),
            ).properties(width= 800, height =500)
            .add_params(brush)
            .transform_filter(click)
)

bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        x=alt.X('count()', title="Number of Buildings (in selected years)",
                axis=alt.Axis(titleFontSize=15, labelFontSize=13)),
        y=alt.Y('agency:N', title=None, sort="-x",
                axis=alt.Axis(labelLimit=300, labelFontSize=14)),
        color=alt.condition(click, color, alt.value('lightgray')),
        tooltip=['agency:N', 'count()'],
    )
    .transform_filter(brush)
    .properties(width=650, height=350)
    .add_params(click)
)

chart =alt.vconcat(points, bars, data=df, title = "Illinois Buildings Visualizations")
tab1,tab2=st.tabs(["Streamlit theme(default)","Altair native theme"])
with tab1:
    st.altair_chart(chart, theme='streamlit',use_container_width=False)

with tab2:
    st.altair_chart(chart, theme=None,use_container_width=False)
    

st.header("Homework 6: Streamlit Write Up")
st.write("Plot 1: Scatterplot of Year Made and Square Footage")
st.write("This scatterplot reveals when a specific Illinois state building was constructed by year, where each building is also encoded with information of the agency by the dot color (referenced to the legend I created) and the number of total floors indicated by the size of the circle data mark. I chose a circle because both the response and predictive variables are numerical, and we want to manage high density in our data points as a lot of the buildings are constrained to a tight range of years. The response variable that this visualization aims to understand is the total square footage of the building, so we can understand if there is a relationship between square footage and constructed year of the building. I used a log scale so that we can observe potential multiplicative differences between our buildings without worrying about an extremely skewed representaation (specifically towards larger-sized buildings). If I had more time, I would make a dropdown that allows you to filter by different time periods so that you can observe differences by a range of years and compare between these different ranges rather than observing individual data points. ")
st.write("Plot 2: Bar Chart of Agency and Number of Total Buildings")
st.write("This bar chart reveals the quantity of buildings a specific Illinis agency has owned and allows us to observe the numerical differences between the top 5 agencies with most buildings in Illinois from our buildings inventory dataset. I chose to intentially make horizontal bar charts because the agencies all share long names that would be more difficult to make readable in a vertical bar chart. I also sorted this bar chart so we can intuitively read the rankings between our top 5 agencies by how many buildings they owned. So, anyone can assume from my bar chart within the first few seconds that the Department of Natural Resources owns the most state buildings in Illinois. More importantly, these two charts are linked by the interactivity of the bar chart, where clicking onto one specific bar will make other circle marks invisible for buildings that belong to the non-marked bars and only output the circle marks of buildings owned by that agency in its associated legend color. This is the interactive filtering mechanism between the two charts. For changes, I would see if I can filter this down so we can see how different counties have different proportions of buildings owned by an Illinois state agency.") 
st.write("There is no overlap with Homework 5. I chose a different data set too.")
