#!/usr/bin/env bash
# install.sh — One-click installer for neo-says
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/mongsill6/neo-says/main/install.sh | bash
#   curl ... | bash -s -- --dev --with-motd
#
# Flags:
#   --dev         Install from git (latest HEAD) instead of PyPI
#   --with-motd   Also set up neo-says as login MOTD

set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PYPI_PACKAGE="neo-says"
GIT_REPO="https://github.com/mongsill6/neo-says.git"
REQUIRED_PYTHON_MAJOR=3
REQUIRED_PYTHON_MINOR=8
SETUP_MOTD_URL="https://raw.githubusercontent.com/mongsill6/neo-says/main/scripts/setup-motd.sh"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()  { printf '\033[1;34m[info]\033[0m  %s\n' "$*"; }
ok()    { printf '\033[1;32m[ok]\033[0m    %s\n' "$*"; }
warn()  { printf '\033[1;33m[warn]\033[0m  %s\n' "$*"; }
err()   { printf '\033[1;31m[error]\033[0m %s\n' "$*"; exit 1; }

banner() {
    cat <<'BANNER'

    _   __                ____
   / | / /__  ____       / __/___ ___  _______
  /  |/ / _ \/ __ \     / /_/ __ `/ / / / ___/
 / /|  /  __/ /_/ /    _\ \/ /_/ / /_/ (__  )
/_/ |_/\___/\____/    /___/\__,_/\__, /____/
                                /____/

  The snarky CLI companion you didn't ask for.

BANNER
}

# ---------------------------------------------------------------------------
# Python detection
# ---------------------------------------------------------------------------

find_python() {
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}

find_pip() {
    local python="$1"
    # Prefer pip/pip3 command, fall back to python -m pip
    for cmd in pip3 pip; do
        if command -v "$cmd" &>/dev/null; then
            echo "$cmd"
            return 0
        fi
    done
    # Try python -m pip
    if "$python" -m pip --version &>/dev/null; then
        echo "$python -m pip"
        return 0
    fi
    return 1
}

check_python_version() {
    local python="$1"
    local version
    version="$("$python" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)" || return 1

    local major minor
    major="${version%%.*}"
    minor="${version#*.}"

    if [ "$major" -lt "$REQUIRED_PYTHON_MAJOR" ]; then
        return 1
    fi
    if [ "$major" -eq "$REQUIRED_PYTHON_MAJOR" ] && [ "$minor" -lt "$REQUIRED_PYTHON_MINOR" ]; then
        return 1
    fi

    echo "$version"
    return 0
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    local dev_mode=false
    local with_motd=false

    for arg in "$@"; do
        case "$arg" in
            --dev)       dev_mode=true ;;
            --with-motd) with_motd=true ;;
            --help|-h)
                echo "Usage: $0 [--dev] [--with-motd]"
                echo "  --dev        Install from git HEAD instead of PyPI"
                echo "  --with-motd  Also configure neo-says as login MOTD"
                exit 0
                ;;
            *)
                err "Unknown option: $arg"
                ;;
        esac
    done

    banner

    # --- Check Python ---
    info "Checking for Python..."
    local python
    python="$(find_python)" || err "Python not found. Please install Python ${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR}+ first."

    local py_version
    py_version="$(check_python_version "$python")" || err "Python ${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR}+ required. Found: $("$python" --version 2>&1)"

    ok "Found $python ($py_version)"

    # --- Check pip ---
    info "Checking for pip..."
    local pip
    pip="$(find_pip "$python")" || err "pip not found. Install it with: $python -m ensurepip --upgrade"

    ok "Found pip: $pip"

    # --- Install neo-says ---
    if [ "$dev_mode" = true ]; then
        info "Installing neo-says from git (dev mode)..."
        $pip install --upgrade "git+${GIT_REPO}" || err "Failed to install neo-says from git."
    else
        info "Installing neo-says from PyPI..."
        $pip install --upgrade "$PYPI_PACKAGE" || err "Failed to install neo-says from PyPI."
    fi

    ok "neo-says installed successfully."

    # --- Verify installation ---
    info "Verifying installation..."

    # Refresh PATH in case pip installed to ~/.local/bin
    export PATH="$HOME/.local/bin:$PATH"

    if ! command -v neo-says &>/dev/null; then
        warn "neo-says command not found in PATH."
        warn "You may need to add ~/.local/bin to your PATH:"
        echo '    export PATH="$HOME/.local/bin:$PATH"'
        echo ""
        warn "Skipping demo run."
    else
        echo ""
        info "Here's your first Neo quote:"
        echo "---"
        neo-says 2>/dev/null || true
        echo "---"
        echo ""
    fi

    # --- Optional MOTD setup ---
    if [ "$with_motd" = true ]; then
        info "Setting up MOTD..."
        local motd_script="/tmp/neo-says/scripts/setup-motd.sh"

        if [ -f "$motd_script" ]; then
            bash "$motd_script"
        else
            # Download the script if not available locally
            info "Downloading setup-motd.sh..."
            local tmp_script
            tmp_script="$(mktemp)"
            if curl -fsSL "$SETUP_MOTD_URL" -o "$tmp_script" 2>/dev/null; then
                bash "$tmp_script"
                rm -f "$tmp_script"
            else
                warn "Could not download setup-motd.sh. Set up MOTD manually later."
            fi
        fi
    fi

    # --- Done ---
    echo ""
    ok "All done! Run 'neo-says' anytime for a snarky quote."
    if [ "$with_motd" = false ]; then
        info "Tip: re-run with --with-motd to show a quote on every login."
    fi
}

main "$@"
