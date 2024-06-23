import asyncio

# Define an asynchronous function
async def fetch_data(url):
    print(f"Fetching data from {url}")
    # Simulate a delay (as if fetching data from a network)
    await asyncio.sleep(2)
    print(f"Data fetched successfully from {url}")
    return f"Data from {url}"

# Define a function to run the asynchronous task
async def main():
    # Execute fetch_data concurrently
    task1 = fetch_data("https://api.example.com/data1")
    task2 = fetch_data("https://api.example.com/data2")

    # Wait for both tasks to complete
    data1 = await task1
    data2 = await task2

    # Process the fetched data
    print("Processing data...")
    print(data1)
    print(data2)

# Run the event loop
asyncio.run(main())

