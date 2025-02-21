import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title('Slugtest evaluation')

st.subheader('Evaluating slug test in :orange[unconfined aquifers with the Bouwer & Rice method]', divider="orange")

st.markdown("""
            ### Introduction and Motivation
            Slug tests are quick and cost-effective field methods used to determine the hydraulic conductivity (K) of an aquifer. They involve a sudden change in water level within a well (either by adding or removing a known volume of water, or inserting/removing a slug) and measuring the subsequent water level recovery over time, see subsequent figure.
            
            These tests are ideal for:
            - Assessing aquifer properties in low-permeability formations.
            - Situations where pumping tests are not feasible due to time or space constraints.
            - Monitoring wells where minimal disturbance to the aquifer is desired.
            
            Types of Slug Tests:
            - Rising-head test: Water level rises after removal of a slug.
            - Falling-head test: Water level falls after adding water or a slug.
            
            **Why use slug tests?** They are fast, inexpensive, and suitable for small-scale investigations, making them a standard tool in hydrogeological site assessments.
           """)
           
lc0, rc0 = st.columns((1,1.3),gap = 'large')
with lc0:
    st.image('05_Applied_hydrogeology/FIGS/slug_confined.png', caption="Schematic representation of a slug test where a slug of water is added to a well. Figure from Kruseman and DeRidder - a Groundwater Project preserved book (https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/).")
with rc0:
    st.video('https://youtu.be/GTq72oB0qZo')
    st.write('_Video:_ Slugtest performed at the Varnum site (Sweden) by adding approximately 10 liter to an groundwater observation well.')


with st.expander('The Theory behind the Bouwer & Rice Method for Unconfined Aquifers'):
    st.markdown("""
            ### The Theory behinf the Bouwer & Rice Method for Unconfined Aquifers
            
            The **Bouwer and Rice (1976) method** is a widely used approach to evaluate **slug test data**, especially in **partially penetrating wells** in **unconfined aquifers**. It relates the **water level recovery** to the **hydraulic conductivity** of the aquifer, accounting for well geometry and screen penetration.
            
            The hydraulic conductivity $K$ is calculated using:
            """)
    st.latex(r'''K = \frac{r_c^2 \ln\left(\frac{R_e}{r_w}\right)}{2L} \cdot \frac{1}{t} \cdot \ln\left(\frac{h_t}{h_0}\right)''')

    st.markdown("""        
            **Where:**
            - $K$: Hydraulic conductivity (m/s)  
            - $r_c$: Radius of the well casing (m) 
            - $r_w$: Radius of the well screen (m)  
            - $R_e$: Effective radius of influence (m)   
            - $L$: Length of the well screen intersecting the aquifer (m)
            - $t$: Elapsed time since the slug event (s)  
            - $h_0$: Initial head displacement (m) 
            - $h_t$: Head displacement at time $t$ (m)
            
            **Estimating the Effective Radius $R_e$**
            The **effective radius** $R_e$ depends on the well penetration, which depends on the thickness and conductivity of the the well pack, the fraction of the screen that is below the water table, anisotropy and skin effects:  
            - **Fully penetrating well:**
            """)
            
    st.latex(r'''R_e = \frac{D}{2}''')
    
    st.markdown("""  
            *(where $D$ is the saturated aquifer thickness)*  
            
            - **Partially penetrating well:**
            """)
            
    st.latex(r'''R_e = 1.1L + r_w''')     
    
    st.markdown("""              
            - **For simplicity**, we use in this app:
            """)
            
    st.latex(r'''R_e = L''')
 
    st.markdown("""    
            Reference: Bouwer, H., & Rice, R. C. (1976). A slug test for determining hydraulic conductivity of unconfined aquifers with completely or partially penetrating wells. Water Resources Research, 12(3), 423-428.
           """)
    
"---"
# Available Data / Choose data

# Select data
columns = st.columns((1,1), gap = 'large')
with columns[0]:
    datasource = st.selectbox("**What data should be used?**",
    ("Varnum (SWE) 2018 - R4", "Load own CSV dataset"), key = 'Data')
with columns[1]:
    if(st.session_state.Data =="Load own CSV dataset"):
        slugsize = st.number_input("Slug size in cm³ (1 liter = 1000 cm³)", value = 700,step=1)
        h_static = st.number_input("Static water level (hydraulic head) in m", value = 0., step=0.01)
    


