⛽ PetroStream Ultra 2.0 - SBAA Basin Analysis Tool
https://petrosouhil.streamlit.app/
https://www.python.org/downloads/
https://opensource.org/licenses/MIT
An advanced petroleum geology dashboard for integrated source rock characterization, maturity analysis, and resource estimation of the Upper Devonian (Frasnian) interval in the SBAA Basin. Built with Streamlit and Plotly.
🎯 Features
📊 Geochemical Analysis
Rock-Eval Pyrolysis: TOC, S2, Tmax, HI, OI analysis
Maturity Assessment: Vitrinite reflectance (Ro) calculation using Jarvie (2007) proxy
Kerogen Typing: Van Krevelen diagrams (HI vs OI)
Cross-Plots: Interactive parameter correlation analysis
🗺️ Spatial Visualization
3D Surface Mapping: Interpolated property maps (Thickness, TOC, S2, Ro, HI)
Well Location Maps: HC Potential classification with interactive hover data
Contour Analysis: 2D contour generation with configurable resolution
📈 Petrophysical Tools
Synthetic Log Viewer: GR, RHOB, NPHI, RT, DT, PE tracks
Burial History Simulator: 1D basin modeling with thermal evolution
Maturity Windows: Oil generation, wet gas, dry gas zone identification
💎 Resource Estimation
Volumetric Calculations: OOIP/OGIP estimation using modified Jarvie (2012) methodology
Sensitivity Analysis: Recovery factor vs drainage area scenarios
HC Generation Model: Transformation ratio and expelled hydrocarbons
📄 Reporting
Automated PDF Reports: Technical documentation with basin statistics
CSV Export: Raw data export for external analysis
Interactive HTML: Dark-themed technical reports
🚀 Quick Start
Prerequisites
Python 3.11 or higher
pip package manager
Installation
bash
Copy
# Clone the repository
git clone https://github.com/yourusername/petrostream.git
cd petrostream

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run petrostream_app.py
Access the App
Open your browser and navigate to http://localhost:8501
📋 Requirements
plain
Copy
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
scipy>=1.11.0
plotly>=5.17.0
openpyxl>=3.1.0
🏗️ Architecture
plain
Copy
petrostream/
├── petrostream_app.py          # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── sbaa_basin_data.csv     # Well data (Rock-Eval, coordinates)
├── assets/
│   ├── dashboard_preview.png   # App screenshot
│   └── logo.png                # PetroStream logo
└── docs/
    ├── methodology.md          # Technical documentation
    └── api_reference.md        # Code documentation
🔬 Methodology
Maturity Calculation
Vitrinite reflectance (Ro) is calculated from Tmax using the Jarvie (2007) proxy:
plain
Copy
Ro = 0.018 × Tmax − 7.16
Table
Maturity Stage	Ro (%)	Tmax (°C)
Immature	< 0.6	< 435
Early Oil	0.6-0.9	435-445
Peak Oil	0.9-1.35	445-465
Wet Gas	1.35-2.0	465-480
Dry Gas	> 2.0	> 480
HC Potential Classification
Based on Peters & Cassa (1994) TOC thresholds:
Table
Classification	TOC (%)
Poor	< 0.5
Fair	0.5-1.0
Good	1.0-2.0
Very Good	2.0-4.0
Excellent	> 4.0
Resource Estimation
Shale Oil-in-Place (OOIP):
plain
Copy
OOIP = (Area × Thickness × φ × (1-Sw)) / (5.615 × Bo)
Gas-in-Place (OGIP):
plain
Copy
OGIP = (Mass × Vl × P) / (Pl + P) / 10^9
Where:
Vl = Langmuir volume (~100 scf/ton per % TOC)
Pl = Langmuir pressure (500 psi)
🎨 UI/UX Design
Dark Luxury Theme: Petroleum industry-inspired dark interface
Gold/Teal Color Scheme: Professional geoscience visualization
Responsive Layout: Optimized for desktop and tablet viewing
Interactive Plotly Charts: Zoom, pan, hover tooltips
Real-time Calculations: Instant parameter updates
📊 Data Sources
The application includes built-in data for 8 exploration wells in the SBAA Basin:
Table
Well	X	Y	Thickness (m)	TOC (%)	S2	Tmax (°C)	HI	OI
SBAA-1	7.5	5.5	70	1.44	4.39	446	315	19
DECH-1	6.5	7.5	68	2.65	16.04	440	484	26
OTLA-1	1.8	1.2	54	1.49	6.91	437	467	33
BDW-1	6.2	6.1	48	0.57	2.04	460	404	24
ODZ-1	5.8	5.0	185	5.74	4.06	445	292	46
OTRT-1	4.2	4.3	188	0.97	0.79	452	93	13
LT-1bis	2.0	2.1	173	0.61	0.43	443	53	48
MGR-1	5.9	4.8	253	0.71	1.88	454	128	22
🛠️ Development
Key Components
Data Loading & Caching:
Python
Copy
@st.cache_data
def load_data():
    # Well data with calculated parameters (Ro, PI, HC_Potential, Maturity)
    ...
Theme Configuration:
Python
Copy
def apply_theme(fig, title, height, ...):
    # Apply PetroStream dark theme to Plotly figures
    ...
Navigation System:
Python
Copy
NAV_ICONS = {
    "🏠  Overview": "Overview",
    "📊  Basin Registry": "Basin Registry",
    "🧪  Geochemical Lab": "Geochemical Lab",
    ...
}
menu = st.sidebar.radio("", list(NAV_ICONS.keys()))
Color Palette
Table
Color Name	Hex Code	Usage
Gold Bright	#f0c040	Primary accent, headers
Gold Mid	#c8982a	Secondary elements
Teal	#00d4aa	Success, active states
Blue Data	#4499ff	Data visualization
Amber	#ff8c00	Warnings, gas windows
Red Warn	#ff4444	Errors, dry gas
BG Void	#04080f	Background
BG Panel	#0c1424	Cards, panels
🐛 Troubleshooting
Common Issues
ValueError in Plotly charts:
Ensure all color values use 6-digit hex or rgba format (not 8-digit hex)
Check that hovertemplate uses proper f-string formatting
Module not found errors:
bash
Copy
pip install -r requirements.txt --upgrade
Streamlit cache issues:
bash
Copy
streamlit cache clear
📚 References
Jarvie, D.M. (2007) - Vitrinite reflectance proxy from Tmax
Peters, K.E. & Cassa, M.R. (1994) - Source rock evaluation
Jarvie, D.M. (2012) - Shale oil resource estimation
Pepper, A.S. & Corvi, P.J. (1995) - HC generation kinetics
👨‍💻 Author
Serhoudji Souhil - MSc Petroleum Geology
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments
Streamlit team for the amazing framework
Plotly team for interactive visualization tools
Petroleum geochemistry community for methodology standards
⛽ PetroStream Ultra 2.0 - Advanced Petroleum Geology Dashboard
