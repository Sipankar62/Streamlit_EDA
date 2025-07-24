import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- Page setting---

st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title(" One click Data Analysis")


# --- File uploader ---

file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.success("File successfully loaded!")
    st.write("### Preview of Data", df.head())

    # --- Basic Info ---

    st.sidebar.markdown("##  Data Summary")
    if st.sidebar.checkbox("Show Data Info"):
        st.write("### Data Info")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

    if st.sidebar.checkbox("Show Shape"):
        st.write(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns")


    # --- Missing Values ---

    if st.sidebar.checkbox("Missing Value Analysis"):
        st.write("### Missing Value Count")
        st.write(df.isnull().sum())


    # --- Column Types ---

    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    st.sidebar.markdown("## Categorical & Numerical Analysis")
    
    # --- Categorical Column Analysis ---


    selected_cat_col = st.sidebar.selectbox("Select Categorical Column", categorical_cols)
    if selected_cat_col:
        st.markdown(f"###  Categorical Analysis: {selected_cat_col.capitalize()}")
        fig1,(ax1,ax2) = plt.subplots(1,2,figsize=(14,4))
        colors = ['Red','Blue','green','skyblue','yellow','brown','orange']
        keys=df[selected_cat_col].value_counts().keys()
        values=df[selected_cat_col].value_counts().values
        ax1.set_title("Bar Chart")
        ax1.set_xlabel(f"{selected_cat_col.capitalize()}")
        ax1.set_ylabel("Count")
        ax1.bar(keys,values,color=colors)
        for i, (i,j) in enumerate(zip(keys, values)):
            ax1.text(i, j + 0.5, str(j), ha='center', va='bottom', fontsize=10)
        ax2.set_title("Pie Chart")
        ax2.pie(values,labels=keys,shadow=True,  autopct="%0.2f%%")
        plt.tight_layout()
        st.pyplot(fig1)



    # --- Numerical Column Analysis ---


    selected_num_col = st.sidebar.selectbox("Select Numerical Column", numerical_cols)
    if selected_num_col:
        st.markdown(f"###  Numerical Analysis: {selected_num_col.capitalize()}")
        fig2, (ax1,ax2) = plt.subplots(1, 2, figsize=(14, 4))
        sns.histplot(df[selected_num_col].dropna(), kde=True, ax=ax1)
        ax1.set_title("Histogram")
        sns.boxplot(x=df[selected_num_col], ax=ax2)
        ax2.set_title("Boxplot")
        st.pyplot(fig2)


    # --- Correlation Heatmap ---


    st.markdown("###  Correlation Heatmap")
    corr = df[numerical_cols].corr()
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
    st.pyplot(fig3)

else:
    st.info("Please upload a CSV file to begin analysis.")


# Footer

st.markdown("---")
st.markdown(
    """
    <hr style="margin-top: 50px;">
    <div style='text-align: right; color: grey; font-size: 14px;'>
       Developed using Streamlit |  Contact: sipankardebnath@gmail.com
    </div>
    """,
    unsafe_allow_html=True
)
