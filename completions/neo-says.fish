# fish completion for neo-says

# Condition helpers
function __neo_says_no_subcommand
    set -l cmd (commandline -opc)
    for c in $cmd[2..]
        switch $c
            case tui pack
                return 1
        end
    end
    return 0
end

function __neo_says_using_subcommand
    set -l cmd (commandline -opc)
    for c in $cmd[2..]
        if test "$c" = "$argv[1]"
            return 0
        end
    end
    return 1
end

function __neo_says_pack_no_subcommand
    set -l cmd (commandline -opc)
    set -l found_pack 0
    for c in $cmd[2..]
        if test $found_pack -eq 1
            switch $c
                case list install remove
                    return 1
            end
        end
        if test "$c" = pack
            set found_pack 1
        end
    end
    return 0
end

function __neo_says_pack_using_subcommand
    set -l cmd (commandline -opc)
    set -l found_pack 0
    for c in $cmd[2..]
        if test $found_pack -eq 1
            if test "$c" = "$argv[1]"
                return 0
            end
        end
        if test "$c" = pack
            set found_pack 1
        end
    end
    return 1
end

# Subcommands (top-level)
complete -c neo-says -f -n __neo_says_no_subcommand -a tui -d 'Launch interactive TUI mode'
complete -c neo-says -f -n __neo_says_no_subcommand -a pack -d 'Manage quote packs'

# Main options (when no subcommand)
complete -c neo-says -n __neo_says_no_subcommand -s c -l category -x -d 'Filter by category'
complete -c neo-says -n __neo_says_no_subcommand -s t -l tag -x -d 'Filter by tag'
complete -c neo-says -n __neo_says_no_subcommand -s l -l list-categories -d 'List available categories'
complete -c neo-says -n __neo_says_no_subcommand -l list-tags -d 'List available tags'
complete -c neo-says -n __neo_says_no_subcommand -l today -d 'Show today\'s quote'
complete -c neo-says -n __neo_says_no_subcommand -l raw -d 'Output raw text without theme'
complete -c neo-says -n __neo_says_no_subcommand -l theme -x -a 'box minimal ascii-art cowsay' -d 'Set theme for this invocation'
complete -c neo-says -n __neo_says_no_subcommand -l set-theme -x -a 'box minimal ascii-art cowsay' -d 'Set default theme'
complete -c neo-says -n __neo_says_no_subcommand -l lang -x -a 'en ko ja' -d 'Set language for this invocation'
complete -c neo-says -n __neo_says_no_subcommand -l set-lang -x -a 'en ko ja' -d 'Set default language'
complete -c neo-says -n __neo_says_no_subcommand -l pack -x -d 'Use a specific quote pack'
complete -c neo-says -n __neo_says_no_subcommand -s h -l help -d 'Show help message'

# Pack sub-subcommands
complete -c neo-says -f -n '__neo_says_using_subcommand pack; and __neo_says_pack_no_subcommand' -a list -d 'List installed quote packs'
complete -c neo-says -f -n '__neo_says_using_subcommand pack; and __neo_says_pack_no_subcommand' -a install -d 'Install a quote pack from file'
complete -c neo-says -f -n '__neo_says_using_subcommand pack; and __neo_says_pack_no_subcommand' -a remove -d 'Remove an installed quote pack'

# Pack install: complete file paths
complete -c neo-says -F -n '__neo_says_pack_using_subcommand install'

# Pack remove: expect pack name (no file completion)
complete -c neo-says -f -n '__neo_says_pack_using_subcommand remove' -x -d 'Pack name to remove'
