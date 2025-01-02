import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType

# Load your trained model
model = joblib.load('your_model.joblib')

# Define initial type (assuming the input is a single string feature)
initial_type = [('input', StringTensorType([None]))]

# Convert to ONNX
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Save the ONNX model
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
