#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_rating_apperance.py

Created by <wen.zhang@wedoapp.com> on Nov 28,2015
"""

def main():
  import argparse
  parser = argparse.ArgumentParser(description="根据输入的本机图片路径，使用face++的SDK测算颜值.")
  parser.add_argument("--path", type=str, help="输入本机的图片全路径，比如--path /Users/xxx/xxx.jpg")
  args = parser.parse_args()
  if args.path is not None:
    import rating_apperance
    rating_apperance.main(args.path)
  else:
    parser.print_help()
if __name__ == '__main__':
  main()
