# Initialize librarys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stylable_container import stylable_container

if st.toggle('show video'):
    st.video('https://www.youtube.com/watch?v=I3zqpXxtsHY')