from llama_cpp import Llama

class Gguf:
    def __init__(self):
        self.model = None


    def load_model(self):
        self.model = Llama.from_pretrained(
            repo_id="mradermacher/JSL-Med-Phi-3.5-Mini-v3-i1-GGUF",
            filename="JSL-Med-Phi-3.5-Mini-v3.i1-Q4_K_M.gguf",
            n_ctx=2048,
            n_gpu_layers=-1,
            n_threads=8,
            n_batch=2048,
            offload_kqv=True,  # Выгрузка слоёв на GPU
            verbose=False,
            logits_all=True
        )