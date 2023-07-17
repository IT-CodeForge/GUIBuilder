

if __name__ == '__main__':
  str = "qdewbqswudhqwnuisohoöusd{dljbqwkudxgqwuodhpisd{dkjcgasdioansdx}dzugasdzuasdhboasd}dhkqaswdilasd{dwljgasdujasdpiaküs{dwljasdjaslöd}skdgjauisholasd}adljhasdkuiahlds"
  level = 0
  t_start_i = 0
  for i, char in enumerate(str):
    if char == "{":
      if level == 0:
        t_start_i = i
      level += 1
    elif char == "}":
      level -= 1
      if level == 0:
        print(str[t_start_i:i+1])