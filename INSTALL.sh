#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# masterHI installer
#
# Usage:
#   ./INSTALL.sh              Install MHI2D, MHI3D, and dependencies
#   ./INSTALL.sh --uninstall  Remove everything installed by this script
# ---------------------------------------------------------------------------

INSTALL_DIR="$HOME/bin/masterHI"
VENV_DIR="$HOME/bin/masterHI/.venv"
MARKER="# Added by masterHI installer"
SCRIPTS=(MHI2D MHI3D)
SUPPORT_FILES=(masterhi_common.py)
ALL_FILES=("${SCRIPTS[@]}" "${SUPPORT_FILES[@]}")
EXTERNAL_TOOLS=(nmrPipe bruk2pipe hmsIST nmrDraw)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()  { printf '\033[1;34m==> %s\033[0m\n' "$*"; }
warn()  { printf '\033[1;33mWARNING: %s\033[0m\n' "$*"; }
err()   { printf '\033[1;31mERROR: %s\033[0m\n' "$*" >&2; }
ok()    { printf '\033[1;32m  OK: %s\033[0m\n' "$*"; }

all_rc_files() {
    local candidates=(
        "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"
        "$HOME/.zshrc"
        "$HOME/.tcshrc" "$HOME/.cshrc"
        "$HOME/.config/fish/config.fish"
    )
    for f in "${candidates[@]}"; do
        [ -f "$f" ] && printf '%s\n' "$f"
    done
}

detect_user_shell() {
    local shell_path="${SHELL:-}"
    if [ -z "$shell_path" ]; then
        shell_path="$(getent passwd "$(whoami)" 2>/dev/null | cut -d: -f7)" || true
    fi
    local name
    name="$(basename "$shell_path" 2>/dev/null)" || name="bash"
    [ -z "$name" ] && name="bash"
    echo "$name"
}

rc_file_for_shell() {
    local shell_name="$1"
    case "$shell_name" in
        zsh)   echo "$HOME/.zshrc" ;;
        tcsh)  [ -f "$HOME/.tcshrc" ] && echo "$HOME/.tcshrc" || echo "$HOME/.cshrc" ;;
        csh)   echo "$HOME/.cshrc" ;;
        fish)  echo "$HOME/.config/fish/config.fish" ;;
        bash)  [ -f "$HOME/.bashrc" ] && echo "$HOME/.bashrc" || echo "$HOME/.bash_profile" ;;
        *)     [ -f "$HOME/.profile" ] && echo "$HOME/.profile" || echo "$HOME/.bashrc" ;;
    esac
}

path_export_line() {
    local shell_name="$1"
    case "$shell_name" in
        tcsh|csh)  printf 'setenv PATH "%s:$PATH"' "$INSTALL_DIR" ;;
        fish)      printf 'set -gx PATH "%s" $PATH' "$INSTALL_DIR" ;;
        *)         printf 'export PATH="%s:$PATH"' "$INSTALL_DIR" ;;
    esac
}

path_already_has_bin() {
    echo "$PATH" | tr ':' '\n' | grep -qx "$INSTALL_DIR"
}

rc_already_has_marker() {
    grep -qF "$MARKER" "$1" 2>/dev/null
}

# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------

do_uninstall() {
    info "Uninstalling masterHI"

    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
        ok "Removed $INSTALL_DIR"
    else
        warn "$INSTALL_DIR does not exist, nothing to remove"
    fi

    local rc_files
    mapfile -t rc_files < <(all_rc_files)
    for rc in "${rc_files[@]}"; do
        if rc_already_has_marker "$rc"; then
            sed -i "/$MARKER/,+1d" "$rc"
            ok "Removed PATH entry from $rc"
        fi
    done

    info "Uninstall complete"
}

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------

