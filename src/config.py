from pathlib import Path

# Definindo o diretório raiz do projeto (um nível acima da pasta src)
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos de entrada e saída
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Garantindo que as pastas existam
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Definições globais de limpeza
NOS_ARTIFICIAIS = ['sem clube', 'fim de carreira', 'desconhecido']