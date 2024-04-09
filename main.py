import sys
from init_data import init_data
from strategy.strategy_mode1 import strategy_mode1 

def main(argument):
  print("Received parameter:", argument)
  init_data()
  
  if argument == "mode1" :
    strategy_mode1()

if __name__ == "__main__":
    # 效验命令行参数列表长度, sys.argv[0] 是脚本名, sys.argv[1] 是你传递的参数 "mode1"
    if len(sys.argv) < 2:
        print("Missing argument")
        main("nomal")  
    else:
        main(sys.argv[1])  # 传递命令行参数 "mode1"