do_install() {
    info "Installing masterHI"

    # 1. Check / install uv ------------------------------------------------
    if ! command -v uv &>/dev/null; then
        warn "'uv' is not installed."
        printf "   Install it now? (curl -LsSf https://astral.sh/uv/install.sh | sh) [Y/n] "
        read -r ans
        case "$ans" in
            [Nn]*)
                err "Cannot proceed without uv. Install it manually: https://docs.astral.sh/uv/"
                exit 1
                ;;
            *)
                curl -LsSf https://astral.sh/uv/install.sh | sh
                # uv installer adds itself to ~/.cargo/bin or ~/.local/bin;
                # make sure it's on PATH for the rest of this script.
                export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
                if ! command -v uv &>/dev/null; then
                    err "uv installation succeeded but 'uv' not found on PATH. Restart your shell and re-run."
                    exit 1
                fi
                ok "uv installed"
                ;;
        esac
    else
        ok "uv found: $(command -v uv)"
    fi

    # 2. Create install dir and venv ---------------------------------------
    mkdir -p "$INSTALL_DIR"
    info "Creating virtual environment at $VENV_DIR"
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
    fi
    uv venv "$VENV_DIR" --python 3.9
    ok "Virtual environment created"

    # 3. Install requirements ----------------------------------------------
    info "Installing Python dependencies"
    uv pip install --python "$VENV_DIR/bin/python" -r "$REPO_DIR/requirements.txt"
    ok "Dependencies installed"

    # 4. Copy files to install dir -----------------------------------------
    info "Installing scripts to $INSTALL_DIR"

    local venv_python="$VENV_DIR/bin/python3"

    for f in "${ALL_FILES[@]}"; do
        cp "$REPO_DIR/$f" "$INSTALL_DIR/$f"
    done

    # Patch shebangs so scripts use the venv python directly
    for f in "${SCRIPTS[@]}"; do
        sed -i "1s|^#!/usr/bin/env python3|#!${venv_python}|" "$INSTALL_DIR/$f"
        chmod +x "$INSTALL_DIR/$f"
        ok "Installed $INSTALL_DIR/$f"
    done
    for f in "${SUPPORT_FILES[@]}"; do
        ok "Installed $INSTALL_DIR/$f"
    done

    # 5. Ensure install dir is on PATH ----------------------------------------
    local SOURCE_HINT=""
    if path_already_has_bin; then
        ok "$INSTALL_DIR is already on PATH"
    else
        local shell_name
        shell_name="$(detect_user_shell)"
        local rc
        rc="$(rc_file_for_shell "$shell_name")"
        local export_line
        export_line="$(path_export_line "$shell_name")"

        info "Detected shell: $shell_name"

        if ! rc_already_has_marker "$rc"; then
            mkdir -p "$(dirname "$rc")"
            printf '\n%s\n%s\n' "$MARKER" "$export_line" >> "$rc"
            ok "Updated: $rc"
        else
            ok "$rc already contains masterHI PATH entry"
        fi

        SOURCE_HINT="source $rc"
    fi

    # 6. Check external tools ----------------------------------------------
    info "Checking for NMR external tools"
    local missing=()
    for tool in "${EXTERNAL_TOOLS[@]}"; do
        if command -v "$tool" &>/dev/null; then
            ok "$tool found"
        else
            missing+=("$tool")
            warn "$tool not found on PATH"
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        warn "Missing tools: ${missing[*]}"
        printf "   MHI2D/MHI3D require nmrPipe and hmsIST at runtime.\n"
        printf "   Make sure they are installed and on your PATH.\n"
    fi

    # 7. Summary -----------------------------------------------------------
    echo ""
    info "Installation complete!"
    if [ -n "$SOURCE_HINT" ]; then
        echo ""
        echo "  ---------------------------------------------------------------"
        printf '  \033[1;33mACTION REQUIRED\033[0m  To use MHI2D/MHI3D in this terminal:\n'
        echo ""
        printf '      \033[1m%s\033[0m\n' "$SOURCE_HINT"
        echo ""
        echo "  Or simply open a new terminal window."
        echo "  ---------------------------------------------------------------"
    fi
    echo ""
    echo "  Virtual environment:  $VENV_DIR"
    echo "  Scripts installed to: $INSTALL_DIR"
    echo ""
    echo "  Usage:"
    echo "    MHI2D --help"
    echo "    MHI3D --help"
    echo ""
    echo "  To uninstall:  $REPO_DIR/INSTALL.sh --uninstall"
    echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

case "${1:-}" in
    --uninstall)
        do_uninstall
        ;;
    --help|-h)
        echo "Usage: $0 [--uninstall]"
        echo ""
        echo "  (no args)     Install MHI2D, MHI3D, and Python dependencies"
        echo "  --uninstall   Remove all installed files and configuration"
        ;;
    "")
        do_install
        ;;
    *)
        err "Unknown option: $1"
        echo "Usage: $0 [--uninstall]"
        exit 1
        ;;
esac
