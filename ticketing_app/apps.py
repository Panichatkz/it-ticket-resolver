import os
import keras
from keras import layers
from django.apps import AppConfig

class TicketingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticketing_app'
    
    # Global memory hooks easily accessible across your entire MVT project views
    cached_mimo_model = None
    cached_vectorizer = None

    def ready(self):
        model_asset_path = os.path.join(os.path.dirname(__file__), "../it_mimo_model.keras")
        
        # Load the compiled Keras Functional API network straight into system RAM memory
        if os.path.exists(model_asset_path):
            TicketingAppConfig.cached_mimo_model = keras.models.load_model(model_asset_path)
            print("\n[SYSTEM CACHE] Keras 3-Input 3-Output MIMO network mounted smoothly to memory.")
        else:
            print("\n[SYSTEM ALERT] Pre-trained model binary asset file not found in root path.")

        # Re-initialize local offline vectorization rules schema 
        sample_corpus = ["vpn connection", "printer jammed", "software license", "laptop screen", "payroll portal"]
        TicketingAppConfig.cached_vectorizer = layers.TextVectorization(max_tokens=2000, output_sequence_length=40)
        TicketingAppConfig.cached_vectorizer.adapt(sample_corpus)
        print("[SYSTEM CACHE] Offline text preprocessing token vectorizer initialized.")
