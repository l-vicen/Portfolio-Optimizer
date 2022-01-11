import streamlit as st

def visualize_feedbacks():
    
    st.title('Feedbacks')
    c1, c2 = st.columns((2, 2))
    c2.header('How to give feedback')
    c2.info('If you want to help us to make the website better, please feel free to fill in this form https://forms.gle/zyt2SvLJek4Quage8')
    
    c1.header('Feedback Analysis')
    sheet_url = 'https://docs.google.com/spreadsheets/d/1fPBrdkXWDQgPfpX5L-PUb3hMFWnSFrj22h1TdyD69qw/export?format=csv&gid=1265255192'
    data = pd.read_csv(sheet_url)

    # Data Cleaning
    data.columns = ['date', 'overwhelmed', 'futureUse', 'clarity', 'description', 'design', 'performance', 'wouldRecommend',
                    '1$', '5$', '10$', 'improvements', 'age', 'experience', 'activity', 'gender']
    data['overwhelmed'].replace({1: 'Definitely not true', 2: 'Not true', 3: 'Dont know', 4: 'True', 5: 'Definitely true'},
                                inplace=True)

    st.markdown('### I was completely overwhelmed with the app and didn\'t know what to do.')
    input = {'Definitely not true': len(data[data['overwhelmed'] == 'Definitely not true']), 'Not true': len(data[data['overwhelmed'] == 'Not true']), 'Dont know': len(data[data['overwhelmed'] == 'Dont know']),
            'True': len(data[data['overwhelmed'] == 'True']), 'Definitely true': len(data[data['overwhelmed'] == 'Definitely true'])}
    keys = list(input.keys())
    values = list(input.values())


    fig=px.bar(data,x=keys,y=values )
    st.plotly_chart(fig)

    st.markdown('---')

    st.markdown('### How differs the take on the overwhelm of the website between different professions or age groups? ')#
    df=pd.crosstab(data["overwhelmed"], data['activity'])
    st.table(df)
    df=pd.crosstab(data["overwhelmed"], data['age'])
    st.table(df)
    st.markdown('---')

    st.markdown('### I could imagine using the app in the future, if I want to buy new shares.')
    input = {'Definitely not true': len(data[data['futureUse'] == 1]), 'Not true': len(data[data['futureUse'] == 2]), 'Dont know': len(data[data['futureUse'] == 3]),
            'True': len(data[data['futureUse'] == 4]), 'Definitely true': len(data[data['futureUse'] == 5])}
    keys = list(input.keys())
    values = list(input.values())

    fig=px.bar(data,x=keys,y=values )
    st.plotly_chart(fig)
    st.markdown('---')

    st.markdown('### I would pay something to use the app.')
    input = {'Definitely not true': len(data[data['1$'] == 1]), 'Not true': len(data[data['1$'] == 2]), 'Dont know': len(data[data['1$'] == 3]),
            'True': len(data[data['1$'] == 4]), 'Definitely true': len(data[data['1$'] == 5])}
    keys = list(input.keys())
    values = list(input.values())

    fig=px.bar(data,x=keys,y=values )
    st.plotly_chart(fig)
    st.markdown('---')

    st.markdown('### Age')
    labels = '<25', '25-40', '40-60', '60+'
    sizes = [len(data[data['age'] == '<25']), len(data[data['age'] == '25-40']), len(data[data['age'] == '40-60']),
            len(data[data['age'] == '60+'])]
    fig=px.pie(data,values=sizes,names=labels)
    st.plotly_chart(fig)

    st.markdown('---')

    st.markdown('### Experience in Finance')
    labels = 'Yes', 'No'
    sizes = [len(data[data['experience'] == 'Yes']), len(data[data['experience'] == 'No'])]
    fig=px.pie(data,values=sizes,names=labels)
    st.plotly_chart(fig)

    st.markdown('---')

    st.markdown('### Current Activity')
    labels = 'Self employed', 'Employed', 'Student', 'Other'
    sizes = [len(data[data['activity'] == 'Self employed']), len(data[data['activity'] == 'Employed']),
            len(data[data['activity'] == 'Student']), len(data[data['activity'] == 'Other'])]
    fig=px.pie(data,values=sizes,names=labels)
    st.plotly_chart(fig)
    st.markdown('---')

    st.markdown('### Gender')
    labels = 'Male', 'Female', 'Diverse'
    sizes = [len(data[data['gender'] == 'Male']), len(data[data['gender'] == 'Female']),
            len(data[data['gender'] == 'Diverse'])]
    fig=px.pie(data,values=sizes,names=labels)
    st.plotly_chart(fig)
    st.markdown('---')


    #st.dataframe(data)
