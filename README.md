# neo-says

> A snarky CLI fortune teller for developers. Because you needed more sass in your terminal.

```
$ neo-says
╭──────────────────────────────────────────╮
│ "It works on my machine" is not a        │
│  deployment strategy.                    │
│                              — Neo 😒    │
╰──────────────────────────────────────────╯
```

## Install

```bash
pip install neo-says
```

Or just clone and run:

```bash
git clone https://github.com/mongsill6/neo-says.git
cd neo-says
python neo_says.py
```

## Usage

```bash
# Random snarky wisdom
neo-says

# Filter by category
neo-says --category git
neo-says --category debugging
neo-says --category meetings

# Add to your shell profile for daily sass
echo 'python ~/neo-says/neo_says.py' >> ~/.bashrc
```

## Categories

- `git` — Version control truths
- `debugging` — Bug hunting wisdom
- `meetings` — Meeting survival guide
- `code-review` — PR commentary
- `production` — Deploy day prayers
- `general` — Universal dev truths

## Contributing

Got a snarky dev quote? PRs welcome. Keep it real, keep it sassy.

## License

MIT
