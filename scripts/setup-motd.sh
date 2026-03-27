#!/usr/bin/env bash
# setup-motd.sh — Set up neo-says as the MOTD shown on login
# Usage: ./setup-motd.sh [--uninstall]

set -euo pipefail

MARKER="# neo-says MOTD"
NEO_SAYS_CMD='neo-says 2>/dev/null || true'
PROFILE_D="/etc/profile.d/neo-says.sh"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()  { printf '\033[1;34m[info]\033[0m  %s\n' "$*"; }
ok()    { printf '\033[1;32m[ok]\033[0m    %s\n' "$*"; }
warn()  { printf '\033[1;33m[warn]\033[0m  %s\n' "$*"; }
err()   { printf '\033[1;31m[error]\033[0m %s\n' "$*"; }

detect_os() {
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "macos" ;;
        *)       echo "unknown" ;;
    esac
}

check_neo_says() {
    if command -v neo-says &>/dev/null; then
        return 0
    fi
    # Also check common pip script locations
    for p in "$HOME/.local/bin/neo-says" /usr/local/bin/neo-says; do
        if [ -x "$p" ]; then
            return 0
        fi
    done
    return 1
}

# ---------------------------------------------------------------------------
# Linux: /etc/profile.d/neo-says.sh
# ---------------------------------------------------------------------------

install_linux() {
    info "Setting up MOTD via $PROFILE_D"

    if [ -f "$PROFILE_D" ] && grep -qF "$MARKER" "$PROFILE_D" 2>/dev/null; then
        warn "MOTD already configured in $PROFILE_D — skipping (idempotent)."
        return 0
    fi

    # Need root to write to /etc/profile.d/
    if [ "$(id -u)" -ne 0 ]; then
        err "Root privileges required to write to $PROFILE_D"
        info "Re-run with: sudo $0"
        return 1
    fi

    cat > "$PROFILE_D" <<EOF
$MARKER
# Displays a snarky Neo quote on every interactive login.
if [ -n "\$PS1" ] && command -v neo-says &>/dev/null; then
    $NEO_SAYS_CMD
fi
EOF
    chmod 644 "$PROFILE_D"
    ok "Created $PROFILE_D — neo-says will run on next login."
}

uninstall_linux() {
    if [ ! -f "$PROFILE_D" ]; then
        info "Nothing to remove — $PROFILE_D does not exist."
        return 0
    fi

    if [ "$(id -u)" -ne 0 ]; then
        err "Root privileges required to remove $PROFILE_D"
        info "Re-run with: sudo $0 --uninstall"
        return 1
    fi

    rm -f "$PROFILE_D"
    ok "Removed $PROFILE_D"
}

# ---------------------------------------------------------------------------
# macOS: ~/.zprofile or ~/.bash_profile
# ---------------------------------------------------------------------------

mac_profile_file() {
    # Prefer zsh (default on modern macOS), fall back to bash
    if [ -n "${ZSH_VERSION:-}" ] || [ "$(basename "${SHELL:-}")" = "zsh" ]; then
        echo "$HOME/.zprofile"
    else
        echo "$HOME/.bash_profile"
    fi
}

install_macos() {
    local profile
    profile="$(mac_profile_file)"
    info "Setting up MOTD via $profile"

    if [ -f "$profile" ] && grep -qF "$MARKER" "$profile" 2>/dev/null; then
        warn "MOTD already configured in $profile — skipping (idempotent)."
        return 0
    fi

    # Append the block
    {
        echo ""
        echo "$MARKER"
        echo "if command -v neo-says &>/dev/null; then"
        echo "    $NEO_SAYS_CMD"
        echo "fi"
    } >> "$profile"

    ok "Appended neo-says MOTD block to $profile"
}

uninstall_macos() {
    local profile
    profile="$(mac_profile_file)"

    if [ ! -f "$profile" ] || ! grep -qF "$MARKER" "$profile" 2>/dev/null; then
        info "Nothing to remove — no neo-says MOTD block found in $profile."
        return 0
    fi

    # Remove the marker line and the 3 lines that follow it
    # Pattern: blank line, marker, if-line, neo-says-line, fi-line
    local tmp
    tmp="$(mktemp)"
    awk -v marker="$MARKER" '
        $0 == marker { skip = 3; next }
        skip > 0     { skip--; next }
        { print }
    ' "$profile" > "$tmp"

    # Remove possible trailing blank line left behind
    sed -i.bak -e :a -e '/^[[:space:]]*$/{ $d; N; ba; }' "$tmp" 2>/dev/null || true
    rm -f "${tmp}.bak"

    mv "$tmp" "$profile"
    ok "Removed neo-says MOTD block from $profile"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    local uninstall=false

    for arg in "$@"; do
        case "$arg" in
            --uninstall|-u) uninstall=true ;;
            --help|-h)
                echo "Usage: $0 [--uninstall]"
                echo "  Sets up (or removes) neo-says as the login MOTD."
                exit 0
                ;;
            *)
                err "Unknown option: $arg"
                exit 1
                ;;
        esac
    done

    local os
    os="$(detect_os)"

    if [ "$uninstall" = true ]; then
        info "Uninstalling neo-says MOTD..."
        case "$os" in
            linux) uninstall_linux ;;
            macos) uninstall_macos ;;
            *)     err "Unsupported OS: $(uname -s)"; exit 1 ;;
        esac
        ok "MOTD uninstall complete."
        exit 0
    fi

    # Install flow
    if ! check_neo_says; then
        err "neo-says is not installed. Install it first:"
        echo "    pip install neo-says"
        exit 1
    fi

    info "Detected OS: $os"
    case "$os" in
        linux) install_linux ;;
        macos) install_macos ;;
        *)     err "Unsupported OS: $(uname -s)"; exit 1 ;;
    esac
}

main "$@"
