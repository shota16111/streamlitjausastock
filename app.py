import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('日本と米国の株価可視化アプリ')


st.sidebar.write("""
# いろいろな株価
# https://finance.yahoo.com/　から情報取得しています。
こちらは株価可視化アプリツールです。以下のオプションから表示日数を指定
"""
)
st.sidebar.write("""
## 表示日数選択
"""
)
days = st.sidebar.slider('日数',1,50,20)

st.write(
    f"""
    ### 過去 **{days}日間** の企業の株価
    """
)

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr =yf.Ticker(tickers[company])
        hist =tkr.history(period = f'{days}d')
        hist.index =hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist =hist.T
        hist.index.name = 'Name'
        df =  pd.concat([df, hist])
    return df

try:
    st.sidebar.write(
        """
        ## 株価の範囲指定
        """
    )
    ymin,ymax =st.sidebar.slider(
    '範囲を指定してください',
    0.0, 3500.0, (0.0, 3500.0)
    )


    tickers = {
        'microsoft':'MSFT',
        'netflix':'NFLX',
        'honda':'HMC',
        'toyota':'TM',
        'sony':'SONY',
        'amazon':'AMZN',
        'apple':'AAPL',
        'google':'GOOG',
    }
    df =get_data(days, tickers)
    companies =st.multiselect(
        '会社名を選択してください',
        list(df.index),
        ['netflix','microsoft','amazon','google']
    )
    if not  companies:
        st.error('少なくとも一社は選んでください。') 
    else:
        data = df.loc[companies]
        st.write("### 株価（USD）",data.sort_index())
        data=data.T.reset_index()
        data=pd.melt(data,id_vars=['Date']).rename(
            columns={'value':'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity =0.8,clip = True)
            .encode(
                x ="Date:T",
                y =alt.Y("Stock Prices(USD):Q",stack =None, scale=alt.Scale(domain=[ymin,ymax])),
                color ="Name:N"
            )
        )
        st.altair_chart(chart, use_container_width=True)
        
        st.sidebar.write(
        """
        ## ソースコード→https://github.com/shota16111/streamlitjausastock
        """
        )  
except:
    st.error("エラーが起きているようです。")