if (st.session_state.Data == "Varnum (SWE) 2018 - R4"):
    slugsize = 700
    h_static = 0
    # Data and parameter from Varnum (SWE) 2018 - R4
    m_time = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287] # time in minutes
    #m_head = [0.0000,0.0528,0.4278,0.6833,0.8195,0.8722,0.9139,0.9472,0.9750,0.9833,0.9917,1.0000,1.0000,0.9972,0.9972,0.9972,0.9972,0.9972,0.9972,0.9972,0.9889,0.9889,0.9889,0.9833,0.9833,0.9722,0.9750,0.9667,0.9556,0.9583,0.9583,0.9389,0.9389,0.9306,0.9222,0.9222,0.9139,0.9139,0.9056,0.9056,0.8972,0.8806,0.8861,0.8778,0.8695,0.8695,0.8611,0.8528,0.8445,0.8361,0.8361,0.8278,0.8195,0.8111,0.8028,0.8028,0.7945,0.7861,0.7861,0.7750,0.7667,0.7500,0.7583,0.7500,0.7417,0.7417,0.7333,0.7250,0.7167,0.7250,0.7083,0.7083,0.7000,0.6917,0.6833,0.6833,0.6583,0.6667,0.6556,0.6500,0.6417,0.6333,0.6333,0.6333,0.6250,0.6139,0.6139,0.6056,0.5972,0.5972,0.5889,0.5889,0.5722,0.5722,0.5639,0.5639,0.5639,0.5556,0.5472,0.5389,0.5389,0.5306,0.5306,0.5222,0.5139,0.5139,0.5056,0.5056,0.4945,0.4945,0.4945,0.4861,0.4778,0.4861,0.4778,0.4695,0.4611,0.4611,0.4528,0.4528,0.4445,0.4445,0.4445,0.4361,0.4361,0.4278,0.4250,0.4250,0.4167,0.4167,0.4083,0.4083,0.4000,0.4000,0.3917,0.3917,0.3833,0.3833,0.3833,0.3750,0.3750,0.3667,0.3667,0.3583,0.3583,0.3583,0.3500,0.3500,0.3417,0.3417,0.3417,0.3417,0.3333,0.3333,0.3250,0.3250,0.3250,0.3250,0.3167,0.3167,0.3056,0.3056,0.2972,0.2972,0.2972,0.2972,0.2972,0.2889,0.2889,0.2889,0.2806,0.2722,0.2722,0.2639,0.2722,0.2639,0.2639,0.2639,0.2556,0.2472,0.2556,0.2556,0.2472,0.2472,0.2472,0.2472,0.2389,0.2389,0.2306,0.2389,0.2389,0.2306,0.2306,0.2306,0.2222,0.2306,0.2139,0.2139,0.2222,0.2222,0.2222,0.2139,0.2139,0.2139,0.2139,0.2056,0.2056,0.2056,0.2056,0.2056,0.1972,0.1972,0.1945,0.1972,0.1972,0.1972,0.1972,0.1889,0.1889,0.1889,0.1806,0.1806,0.1806,0.1806,0.1806,0.1722,0.1722,0.1611,0.1722,0.1611,0.1611,0.1611,0.1611,0.1611,0.1528,0.1528,0.1528,0.1611,0.1528,0.1528,0.1445,0.1445,0.1528,0.1445,0.1445,0.1445,0.1361,0.1445,0.1361,0.1361,0.1361,0.1361,0.1361,0.1361,0.1278,0.1278,0.1278,0.1278,0.1195,0.1195,0.1195,0.1195,0.1195,0.1195,0.1195,0.1195,0.1111,0.1111,0.1111,0.1111,0.1111,0.1111,0.1111,0.1111,0.1111,0.1028,0.1028,0.1028,0.1028,0.1028,0.1028,0.1028,0.1028,0.0945,0.0945,0.0945,0.0945,0.0945]   # normalized drawdown in meters
    
    m_head = [0.00000,0.01131,0.09161,0.14633,0.17548,0.18678,0.19570,0.20284,0.20879,0.21057,0.21236,0.21414,0.21414,0.21355,0.21355,0.21355,0.21355,0.21355,0.21355,0.21355,0.21176,0.21176,0.21176,0.21057,0.21057,0.20820,0.20879,0.20700,0.20463,0.20522,0.20522,0.20106,0.20106,0.19927,0.19749,0.19749,0.19570,0.19570,0.19392,0.19392,0.19213,0.18857,0.18976,0.18797,0.18619,0.18619,0.18441,0.18262,0.18084,0.17905,0.17905,0.17727,0.17548,0.17370,0.17191,0.17191,0.17013,0.16834,0.16834,0.16596,0.16417,0.16061,0.16239,0.16061,0.15882,0.15882,0.15704,0.15525,0.15347,0.15525,0.15168,0.15168,0.14990,0.14811,0.14633,0.14633,0.14098,0.14276,0.14038,0.13919,0.13741,0.13562,0.13562,0.13562,0.13384,0.13146,0.13146,0.12968,0.12789,0.12789,0.12611,0.12611,0.12254,0.12254,0.12075,0.12075,0.12075,0.11897,0.11719,0.11540,0.11540,0.11362,0.11362,0.11183,0.11005,0.11005,0.10826,0.10826,0.10589,0.10589,0.10589,0.10410,0.10232,0.10410,0.10232,0.10053,0.09875,0.09875,0.09696,0.09696,0.09518,0.09518,0.09518,0.09340,0.09340,0.09161,0.09101,0.09101,0.08923,0.08923,0.08744,0.08744,0.08566,0.08566,0.08387,0.08387,0.08209,0.08209,0.08209,0.08030,0.08030,0.07852,0.07852,0.07673,0.07673,0.07673,0.07495,0.07495,0.07316,0.07316,0.07316,0.07316,0.07138,0.07138,0.06960,0.06960,0.06960,0.06960,0.06781,0.06781,0.06544,0.06544,0.06365,0.06365,0.06365,0.06365,0.06365,0.06187,0.06187,0.06187,0.06008,0.05830,0.05830,0.05651,0.05830,0.05651,0.05651,0.05651,0.05473,0.05294,0.05473,0.05473,0.05294,0.05294,0.05294,0.05294,0.05116,0.05116,0.04937,0.05116,0.05116,0.04937,0.04937,0.04937,0.04759,0.04937,0.04581,0.04581,0.04759,0.04759,0.04759,0.04581,0.04581,0.04581,0.04581,0.04402,0.04402,0.04402,0.04402,0.04402,0.04224,0.04224,0.04165,0.04224,0.04224,0.04224,0.04224,0.04045,0.04045,0.04045,0.03867,0.03867,0.03867,0.03867,0.03867,0.03688,0.03688,0.03451,0.03688,0.03451,0.03451,0.03451,0.03451,0.03451,0.03272,0.03272,0.03272,0.03451,0.03272,0.03272,0.03094,0.03094,0.03272,0.03094,0.03094,0.03094,0.02915,0.03094,0.02915,0.02915,0.02915,0.02915,0.02915,0.02915,0.02737,0.02737,0.02737,0.02737,0.02558,0.02558,0.02558,0.02558,0.02558,0.02558,0.02558,0.02558,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02380,0.02202,0.02202,0.02202,0.02202,0.02202,0.02202,0.02202,0.02202,0.02023,0.02023,0.02023,0.02023,0.02023]
