import streamlit as st
import home

import models.mean_variance_optimization as mvo
import models.hierarchical_risk_parity as hrp
import models.black_litterman_allocation as bla

import open_project 


# Page configurations in App
st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title=None,  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)

class Router:
    def display_router(self):
        # Sidebar attributes
        self.features = ['Home Page', 'Mean-Variance Optimization (MPT)', 'Hierarchical Risk Parity (HRP)', 'Black-Litterman Allocation (BLA)', 'Open Project (Feedbacks)']
        self.page = st.sidebar.selectbox('Choose Algorithm', self.features)
        st.sidebar.markdown('---')

    def route(self):
         # HOME PAGE
        if self.page == self.features[0]:
            home.display_home()
        
        # MEAN VARIANCE OPTIMIZATION
        elif self.page == self.features[1]:
            mvo.mean_variance_setup()

        # RISK PARITY
        elif self.page == self.features[2]:
            hrp.hrp_setup()

        # BLACK LITTERMAN
        elif self.page == self.features[3]:
            bla.bla_setup()

        else:
            open_project.visualize_feedbacks()
            
# Initiating class
route = Router()

# Displaying home structure
home.sidebar.sidebar_functionality()
route.display_router()
route.route()

home.sidebar.sidebar_inform_libs()
home.sidebar.sidebar_contact()