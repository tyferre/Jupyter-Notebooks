import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button

st.title('📃 Basic Theory underlying PumpingTestAnalysis')

st.subheader(':orange-background[The Theis, Neuman, and Hantush-Jacob solution]', divider="orange")

st.markdown("""
            ### Introduction and Overview
            This part of the application provides a general overview about groundwater flow towards a well. The basic principles for a quantitative description of the process with mathematical equations are explained and derived. The individual details for specific solutions (like Theis, Hantush/Jacob, Neuman) are provided in the specific parts of the application.
            
            We provide a few questions to allow you to assess the current state of your knowledge.
"""
)

# Initial assessment
lc1, cc1, rc1 = st.columns([1,1.5,1])

with cc1:
    show_initial_assessment = button("**Show/Hide the initial assessment**", key = 'button1')

if show_initial_assessment:
    columnsQ1 = st.columns((1,1))
     
    with columnsQ1[0]:
        stb.single_choice(":orange[**Where do you find the hydraulic head within a confined aquifer?**]",
                  ["Below the aquifer top.", "Directly at the aquifer top.", "Above the aquifer top.", "A confined aquifer doesn't show a hydraulic head"],
                  2,success='CORRECT! Confined aquifer heads are above the top of the aquifer. This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think the situation.')
        stb.single_choice(":orange[**What is considered as transient state?**]",
                  ["The model represents a long-term average.", "The model changes over time.", "The model changes over space.", "When the model accounts for water abstraction."],
                  1,success='CORRECT! Head changes with time in a transient situation. This understanding is important for the subsequent steps.', error='This option is not suitable. Re-Think the situation.')             
    with columnsQ1[1]:
        stb.single_choice(":orange[**What parameter is used to describe the ability of an aquifer to transmit water?**]",
                  ["Storativity", "Hydraulic head", "Transmissivity", "Specific storage"],
                  2,success='CORRECT! Transmissivity describes the ability of an aquifer to transmit water.', error='This is not correct. Feel free to re-think this and/or look up terms and answer again.') 
        stb.single_choice(":orange[**What is the equivalent to 0.001 m³/s?**]",
                  ["1 Liter per second", "10 Liters per second", "100 Liters per second", "1 000 Liters per second", "10 000 Liters per second"],
                  0,success='CORRECT! 1000 Liters are one m³', error='This is not correct. Feel free to re-think this and/or look up the relationship between liters and cubic meters, and answer again.')  
          
"---"

st.markdown("""
            ### General situation
            The mathematics included in this application consider only homogeneous and isotropic aquifers. Natural aquifers are not homogeneous nor isotropic (although they come close to isotropic in most instances), so in practice the procedures presented in this application are applied to heterogeneous and anisoptropic aquifers to glean average parameters representative of bulk behavior of the system. The aquifer can be confined, leaky, or unconfined. 
            
            If a well is pumping water out of the aquifer, water flows radially towards the well. 
            
            The following equation can be used  to describe hydraulic head at a distance _r_ from the well. This equation accounts for 1-dimensional radial transient flow toward a fully penetrating well within a confined or unconfined aquifer without any other sinks and sources of water.
"""
)



st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
st.markdown("""
            ### Mathematical model and solution
            Charles V. Theis (1935) derived an equation describing drawdown _s_ with radial distance _r_ from the well.
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.markdown("""
            with the well function
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.markdown("""
            and the dimensionless variable _u_
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.markdown("""
            This equation is not easy to solve. Historically, values for the well function were provided by tables, or were presented as a type-curve of drawdown as a function of time around a well. 
            
            Plotting field measurements of drawdown over time during a pumping test on graph paper and matching it to the type curve to estimate transmissivity _T_ and storativity _S_ is a time-tested hydrogeological method. 
            
            Today however, rather than physically plotting data on paper, we use computer codes to match the data to the type curve because it is easier and more convenient. 
            
            However, it is best practice to view the data in graphical form whether it is plotted by hand or by a computer because the shape of the curve provides insight to the nature of the groundwater system and sometimes plotting the data reveals errors in the data.
                  
            Subsequently, in this application, the Theis equation is solved using Python codes.
"""
)            

st.markdown (
    """   
    :green
    ___
"""
)
st.markdown("""
Theis, C.V., 1935. The relation between the lowering of the piezometric surface and the rate and duration of discharge of a well using groundwater storage, Transactions of the American Geophysical Union, volume 16, pages 519-524.
"""
)            

columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    st.write()
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_🙋_▶️ Transient_Flow to a Well.py")
