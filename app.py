import streamlit as st

st.set_page_config(
    page_title="Adepu Harshavardhan | AI/ML Portfolio",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 Adepu Harshavardhan")
st.subheader("AI/ML & Generative AI Engineer | Building Production-Ready Applications")

st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**GenAI Developer** | Passionate about building practical AI applications using Gemini, LangChain & Streamlit")
    st.markdown("Open to **Fresher / Returnship / Entry-Level** opportunities in AI/ML (2026)")

with col2:
    st.image("https://avatars.githubusercontent.com/u/Adepuharshavardhan2001", width=130)

st.markdown("---")

# Featured Projects
st.header("Featured Projects")

projects = [
    {
        "title": "CalmMind - Mental Health Support Chatbot",
        "desc": "Empathetic multi-turn Mental Health Assistant using Gemini + LangChain. Provides emotional support, mindfulness guidance & coping strategies.",
        "tech": "Gemini API, LangChain, Streamlit",
        "live": "https://sentiment---with---cot-from-customer-reviews-kx8vbxhrpcgtybrdv.streamlit.app/",          
        "github": "https://github.com/Adepuharshavardhan2001/Mental-Health-Chatbot"
    },
    {
        "title": "Complaint Analyzer",
        "desc": "AI system that analyzes customer complaints and returns structured output (category, severity, root issue & recommended actions).",
        "tech": "Gemini API, LangChain, Streamlit",
        "live": "https://complaint-analyzer-hfwazsdbf5v3btxt379kzw.streamlit.app/",  
        "github": "https://github.com/Adepuharshavardhan2001/Complaint-analyzer"
    },
    {
        "title": "Sentiment Analysis with Chain-of-Thought",
        "desc": "Transparent sentiment analysis on customer reviews using Few-shot Chain-of-Thought prompting with detailed reasoning.",
        "tech": "Gemini API, LangChain, Streamlit",
        "live": "https://sentiment---with---cot-from-customer-reviews-hezccowbtzepdb9ee.streamlit.app/",
        "github": "https://github.com/Adepuharshavardhan2001/sentiment---with---Cot-from-Customer-reviews"
    }
]

# Display Projects in 2 columns
cols = st.columns(2)
for idx, project in enumerate(projects):
    with cols[idx % 2]:
        with st.container(border=True):
            st.subheader(project["title"])
            st.write(project["desc"])
            st.caption(f"**Tech**: {project['tech']}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🌐 Live Demo", project["live"], type="primary")
            with c2:
                st.link_button("🔗 GitHub", project["github"])

st.markdown("---")

# Contact
st.header("Get In Touch")
st.write("📧 Email: [adepuharshavardhan2001@gmail.com](mailto:adepuharshavardhan2001@gmail.com)")  # ← Update
st.write("🔗 [GitHub](https://github.com/Adepuharshavardhan2001)")
st.write("🔗 [LinkedIn](linkedin.com/in/adepu-harshavardhan-ds)")           
      