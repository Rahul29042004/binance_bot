import subprocess

# List of commands to run each bot module
commands = [
    "python -m market_orders BTCUSDT BUY 0.001",
    "python -m advanced.grid BTCUSDT 0.001 50000 --levels 2 --step_pct 0.5",
    "python -m advanced.oco BTCUSDT BUY 0.001 --take_profit 52000 --stop_loss 48000",
    "python -m advanced.twap BTCUSDT BUY 0.004 --duration 60 --interval 10"
]

for cmd in commands:
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True)
