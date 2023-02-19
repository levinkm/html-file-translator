import os
import asyncio
from base import translate_file
# from translate import check
rootdir = './'
extensions = ('.html',)

all_tasks = []

loop = asyncio.new_event_loop()


async def main():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext in extensions:
                print(os.path.join(subdir, file))

                file1 = os.path.join(subdir, file)

                all_tasks.append(loop.create_task(await translate_file(file1)))

    await asyncio.gather(*all_tasks)


if __name__ == "__main__":
    loop.run_until_complete(main())
    # print("Done")
