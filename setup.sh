PY_MINOR_VERSION_STRING='Python 3.10'
PY_CANONICAL_CMD='python3.10'
PY_VERSION_PATTERN='\s3\.10\.\d*'

if "$PY_CANONICAL_CMD" --version 2> /dev/null | grep -q "$PY_VERSION_PATTERN"; then
  PY_CMD="$PY_CANONICAL_CMD"
elif python3 --version 2> /dev/null | grep -q "$PY_VERSION_PATTERN"; then
  PY_CMD="python3"
elif python --version 2> /dev/null | grep -q "$PY_VERSION_PATTERN"; then
  PY_CMD="python"
else
  echo "ERROR: $PY_MINOR_VERSION_STRING not found!"
  exit 1
fi

echo "Using $PY_MINOR_VERSION_STRING from $(which $PY_CMD)"

"$PY_CMD" -m venv --clear ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
deactivate

# TODO: Check if already installed; check Rust version.
cargo install diesel_cli --no-default-features --features "sqlite"

echo ""
echo "DONE - Setup complete, happy hacking!"