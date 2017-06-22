# -*- coding: utf-8 -*-

def mergeTimeAt(testArr):
    print 'got testArr', testArr
    outputArr = []

    curIdx = 0
    mergeSpan = 7
    prevTimeSpot = 0

    # First Index check
    try:
        prevTimeSpot = testArr[0]
        outputArr.append([0, prevTimeSpot])
    except IndexError:
        print 'except'
        exit(0)


    for idx, timeSpot in enumerate(testArr):
        if timeSpot - outputArr[curIdx][1] < mergeSpan: # mergeSpan보다 작으면 뒷값 바꿈
            outputArr[curIdx][1] = timeSpot
        else: # mergeSpan보다 크면 뒷값을 mergeSpan만큼 더해줌
            outputArr[curIdx][1] += mergeSpan
            curIdx += 1
            if idx+1 < len(testArr) - 1: # 길이가 추가 가능한 길이이면 뒷값에 추가
                outputArr.append([testArr[idx], testArr[idx]])
    print 'mergedArr' + str(outputArr)
    return outputArr