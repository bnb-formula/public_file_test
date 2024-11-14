def name():
  name_input = input("Enter your name: ")
  print(f"Hello, {name_input}")
  return name_input

def age():
  age_input = int(input("Enter your age: "))
  
  if age_input < 15:
    print(f"You are a kid. Your age: {age_input}")
  elif 20 >= age_input >=15:
    print(f"You are a teenager. Your age: {age_input}")
  else:
    print(f"You are an adult guy. Your age: {age_input}")
