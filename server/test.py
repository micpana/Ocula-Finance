import MetaTrader5 as mt5
from datetime import datetime, timedelta

# Initialize MT5 connection
if not mt5.initialize():
    print(f"Initialization failed, error code: {mt5.last_error()}")
    exit()

# Get the server time
server_time = mt5.time()

if server_time is not None:
    # Convert the server time to a datetime object
    server_time_dt = datetime.utcfromtimestamp(server_time)
    local_time = datetime.utcnow()

    # Calculate the broker's timezone offset
    timezone_offset = (server_time_dt - local_time).total_seconds() / 3600

    print(f"Broker's Timezone Offset (in hours from UTC): {timezone_offset}")
else:
    print(f"Failed to retrieve server time, error code: {mt5.last_error()}")

# Shutdown MT5 connection
mt5.shutdown()
