#!/usr/bin/env bash

set -e
set -o pipefail

# ============================================
# ProjectSetup 3.0 - Interactive Launcher
# Linux / Bash
# ============================================

CUR_DIR="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[INFO] Project root: $SCRIPT_DIR"
echo

# --- Verifica Python ---
if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERRO] Python 3 nao encontrado no PATH!"
  exit 1
fi

PY_VERSION="$(python3 --version | awk '{print $2}')"
echo "[INFO] Python $PY_VERSION detectado"

# --- Ativa venv se existir ---
if [[ -f "$SCRIPT_DIR/venv/bin/activate" ]]; then
  echo "[INFO] Ativando venv..."
  source "$SCRIPT_DIR/venv/bin/activate"
else
  echo "[INFO] Usando Python global"
fi

# --- Instala todas dependências do requirements.txt ---
REQ_FILE="$SCRIPT_DIR/projectsetup3/requirements/requirements.txt"
if [[ -f "$REQ_FILE" ]]; then
  echo "[INFO] Instalando todas dependencias de $REQ_FILE ..."
  python3 -m pip install --user -r "$REQ_FILE"
else
  echo "[WARN] requirements.txt nao encontrado em $REQ_FILE"
fi

# --- Instala pacote local projectsetup3 (editable) ---
if ! python3 -c "import projectsetup3" >/dev/null 2>&1; then
  echo "[WARN] Modulo projectsetup3 nao encontrado"
  echo "[INFO] Instalando pacote local (editable)..."
  if [[ ! -f "$SCRIPT_DIR/pyproject.toml" ]]; then
    echo "[ERRO] pyproject.toml nao encontrado no root!"
    exit 1
  fi
  python3 -m pip install -e "$SCRIPT_DIR"
fi

# --- Executa o pacote ProjectSetup ---
echo
echo "[INFO] Iniciando ProjectSetup 3.0..."
echo
python3 -m projectsetup3 "$@" 2>&1
EXIT_CODE=$?

# --- Finalizacao ---
echo
if [[ $EXIT_CODE -ne 0 ]]; then
  echo "[ERRO] Encerrado com codigo $EXIT_CODE"
  read -p "Pressione Enter para sair..."
else
  echo "[OK] Finalizado com sucesso!"
  sleep 2
fi

cd "$CUR_DIR"
exit "$EXIT_CODE"
