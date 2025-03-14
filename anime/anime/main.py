import warnings
# 忽略来自scrapy.selector.unified模块的UserWarning
warnings.filterwarnings('ignore', category=UserWarning, module='scrapy.selector.unified')

import initialMySQL as im
import argparse
import sys
import os
from scrapy import cmdline

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Scrapy 爬虫启动脚本")
    parser.add_argument("-s", "--spider", default="bili", help="爬虫名称")
    parser.add_argument("-j", "--jobdir", default="./jobs/bili_job", help="续爬工作目录")
    args = parser.parse_args()

    # 检查并创建工作目录
    if not os.path.exists(args.jobdir):
        os.makedirs(args.jobdir, exist_ok=True)
        print(f"创建续爬目录: {args.jobdir}")

    # 构建 Scrapy 命令参数
    cmd_args = [
        "scrapy",
        "crawl",
        args.spider,
        "-s", f"JOBDIR={args.jobdir}"
    ]

    # 执行命令
    try:
        cmdline.execute(cmd_args)
    except SystemExit as e:
        if e.code == 0:
            print("✅ 爬虫执行完成")
        else:
            print(f"❌ 爬虫异常终止，错误码: {e.code}")

if __name__ == "__main__":
    # im.pymysql_drop_table()
    # im.pymysql_create_table()
    # #
    #cmdline.execute(['scrapy', 'crawl', 'bili'])
    cmdline.execute(['scrapy', 'crawl', 'biliChina'])