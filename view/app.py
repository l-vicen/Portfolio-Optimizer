import streamlit as st
import home as ho
import mean_variance_optimization as mvo

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
        self.features = ['Home Page', 'Mean-Variance Optimization (MPT)', 'Expected Returns', 'Risk Models', 'Black-Litterman Allocation', 'Hierarchical Risk Parity (HRP)']
        self.page = st.sidebar.selectbox('Choose Algorithm', self.features)
        st.sidebar.markdown('---')

    # TODO : Add feature to router
    def route(self):
         # HOME PAGE
        if self.page == self.features[0]:
            ho.display_home()
        
        # HOME PAGE
        elif self.page == self.features[1]:
            mvo.mean_variance_setup()

        else:
            pass
            
# Initiating class
route = Router()


ho.sidebar.sidebar_functionality()
route.display_router()
route.route()

ho.sidebar.sidebar_contact()