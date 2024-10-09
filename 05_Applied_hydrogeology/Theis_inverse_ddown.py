# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import streamlit as st

st.title('Theis drawdown prediction - Fitting Formation parameter to measured data')
st.write('This notebook demonstrate the application of the Theis principle for pumping test evaluation in confined, transient setups. The notebook is based on an Spreadsheet from Prof. Rudolf Liedl.')

st.subheader('General situation')
st.write('We consider a confined aquifer with constant transmissivity. If a well is pumping water out of the aquifer, radial flow towards the well is induced.')
st.write('The calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined aquifer without further sinks and sources:')
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')

st.subheader('Mathematical model and solution')
st.write('Charles V. Theis presented a solution for this by deriving')
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.write('with the well function')
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.write('and the dimensionless variable')
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.write('This equations are not easy to solve. Historically, values for the well function were provided by tables or as so called type-curve. The type-curve matching with experimental data for pumping test analysis can be considered as one of the basic hydrogeological methods.')
st.write('However, modern computer provide an easier and more convinient way to solve the 1D radial flow equation based on the Theis approach. Subsequently, the Theis equation is solved with Python routines. The results for the measured data are graphically presented.')
"---"

# Computation


# Data from SYMPLE exercise
m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
m_time_s = [i*60 for i in m_time] # time in seconds
m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters

num_times = len(m_time)

# Parameters needed to solve Theis (From the SYMPLE example/excercise)
r = 120       # m
b = 8.5       # m
Qs = 0.3/60   # m^3/s
Qd = Qs*60*24 # m^3/d

# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def theis_wu(Q, T, s):
    wu = s * 4. * np.pi * T / Q
    return wu

def compute_s(T, S, t, Q, r):
    u = theis_u(T, S, r, t)
    s = theis_s(Q, T, u)
    return s

# (Here, the methode computes the data for the well function. Those data can be used to generate a type curve.)
u_max = 1
r_max = 100000
u  = [u_max for x in range(r_max)]
um = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
um_inv = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]
w_um = [well_function(u_max/r_max) for x in range(r_max)]

for x in range(1,r_max,1):
    if x>0:
        u[x] = x*u_max/r_max
        u_inv[x] = 1/u[x]
        w_u[x] = well_function(u[x])

# This is the function to plot the graph with the data     

# Get input data
# Define the minimum and maximum for the logarithmic scale

log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
log_max1 = 0.0  # T / Corresponds to 10^0 = 1

log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
log_max2 = 0.0  # S / Corresponds to 10^0 = 1

max_t = 86400*3
max_s = 10
    
columns = st.columns((1,1), gap = 'large')

with columns[0]:
    T_slider_value=st.slider('(log of) Transmissivity in m2/s', log_min1,log_max1,-4.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    T = 10 ** T_slider_value
    # Display the logarithmic value
    st.write("**Transmissivity in m2/s:** %5.2e" %T)
    S_slider_value=st.slider('(log of) Storativity', log_min2,log_max2,-4.0,0.01,format="%4.2f" )
    # Convert the slider value to the logarithmic scale
    S = 10 ** S_slider_value
    # Display the logarithmic value
    st.write("**Storativity (dimensionless):** %5.2e" %S)
with columns[1]:
    t_search = st.slider(f'**Select the value of time for printout**', 1,max_t,1,1)    
    
# Compute K and SS to provide parameters for plausability check
# (i.e. are the parameter in a reasonable range)
K = T/b     # m/s
SS = S/b    # 1/m

# PLOT MEASURED DATA
x = 0
for t1 in m_time_s:
    um[x] = theis_u(T,S,r,t1)
    um_inv[x] = 1/um[x]
    w_um[x] = theis_wu(Qs,T,m_ddown[x])
    x = x+1

# PLOT DRAWDOWN VS TIME

# Range of delta_h / delta_l values (hydraulic gradient)
t2 = np.linspace(1, max_t, 200)
    
# Compute Q for each hydraulic gradient
s  = compute_s(T, S, t2, Qs, r)

# Compute s for a specific point
x_point = t_search
y_point = compute_s(T, S, t_search, Qs, r)
    
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(1, 2, 1)
ax.plot(u_inv, w_u)
ax.plot(um_inv[:num_times], w_um[:num_times],'ro')
plt.yscale("log")
plt.xscale("log")
plt.axis([1,1E5,1E-2,1E+2])
ax.set(xlabel='1/u', ylabel='w(u)',title='Theis drawdown')
ax.grid(which="both")
plt.legend(('well function','measured'))

ax = fig.add_subplot(1, 2, 2)
plt.plot(t2, s, linewidth=3., color='r', label=r'Drawdown prediction')
plt.xlim(1, max_t)
plt.ylim(max_s, 0)
plt.plot(x_point,y_point, marker='o', color='b',linestyle ='None', label='drawdown output') 
plt.xlabel(r'Time in sec', fontsize=14)
plt.ylabel(r'Drawdown in m', fontsize=14)
plt.title('Drawdown prediction with Theis', fontsize=16)
plt.legend()
plt.grid(True)
    
st.pyplot(fig)

st.write("Transmissivity T = ","% 10.2E"% T, " m^2/s")
st.write("Storativity    S = ","% 10.2E"% S, "[-]")
st.write(' ')
st.write('Distance from the well (in ): %8.2f' %r)
st.write("Time since pumping start (in s): ", x_point)
st.write('Drawdown at this distance and time (in m):  %5.2f' %y_point)


