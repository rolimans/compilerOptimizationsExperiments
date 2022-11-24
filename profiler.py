#!/usr/bin/python3

import subprocess
import os
import json


def compileAndRun(compilationFlags=[], runArg=7):
    os.environ["TIMEFORMAT"] = "%E"

    compileCommand = " ".join(
        ["gcc -o main fannkuchredux.c"] + compilationFlags)
    print("Compiling with: " + compileCommand)
    os.system(f'time ({compileCommand}) 2> compileTimeOut')

    print("Running...")
    os.system(f'(time ./main {runArg}) 2> timeOut > out')
    print("Finished running.")

    expectedOutputFile = "expectedOut"+str(runArg)

    diffCode = subprocess.call(["diff", "out", expectedOutputFile])

    with open("timeOut", "r") as f:
        time = float(f.read().replace(",", '.'))

    with open("compileTimeOut", "r") as f:
        compileTime = float(f.read().replace(",", '.'))

    os.remove("out")
    os.remove("timeOut")
    os.remove("compileTimeOut")
    os.remove("main")

    return {
        "time": time,
        "error": diffCode != 0,
        "compilationTime": compileTime,
        "compilationFlags": compilationFlags,
        "runArg": runArg
    }


runs = []
compilationsFlags = [
    ["-O0", "-march=native"],
    ["-O1", "-march=native"],
    ["-O2", "-march=native"],
    ["-O3", "-march=native"],
    ["-ftree-partial-pre", "-fcaller-saves", "-finline",
     "-finline-small-functions", "-freorder-blocks"],
]

runArgs = [11, 12]

for compilationFlags in compilationsFlags:
    for runArg in runArgs:
        currSample = {
            "hasError": False,
            "compilationFlags": compilationFlags,
            "runArg": runArg,
            "times": [],
            "compilationTimes": [],
            "meanTime": 0,
            "meanCompilationTime": 0,
        }
        for i in range(10):
            print(f"Run {i+1}/10")
            result = compileAndRun(compilationFlags, runArg)
            if result["error"]:
                currSample["hasError"] = True
            else:
                currSample["times"].append(result["time"])
                currSample["compilationTimes"].append(
                    result["compilationTime"])
        currSample["meanTime"] = sum(
            currSample["times"]) / len(currSample["times"])
        currSample["meanCompilationTime"] = sum(
            currSample["compilationTimes"]) / len(currSample["compilationTimes"])
        runs.append(currSample)


with open("runs.json", 'w') as f:
    f.write(json.dumps(runs, indent=4))
