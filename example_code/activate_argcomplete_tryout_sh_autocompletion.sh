#!/usr/bin/env bash


# ALTERNATIVE: activate auto-completion for one script only (I have not tried this out successfully)
#eval "$(register-python-argcomplete argcomplete_tryout_sh)"

echo "[ERIKA 3004] Activating script autocompletion"
echo "[ERIKA 3004] (see https://argcomplete.readthedocs.io/en/latest/#global-completion )"

argcomplete_support_installed=$(type -P activate-global-python-argcomplete)
if [[ "$?" -ne 0 ]]; then
    echo "[ERIKA 3004] Unexpected error (type -P)"
    exit 1
fi
if [[ -z "${argcomplete_support_installed}" ]]; then
    echo "[ERIKA 3004] FAILED. Install argcomplete python module: pip3 install argcomplete"
    exit 1
fi

activate-global-python-argcomplete 1>/dev/null 2>/dev/null
if [[ "$?" -ne 0 ]]; then

    echo "[ERIKA 3004] Direct installation FAILED."
    echo "[ERIKA 3004] Instead, will generate a script instead..."
    echo "[ERIKA 3004] activate-global-python-argcomplete --dest=- > /tmp/python-argcomplete.sh"
    activate-global-python-argcomplete --dest=- > /tmp/python-argcomplete.sh
    if [[ "$?" -ne 0 ]]; then
        echo "[ERIKA 3004] Script generation FAILED as well. Exiting..."
        exit 1
    fi
    echo "[ERIKA 3004] DONE"
    echo "[ERIKA 3004] ...and copy it to the target directory then."
    echo "[ERIKA 3004] THIS WILL REQUIRE SUDO ACCESS:"
    echo "[ERIKA 3004] sudo cp /tmp/python-argcomplete.sh /etc/bash_completion.d"
    sudo cp /tmp/python-argcomplete.sh /etc/bash_completion.d
    if [[ "$?" -ne 0 ]]; then
        echo "[ERIKA 3004] Copying the script FAILED. Exiting..."
        exit 1
    fi
fi

echo "[ERIKA 3004] Python auto-completion successfully activated."

