To start the app first install Docker
Then enter you models API KEY and Model name in .env file
Then follow the given steps:
  docker build -t langgraph-chatbot .  \n
  docker run -p 8000:8000 langgraph-chatbot  \n
  http://localhost:8000  \n

For, Postman:-
  curl -X POST "http://localhost:8000/chat?message=Hello my name is Ram"
  curl -X POST "http://localhost:8000/chat?message=What is my name?"
