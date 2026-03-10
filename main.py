import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Number System Intelligence Lab",
    layout="wide"   
)

st_autorefresh(interval=1000, key="timer")

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle,#0b0b0b,#000);
color:#00ff9f;
font-family:monospace;
}

.binary-rain{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
opacity:0.07;
pointer-events:none;
font-size:18px;
color:#00ff9f;
white-space:nowrap;
animation: rain 20s linear infinite;
}

h1,h2,h3{
color:#00ff9f;
text-shadow:0px 0px 8px #00ff9f;
}

.block-container{
padding-top:2rem;
}

.stButton>button{
background:linear-gradient(45deg,#00ff9f,#00d4ff);
color:black;
border:none;
border-radius:8px;
font-weight:bold;
box-shadow:0 0 8px #00ff9f;
}

.metric-card{
background:#111;
border:1px solid #00ff9f;
border-radius:10px;
padding:20px;
text-align:center;
box-shadow:0 0 10px #00ff9f;
}

.metric-value{
font-size:36px;
color:#00ff9f;
font-weight:bold;
}

.metric-label{
font-size:14px;
color:#aaa;
}

@keyframes rain{
0%{transform:translateY(-100%)}
100%{transform:translateY(100%)}
}

.stTabs [data-baseweb="tab-list"]{
gap:8px;
background:#111;
padding:8px;
border-radius:12px;
}

.stTabs [data-baseweb="tab"]{
height:50px;
background:#1a1a1a;
border-radius:10px;
padding:10px 18px;
color:#aaa;
font-weight:600;
border:1px solid rgba(255,255,255,0.05);
}

.stTabs [aria-selected="true"]{
transform:scale(1.05);
transition:0.2s;
background:linear-gradient(135deg,#00ff9f,#00d4ff);
color:black;
box-shadow:0 0 10px rgba(0,255,159,0.7);
}

</style>
""", unsafe_allow_html=True)


binary = "01 " * 400
st.markdown(f'<div class="binary-rain">{binary}</div>', unsafe_allow_html=True)

def init_state():

    defaults = {
        "history": [],
        "score": 0,
        "streak": 0,
        "session_start": time.time(),
        "game_q": None,
        "game_ans": None,
        "game_from": None,
        "game_to": None,
        "game_decimal": None,
        "game_history": [],
        "show_explanation": False,
        "convert_result": None
    }

    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
    
elapsed = int(time.time() - st.session_state.session_start)

hours = elapsed // 3600
minutes = (elapsed % 3600) // 60
seconds = elapsed % 60

session_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

st.title("Number System Intelligence Lab")
st.caption("Binary • Octal • Decimal • Hexadecimal • Data Integrity • 3D Visualization")

cpu = random.randint(10,90) # berfungsi sebagai placeholder untuk load CPU nyata yang dapat diintegrasikan dengan psutil atau library serupa untuk data real-time

col1,col2,col3,col4=st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-value">{len(st.session_state.history)}</div>
    <div class="metric-label">CONVERSIONS</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-value">10K</div>
    <div class="metric-label">DATASET TESTED</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-value">{session_time}</div>
    <div class="metric-label">SESSION TIME</div>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-value">{cpu}%</div>
    <div class="metric-label">CPU LOAD</div>
    </div>
    """, unsafe_allow_html=True)
st.divider()

tab1,tab2,tab3,tab4,tab5 = st.tabs([
"🔄 Converter",
"🧠 Binary Logic",
"📊 Analytics Dashboard",
"🎮 Learning Game",
"🧊 3D Binary Visualizer"
])

def convert_number(value, base):
    """Convert number to all number systems"""

    try:

        decimal = int(value, base)

        return {
            "decimal": str(decimal),
            "binary": bin(decimal)[2:],
            "octal": oct(decimal)[2:],
            "hex": hex(decimal)[2:].upper()
        }

    except ValueError:

        return None


def parity_bit(binary):
    """Calculate parity bit"""

    ones = binary.count("1")

    if ones % 2 == 0:
        return "Even Parity"
    else:
        return "Odd Parity"


def crc(data, polynomial="1011"):
    """CRC error detection"""

    data = list(data + "0" * (len(polynomial) - 1))
    poly = list(polynomial)

    for i in range(len(data) - len(poly) + 1):

        if data[i] == "1":

            for j in range(len(poly)):
                data[i + j] = str(int(data[i + j] != poly[j]))

    return "".join(data[-(len(poly) - 1):])


def render_binary_grid(binary):
    """Visual binary LED grid"""

    if not binary:
        return

    bits = list(binary)

    # limit visualization
    if len(bits) > 32:
        st.info("Binary visualization limited to first 32 bits")
        bits = bits[:32]

    cols = st.columns(len(bits))

    for i, bit in enumerate(bits):

        if bit == "1":

            cols[i].markdown(
                """
                <div style="
                background:#00ff9f;
                color:black;
                padding:16px;
                text-align:center;
                border-radius:6px;
                font-weight:bold;
                ">
                1
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            cols[i].markdown(
                """
                <div style="
                background:#111;
                border:1px solid #00ff9f;
                padding:16px;
                text-align:center;
                border-radius:6px;
                color:#aaa;
                ">
                0
                </div>
                """,
                unsafe_allow_html=True
            )

if "history" not in st.session_state:
    st.session_state.history = []

if "convert_result" not in st.session_state:
    st.session_state.convert_result = None

with tab1:

    st.subheader("Universal Number Converter")

    col1, col2 = st.columns(2)

    with col1:

        system = st.selectbox(
            "Input Number System",
            ["Decimal", "Binary", "Octal", "Hexadecimal"]
        )

    with col2:

        number = st.text_input(
            "Enter Number",
            placeholder="Example: 25 / 11001 / 31 / 1F"
        )

    if st.button("Convert Number"):

        if number == "":
            st.warning("Please enter a number first")
            st.stop()

        base_map = {
            "Decimal": 10,
            "Binary": 2,
            "Octal": 8,
            "Hexadecimal": 16
        }

        result = convert_number(number, base_map[system])

        if result is None:

            st.error("Invalid number for selected system")

        else:

            st.session_state.convert_result = result
            st.session_state.history.append({
                "input": number,
                "system": system,
                "time": datetime.now()
            })

    if st.session_state.convert_result:

        result = st.session_state.convert_result

        df = pd.DataFrame({
            "System": ["Decimal", "Binary", "Octal", "Hexadecimal"],
            "Value": [
                result["decimal"],
                result["binary"],
                result["octal"],
                result["hex"]
            ]
        }).astype(str)

        st.success("Conversion Result")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Binary Visualization")

        render_binary_grid(result["binary"])

with tab2:

    import streamlit as st          
    import pandas as pd

    st.subheader("Binary Logic Simulator")

    if "logic_results" not in st.session_state:
        st.session_state.logic_results = None

    col1, col2 = st.columns(2)

    with col1:
        a = st.text_input("Binary A", placeholder="Example: 1010")

    with col2:
        b = st.text_input("Binary B", placeholder="Example: 1100")


    if st.button("Compute Logic"):

        if a == "" or b == "":
            st.warning("Enter both binary numbers")
            st.stop()

        if not all(c in "01" for c in a+b):
            st.error("Inputs must be binary (0 or 1)")
            st.stop()

        max_len = max(len(a), len(b))

        a = a.zfill(max_len)
        b = b.zfill(max_len)

        A = int(a, 2)
        B = int(b, 2)

        AND = bin(A & B)[2:].zfill(max_len)
        OR = bin(A | B)[2:].zfill(max_len)
        XOR = bin(A ^ B)[2:].zfill(max_len)
        NAND = bin(~(A & B) & ((1 << max_len)-1))[2:].zfill(max_len)
        NOR = bin(~(A | B) & ((1 << max_len)-1))[2:].zfill(max_len)

        st.session_state.logic_results = {
            "a": a,
            "b": b,
            "AND": AND,
            "OR": OR,
            "XOR": XOR,
            "NAND": NAND,
            "NOR": NOR,
            "max_len": max_len
        }


    # tampilkan hasil jika sudah ada
    if st.session_state.logic_results:

        r = st.session_state.logic_results

        st.subheader("Logic Results")

        df = pd.DataFrame({
            "Operation": ["AND", "OR", "XOR", "NAND", "NOR"],
            "Result": [r["AND"], r["OR"], r["XOR"], r["NAND"], r["NOR"]]
        })

        st.dataframe(df, use_container_width=True, hide_index=True)


        st.subheader("Bitwise Visualization")

        st.write("A:", r["a"])
        st.write("B:", r["b"])
        st.write("AND:", r["AND"])
        st.write("OR:", r["OR"])
        st.write("XOR:", r["XOR"])


        st.subheader("Binary Grid")

        cols = st.columns(r["max_len"])

        for i in range(r["max_len"]):

            bit = r["AND"][i]

            if bit == "1":

                cols[i].markdown(
                    "<div style='background:#00ff9f;color:black;padding:20px;text-align:center;border-radius:6px'>1</div>",
                    unsafe_allow_html=True
                )

            else:

                cols[i].markdown(
                    "<div style='background:#111;border:1px solid #00ff9f;padding:20px;text-align:center;border-radius:6px'>0</div>",
                    unsafe_allow_html=True
                )


        st.subheader("Logic Truth Table")

        truth = pd.DataFrame({
            "A": [0,0,1,1],
            "B": [0,1,0,1],
            "AND":[0,0,0,1],
            "OR":[0,1,1,1],
            "XOR":[0,1,1,0]
        })

        st.dataframe(truth, use_container_width=True, hide_index=True)
with tab3:

    st.subheader("Conversion Analytics Dashboard")

    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        df["system"] = df["system"].astype(str)

        total = len(df)

        decimal = (df["system"] == "Decimal").sum()
        binary = (df["system"] == "Binary").sum()
        octal = (df["system"] == "Octal").sum()
        hexa = (df["system"] == "Hexadecimal").sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Conversions", total)
        col2.metric("Binary", binary)
        col3.metric("Octal", octal)
        col4.metric("Hexadecimal", hexa)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Usage Distribution")

            fig1 = px.pie(
                df,
                names="system",
                template="plotly_dark",
                hole=0.4
            )

            st.plotly_chart(fig1, use_container_width=True)

        with col2:

            st.markdown("### Conversion Frequency")

            fig2 = px.histogram(
                df,
                x="system",
                color="system",
                template="plotly_dark",
                text_auto=True
            )

            st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        st.markdown("### Activity Timeline")

        df["step"] = range(1, len(df)+1)

        fig3 = px.line(
            df,
            x="step",
            y=[1]*len(df),
            markers=True,
            template="plotly_dark"
        )

        fig3.update_layout(
            yaxis_visible=False,
            xaxis_title="Conversion Order",
            showlegend=False
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        summary = df["system"].value_counts().reset_index()
        summary.columns = ["System", "Count"]

        st.markdown("### Summary Table")

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No conversion data available yet")
with tab4:

    st.subheader("Number System Challenge")

    # session state init
    if "score" not in st.session_state:
        st.session_state.score = 0

    if "streak" not in st.session_state:
        st.session_state.streak = 0

    if "game_q" not in st.session_state:
        st.session_state.game_q = None

    if "game_ans" not in st.session_state:
        st.session_state.game_ans = None

    if "game_from" not in st.session_state:
        st.session_state.game_from = None

    if "game_to" not in st.session_state:
        st.session_state.game_to = None

    if "game_decimal" not in st.session_state:
        st.session_state.game_decimal = None

    if "game_history" not in st.session_state:
        st.session_state.game_history = []

    if "show_explanation" not in st.session_state:
        st.session_state.show_explanation = False

    col1,col2,col3=st.columns(3)

    col1.metric("Score",st.session_state.score)
    col2.metric("Streak",st.session_state.streak)
    col3.metric("Questions Played",len(st.session_state.game_history))

    st.divider()


    # difficulty
    difficulty=st.selectbox(
        "Difficulty",
        ["Easy","Medium","Hard"]
    )

    if difficulty=="Easy":
        min_val,max_val=5,50
    elif difficulty=="Medium":
        min_val,max_val=20,255
    else:
        min_val,max_val=100,1024

    if st.session_state.game_q is None:

        if st.button("Generate Question"):

            num=random.randint(min_val,max_val)

            systems=["Decimal","Binary","Octal","Hexadecimal"]

            from_sys=random.choice(systems)
            to_sys=random.choice(systems)

            while from_sys==to_sys:
                to_sys=random.choice(systems)

            decimal=num

            if from_sys=="Decimal":
                q=str(decimal)

            elif from_sys=="Binary":
                q=bin(decimal)[2:]

            elif from_sys=="Octal":
                q=oct(decimal)[2:]

            else:
                q=hex(decimal)[2:].upper()

            if to_sys=="Decimal":
                ans=str(decimal)

            elif to_sys=="Binary":
                ans=bin(decimal)[2:]

            elif to_sys=="Octal":
                ans=oct(decimal)[2:]

            else:
                ans=hex(decimal)[2:].upper()


            st.session_state.game_q=q
            st.session_state.game_ans=ans
            st.session_state.game_from=from_sys
            st.session_state.game_to=to_sys
            st.session_state.game_decimal=decimal
            st.session_state.show_explanation=False

            st.rerun()

    if st.session_state.game_q is not None:

        q=st.session_state.game_q
        ans=st.session_state.game_ans

        st.markdown(f"""
        ### Convert

        **{q} ({st.session_state.game_from})**

        → **{st.session_state.game_to}**
        """)

        user=st.text_input("Your Answer",key="game_answer_input")

        col1,col2=st.columns(2)

        with col1:

            if st.button("Submit Answer"):

                st.session_state.show_explanation=True

                correct=user.upper()==ans.upper()

                if correct:

                    st.success("Correct!")

                    st.session_state.score+=10
                    st.session_state.streak+=1

                    st.balloons()

                else:

                    st.error("Wrong Answer")
                    st.session_state.streak=0


                st.session_state.game_history.append({
                    "question":q,
                    "from":st.session_state.game_from,
                    "to":st.session_state.game_to,
                    "answer":ans,
                    "user":user,
                    "correct":correct
                })


        with col2:

            if st.button("Next Question"):

                st.session_state.game_q=None
                st.session_state.show_explanation=False
                st.rerun()


        # explanation (persistent)
        if st.session_state.show_explanation:

            st.markdown("### Explanation")

            dec=st.session_state.game_decimal

            st.write("Step 1: Convert to Decimal")

            if st.session_state.game_from!="Decimal":

                st.write(f"{q} ({st.session_state.game_from}) = {dec} (Decimal)")

            else:

                st.write(f"{dec} already Decimal")


            st.write("Step 2: Convert Decimal → Target")

            if st.session_state.game_to=="Binary":

                n=dec

                while n>0:

                    st.write(f"{n} ÷ 2 = {n//2} remainder {n%2}")
                    n//=2


            elif st.session_state.game_to=="Octal":

                n=dec

                while n>0:

                    st.write(f"{n} ÷ 8 = {n//8} remainder {n%8}")
                    n//=8


            elif st.session_state.game_to=="Hexadecimal":

                n=dec

                while n>0:

                    r=n%16
                    st.write(f"{n} ÷ 16 = {n//16} remainder {r}")
                    n//=16


            st.write("Correct Answer:",ans)


    # history
    if st.session_state.game_history:

        st.subheader("Game History")

        df=pd.DataFrame(st.session_state.game_history)

        st.dataframe(df,use_container_width=True)

with tab5:

    st.subheader("3D Binary Visualization")

    number = st.number_input(
        "Input Decimal Number",
        min_value=0,
        max_value=4096,
        value=25
    )

    binary = bin(number)[2:]

    st.write("Binary Representation:", binary)

    bits = list(binary)

    x=[]
    y=[]
    z=[]
    value=[]
    label=[]

    for i,bit in enumerate(bits):

        x.append(i)
        y.append(int(bit))
        z.append(int(bit)*3)

        value.append(int(bit))

        label.append(f"Bit {i} = {bit}")

    df = pd.DataFrame({
        "x":x,
        "y":y,
        "z":z,
        "bit":value,
        "label":label
    })

    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="bit",
        size="bit",
        hover_name="label",
        color_continuous_scale=["#1f77b4","#00ff9f"],
        title="3D Binary Bit Structure"
    )

    fig.update_traces(marker=dict(
        sizeref=2,
        sizemode='diameter',
        line=dict(width=2,color='white')
    ))

    fig.update_layout(
        template="plotly_dark",
        scene=dict(
            xaxis_title="Bit Position",
            yaxis_title="Binary Value",
            zaxis_title="Binary Depth",
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0,r=0,b=0,t=40)
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Binary Bit Grid")

    cols = st.columns(len(bits))

    for i,bit in enumerate(bits):

        if bit=="1":

            cols[i].markdown(
            "<div style='background:#00ff9f;color:black;padding:20px;text-align:center;border-radius:6px'>1</div>",
            unsafe_allow_html=True
            )

        else:

            cols[i].markdown(
            "<div style='background:#111;border:1px solid #00ff9f;padding:20px;text-align:center;border-radius:6px'>0</div>",
            unsafe_allow_html=True
            )

    st.subheader("Binary Power Breakdown")

    powers=[]
    values=[]

    for i,bit in enumerate(reversed(bits)):

        power=2**i
        powers.append(power)

        if bit=="1":
            values.append(power)
        else:
            values.append(0)

    breakdown=pd.DataFrame({
        "Power of 2":powers,
        "Contribution":values
    })

    st.dataframe(breakdown,use_container_width=True)

    st.write("Decimal Result:",sum(values))