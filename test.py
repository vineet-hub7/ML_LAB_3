import pickle

with open('model_social.pkl', 'rb') as f:
    model_social = pickle.load(f)

with open('scaler_ss.pkl', 'rb') as f:
    scaler_ss = pickle.load(f)

with open('model_tennis.pkl', 'rb') as f:
    model_tennis = pickle.load(f)

print("Loaded Social Model:", type(model_social))
print("Loaded Scaler:", type(scaler_ss))
print("Loaded Tennis Model:", type(model_tennis))
