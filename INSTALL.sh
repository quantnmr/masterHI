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

shell_rc_files() {
    local candidates=("$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.profile")
    local found=()
    for f in "${candidates[@]}"; do
        [ -f "$f" ] && found+=("$f")
    done
    # If nothing exists, default to .bashrc
    if [ ${#found[@]} -eq 0 ]; then
        found=("$HOME/.bashrc")
    fi
    printf '%s\n' "${found[@]}"
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
    mapfile -t rc_files < <(shell_rc_files)
    for rc in "${rc_files[@]}"; do
        if rc_already_has_marker "$rc"; then
            # Remove the marker line and the export line that follows it
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

    # 5. Ensure ~/bin is on PATH -------------------------------------------
    if path_already_has_bin; then
        ok "$INSTALL_DIR is already on PATH"
    else
        info "Adding $INSTALL_DIR to PATH in shell config"
        local rc_files
        mapfile -t rc_files < <(shell_rc_files)
        local modified=()
        for rc in "${rc_files[@]}"; do
            if ! rc_already_has_marker "$rc"; then
                printf '\n%s\nexport PATH="%s:$PATH"\n' "$MARKER" "$INSTALL_DIR" >> "$rc"
                modified+=("$rc")
            fi
        done
        if [ ${#modified[@]} -gt 0 ]; then
            ok "Updated: ${modified[*]}"
            warn "Restart your shell or run:  source ${modified[0]}"
        fi
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
