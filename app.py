import gradio as gr
import pickle
import numpy as np

# Load models and scalers safely
def load_pickle(file_name):
    try:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return None

# Load all required files
model_tennis = load_pickle('model_tennis.pkl')
model_social = load_pickle('model_social.pkl')
scaler_ss = load_pickle('scaler_ss.pkl')
scaler_mm = load_pickle('scaler_mm.pkl')

def predict_tennis(outlook, temp, humidity, wind):
    if not model_tennis: return "Model not loaded properly."
    
    # Encoded value mapping based on trained models
    out_map = {"Overcast": 0, "Rain": 1, "Sunny": 2}
    temp_map = {"Cool": 0, "Hot": 1, "Mild": 2}
    hum_map = {"High": 0, "Normal": 1}
    wind_map = {"Strong": 0, "Weak": 1}
    
    features = np.array([[out_map[outlook], temp_map[temp], hum_map[humidity], wind_map[wind]]])
    pred = model_tennis.predict(features)[0]
    
    # Decode target: No=0, Yes=1
    return "✅ Yes, play tennis!" if pred == 1 else "❌ No, do not play."


def predict_social(age, salary, scaler_choice):
    if not model_social: return "Model not loaded properly."
    
    features = np.array([[float(age), float(salary)]])
    
    # Apply chosen scaler
    if scaler_choice == "MinMax Scaler":
        if not scaler_mm: return "MinMax Scaler missing!"
        features_scaled = scaler_mm.transform(features)
    else:
        if not scaler_ss: return "Standard Scaler missing!"
        features_scaled = scaler_ss.transform(features)
        
    pred = model_social.predict(features_scaled)[0]
    
    # Decode target: Not Purchased=0, Purchased=1
    return "🛒 Will Purchase" if pred == 1 else "🚫 Will Not Purchase"


# Gradio Block UI Design
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate")) as demo:
    gr.Markdown("# 🤖 ML Prediction Studio")
    gr.Markdown("Experience the power of our trained Naive Bayes models!")
    
    with gr.Tabs():
        # Play Tennis Tab
        with gr.TabItem("🎾 Play Tennis Predictor"):
            gr.Markdown("### Should you play Tennis today?")
            
            with gr.Row():
                outlook_in = gr.Dropdown(choices=["Sunny", "Overcast", "Rain"], label="Outlook", value="Sunny")
                temp_in = gr.Dropdown(choices=["Hot", "Mild", "Cool"], label="Temperature", value="Hot")
            
            with gr.Row():
                humidity_in = gr.Dropdown(choices=["High", "Normal"], label="Humidity", value="High")
                wind_in = gr.Dropdown(choices=["Weak", "Strong"], label="Wind", value="Weak")
                
            tennis_btn = gr.Button("Predict Outcome", variant="primary")
            tennis_out = gr.Textbox(label="Prediction Result", show_label=True, elem_classes="result-box")
            
            tennis_btn.click(fn=predict_tennis, inputs=[outlook_in, temp_in, humidity_in, wind_in], outputs=tennis_out)
            
        # Social Network Ads Tab
        with gr.TabItem("📱 Social Network Ads"):
            gr.Markdown("### Product Purchase Predictor")
            
            with gr.Row():
                age_in = gr.Number(label="Age", value=30, precision=0)
                salary_in = gr.Number(label="Estimated Salary ($)", value=50000)
                
            scaler_in = gr.Radio(choices=["Standard Scaler", "MinMax Scaler"], label="Feature Scaler Algorithm", value="Standard Scaler")
            
            social_btn = gr.Button("Predict Purchase", variant="primary")
            social_out = gr.Textbox(label="Prediction Result", show_label=True)
            
            social_btn.click(fn=predict_social, inputs=[age_in, salary_in, scaler_in], outputs=social_out)

if __name__ == "__main__":
    # Hugging Face Spaces exposes port 7860
    demo.launch(server_name="0.0.0.0", server_port=7860)
