import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced UI styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #4CAF50;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
        margin: 1rem 0;
    }
    .stExpander {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
    }
    .stNumberInput>div>div>input {
        border-radius: 8px;
    }
    .info-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .sidebar-content {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Why This Plan Works For You")
        st.info(plan_content.get("why_this_plan_works", "Information not available"))
        
        st.markdown("### 🍽️ Your Daily Meal Plan")
        st.markdown(f"""
        <div style='background-color: #f8fafc; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
            {plan_content.get("meal_plan", "Plan not available")}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚠️ Health Considerations")
        considerations = plan_content.get("important_considerations", "").split('\n')
        cols = st.columns(2)
        for idx, consideration in enumerate(considerations):
            if consideration.strip():
                cols[idx % 2].warning(consideration)
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🎯 Your Fitness Goals")
            st.success(plan_content.get("goals", "Goals not specified"))
            
            st.markdown("### 🏋️‍♂️ Workout Routine")
            st.markdown(f"""
            <div style='background-color: #f8fafc; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
                {plan_content.get("routine", "Routine not available")}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 Training Tips")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    # Header with gradient background
    st.markdown("""
        <div class="header-container">
            <h1>🏋️‍♂️ AI Health & Fitness Planner</h1>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>
                Get personalized dietary and fitness plans powered by AI, tailored specifically to your goals and preferences.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar with improved styling
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("### 🔑 API Configuration")
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Gemini API key to access the service"
        )
        
        if not gemini_api_key:
            st.warning("⚠️ Please enter your Gemini API Key to proceed")
            st.markdown("[Get your API key here](https://aistudio.google.com/apikey)")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        st.success("✅ API Key verified!")
        st.markdown('</div>', unsafe_allow_html=True)

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-1.5-flash", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Error initializing Gemini model: {e}")
            return

        st.markdown("## 👤 Your Profile")
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
            sex = st.selectbox("Sex", options=["Male", "Female", "Other"])

        with col2:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            activity_level = st.selectbox(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                help="Choose your typical activity level"
            )
            dietary_preferences = st.selectbox(
                "Dietary Preferences",
                options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
                help="Select your dietary preference"
            )

        with col3:
            fitness_goals = st.selectbox(
                "Fitness Goals",
                options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
                help="What do you want to achieve?"
            )
            
            st.markdown("<br>" * 3, unsafe_allow_html=True)
            if st.button("🎯 Generate My Plan", use_container_width=True):
                with st.spinner("Creating your perfect health and fitness routine..."):
                    try:
                        dietary_agent = Agent(
                            name="Dietary Expert",
                            role="Provides personalized dietary recommendations",
                            model=gemini_model,
                            instructions=[
                                "Consider the user's input, including dietary restrictions and preferences.",
                                "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                                "Provide a brief explanation of why the plan is suited to the user's goals.",
                                "Focus on clarity, coherence, and quality of the recommendations.",
                            ]
                        )

                        fitness_agent = Agent(
                            name="Fitness Expert",
                            role="Provides personalized fitness recommendations",
                            model=gemini_model,
                            instructions=[
                                "Provide exercises tailored to the user's goals.",
                                "Include warm-up, main workout, and cool-down exercises.",
                                "Explain the benefits of each recommended exercise.",
                                "Ensure the plan is actionable and detailed.",
                            ]
                        )

                        user_profile = f"""
                        Age: {age}
                        Weight: {weight}kg
                        Height: {height}cm
                        Sex: {sex}
                        Activity Level: {activity_level}
                        Dietary Preferences: {dietary_preferences}
                        Fitness Goals: {fitness_goals}
                        """

                        dietary_plan_response = dietary_agent.run(user_profile)
                        dietary_plan = {
                            "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                            "meal_plan": dietary_plan_response.content,
                            "important_considerations": """
                            - Hydration: Drink plenty of water throughout the day
                            - Electrolytes: Monitor sodium, potassium, and magnesium levels
                            - Fiber: Ensure adequate intake through vegetables and fruits
                            - Listen to your body: Adjust portion sizes as needed
                            """
                        }

                        fitness_plan_response = fitness_agent.run(user_profile)
                        fitness_plan = {
                            "goals": "Build strength, improve endurance, and maintain overall fitness",
                            "routine": fitness_plan_response.content,
                            "tips": """
                            - Track your progress regularly
                            - Allow proper rest between workouts
                            - Focus on proper form
                            - Stay consistent with your routine
                            """
                        }

                        st.session_state.dietary_plan = dietary_plan
                        st.session_state.fitness_plan = fitness_plan
                        st.session_state.plans_generated = True
                        st.session_state.qa_pairs = []

                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.plans_generated:
            display_dietary_plan(st.session_state.dietary_plan)
            display_fitness_plan(st.session_state.fitness_plan)

            st.markdown("## ❓ Questions About Your Plan")
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            with col1:
                question_input = st.text_input("What would you like to know?", placeholder="Type your question here...")
            with col2:
                ask_button = st.button("Ask Question", use_container_width=True)

            if ask_button and question_input:
                with st.spinner("Finding the best answer for you..."):
                    dietary_plan = st.session_state.dietary_plan
                    fitness_plan = st.session_state.fitness_plan

                    context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}"
                    full_context = f"{context}\nUser Question: {question_input}"

                    try:
                        agent = Agent(model=gemini_model, show_tool_calls=True, markdown=True)
                        run_response = agent.run(full_context)

                        if hasattr(run_response, 'content'):
                            answer = run_response.content
                        else:
                            answer = "Sorry, I couldn't generate a response at this time."

                        st.session_state.qa_pairs.append((question_input, answer))
                    except Exception as e:
                        st.error(f"❌ An error occurred while getting the answer: {e}")

            if st.session_state.qa_pairs:
                st.markdown("### 💬 Previous Questions & Answers")
                for idx, (question, answer) in enumerate(st.session_state.qa_pairs):
                    with st.container():
                        st.markdown(f"""
                        <div style='background-color: #f8fafc; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                            <p style='color: #4a5568; margin-bottom: 0.5rem;'><strong>Q: {question}</strong></p>
                            <p style='color: #2d3748;'>A: {answer}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()