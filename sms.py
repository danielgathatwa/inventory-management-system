# import package
import africastalking


# Initialize SDK
username = "kabiru"    # use 'sandbox' for development in the test environment
api_key = "d3875b86a37a06d561f8501242daaaf64a4d95085f99ab8c5da64a020a4aa33d"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("kasweetie ka-Awesome !!!", ["+254713259011"])
print(response)