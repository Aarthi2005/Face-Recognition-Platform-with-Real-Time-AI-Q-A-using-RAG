import asyncio
import websockets
import json
import datetime

# Function to get the names of all registered users
def get_all_registered_users():
    try:
        with open("user_registration_logs.txt", "r") as file:
            lines = file.readlines()
            if lines:
                users = [line.split()[0] for line in lines]
                return f"The registered users are: {', '.join(users)}."
            else:
                return "No users are registered."
    except FileNotFoundError:
        return "User registration log file not found."
    except Exception as e:
        return f"Error reading the file: {e}"

# Function to get the last registered user
def get_last_registered_user():
    try:
        with open("user_registration_logs.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_user_line = lines[-1]
                last_user = last_user_line.split()[0]
                return f"The last registered user is {last_user}."
            else:
                return "No users are registered."
    except FileNotFoundError:
        return "User registration log file not found."
    except Exception as e:
        return f"Error reading the file: {e}"

# Function to get the first registered user
def get_first_registered_user():
    try:
        with open("user_registration_logs.txt", "r") as file:
            lines = file.readlines()
            if lines:
                first_user_line = lines[0]
                first_user = first_user_line.split()[0]
                return f"The first registered user is {first_user}."
            else:
                return "No users are registered."
    except FileNotFoundError:
        return "User registration log file not found."
    except Exception as e:
        return f"Error reading the file: {e}"

# Function to get the number of registered users
def get_number_of_registered_users():
    try:
        with open("user_registration_logs.txt", "r") as file:
            lines = file.readlines()
            return f"There are currently {len(lines)} registered users." if lines else "No users are registered."
    except FileNotFoundError:
        return "User registration log file not found."
    except Exception as e:
        return f"Error reading the file: {e}"

# Function to get the registration time of a specific user
def get_user_registration_time(user_name):
    try:
        with open("user_registration_logs.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.lower().startswith(user_name.lower()):
                    # Extract the time part from the log
                    time_registered = line.split('at')[1].strip()
                    return f"{user_name} registered at {time_registered}."
            return f"No registration time found for {user_name}."
    except FileNotFoundError:
        return "User registration log file not found."
    except Exception as e:
        return f"Error reading the file: {e}"

# WebSocket server handler for queries
async def handle_query(websocket, path):
    try:
        message = await websocket.recv()
        print(f"Received message: {message}")

        data = json.loads(message)
        print(f"Received data: {data}")

        query = data["question"]
        print(f"Question received: {query}")

        # Handling different types of queries using a case-insensitive approach
        query_lower = query.lower()

        if "last registered user" in query_lower:
            response = get_last_registered_user()
        elif "first registered user" in query_lower:
            response = get_first_registered_user()
        elif "list the name of registered users" in query_lower or "list the name of currently registered users" in query_lower:
            response = get_all_registered_users()
        elif "currently how many registered users" in query_lower or "how many registered users" in query_lower or "how many registered user" in query_lower:
            response = get_number_of_registered_users()
        elif "at what time" in query_lower and "registered" in query_lower:
            # Extract user name from the query (e.g., "At what time gp registered?")
            user_name = query_lower.split("at what time")[-1].split("registered")[0].strip()
            response = get_user_registration_time(user_name)
        else:
            response = "Sorry, I don't know the answer to that question."

        # Make sure the response is a string
        await websocket.send(str(response))
    except KeyError as e:
        print(f"KeyError: {e}")
        await websocket.send("Error: 'question' key not found in the message.")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send(f"An error occurred: {e}")

# WebSocket server
async def main():
    async with websockets.serve(handle_query, "localhost", 8001):
        print("RAG server running on ws://localhost:8001")
        await asyncio.Future()  # run forever

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
