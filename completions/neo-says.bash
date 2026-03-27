# bash completion for neo-says                            -*- shell-script -*-

_neo_says()
{
    local cur prev words cword
    _init_completion || return

    local -r subcommands="tui pack"
    local -r themes="box minimal ascii-art cowsay"
    local -r langs="en ko ja"
    local -r pack_subcommands="list install remove"

    # Find which subcommand (if any) has been specified
    local subcmd=""
    local pack_subcmd=""
    local i
    for ((i = 1; i < cword; i++)); do
        case "${words[i]}" in
            tui|pack)
                subcmd="${words[i]}"
                ;;
            list|install|remove)
                if [[ "$subcmd" == "pack" ]]; then
                    pack_subcmd="${words[i]}"
                fi
                ;;
        esac
    done

    # Handle pack sub-subcommands
    if [[ "$subcmd" == "pack" ]]; then
        if [[ -z "$pack_subcmd" ]]; then
            COMPREPLY=($(compgen -W "$pack_subcommands" -- "$cur"))
            return
        fi
        case "$pack_subcmd" in
            install)
                # Complete file paths
                _filedir
                return
                ;;
            remove|list)
                # No further completion
                return
                ;;
        esac
        return
    fi

    # Handle tui (no further options)
    if [[ "$subcmd" == "tui" ]]; then
        return
    fi

    # Complete option arguments
    case "$prev" in
        -c|--category)
            return
            ;;
        -t|--tag)
            return
            ;;
        --theme|--set-theme)
            COMPREPLY=($(compgen -W "$themes" -- "$cur"))
            return
            ;;
        --lang|--set-lang)
            COMPREPLY=($(compgen -W "$langs" -- "$cur"))
            return
            ;;
        --pack)
            return
            ;;
    esac

    # Complete subcommands and options
    if [[ "$cur" == -* ]]; then
        local opts="-c --category -t --tag -l --list-categories --list-tags
                     --today --raw --theme --set-theme --lang --set-lang
                     --pack -h --help"
        COMPREPLY=($(compgen -W "$opts" -- "$cur"))
    else
        COMPREPLY=($(compgen -W "$subcommands" -- "$cur"))
    fi
}

complete -F _neo_says neo-says