elif(st.session_state.Data =="Load own CSV dataset"):
    # LOAD CSV / Initialize
    m_time = []
    m_head = []
    uploaded_file = st.file_uploader("Choose a CSV file for evaluation (time in seconds / normalized heads in meters)")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        m_time = list(df.iloc[:,0].values)
        m_head = list(df.iloc[:,1].values)
    st.write(m_head)

"---"
st.subheader('Computation')

# Computation

# Fixed values

tmax = 300

# User defined values


    
# Define the minimum and maximum for the logarithmic scale
log_min = -6.0 # Corresponds to 10^-7 = 0.0000001
log_max =  -2.0  # Corresponds to 10^0 = 1

lc1, rc1 = st.columns((1,1))
with lc1:
    with st.expander('Provide well parameter'):
        rc = st.number_input("well casing radius", value = 0.03,step=.0001, format="%.4f")
        rw = st.number_input("well screen radius", value = 0.085,step=.001, format="%.3f")
        L  = st.number_input("Lenght of the well screen", value = 2.1,step=.1, format="%.1f")
    


with rc1:
    # Log slider with input and print
    t_off = st.slider('**Time offset** in s', 0, 60, 0, 1)
    container = st.container()
    K_slider_value=st.slider('_(log of) hydraulic conductivity in m/s_', log_min,log_max,-3.0,0.01,format="%4.2f" )
    K = 10 ** K_slider_value
    container.write("**Hydraulic conductivity in m/s:** %5.2e" %K)

# Calculation
H0 = 0.01*slugsize/np.pi/(rc*100)**2
F = 2 * np.pi * L/np.log(L/rw)
prq = np.pi * rc**2
t = np.arange(0, tmax, 1)

t_plot=[]
for i in t:
  t_plot.append(i+t_off)
  
h_norm = []
for i in m_head:
    h_norm.append((i-h_static)/H0)

exp_decay = np.exp(-F/prq*K*t)

# Plot figure
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot()
ax.plot(t_plot,exp_decay, color='magenta', label='computed')
plt.plot(m_time,h_norm, 'bo', mfc='none', label='measured')
plt.axis([0,tmax,0,1])

plt.xlabel(r'time t in (s)', fontsize=14)
plt.ylabel(r'H/Ho', fontsize=14)
plt.title('Slugtest evaluation (positive slug)', fontsize=16)
plt.legend(fontsize=14)

st.pyplot(fig=fig)

st.write('Slugsize = ', slugsize, ' cm³')
st.write('Initial water level $H_0$ = ', H0, ' m')