def sidebar_styles():
    return """
    <style>
    div.stButton > button {
        font-size: 14px;
        font-weight: 400;
        color: white;
        background-color: transparent;
        border: none;
        padding: 0;
        text-align: left;
    }
    }
    </style>
    """
def hide_streamlit_style():
    return """
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

def background_style():
    return """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://t3.ftcdn.net/jpg/04/29/35/62/360_F_429356296_CVQ5LkC6Pl55kUNLqLisVKgTw9vjyif1.jpg');
        background-size: fit;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    [data-testid="stAppViewContainer"] > .main {
        background-color: rgba(0,0,0,0);
    }

    
    [data-testid="stSidebar"] {
        background-color: rgba(0,0,0,0.6);
    }
    </style>
    """
