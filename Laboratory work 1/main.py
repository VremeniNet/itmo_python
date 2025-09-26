def SumTwo(a, b):
    if type(b) is not int or any(type(x) is not int for x in a):
        return None
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            if a[i] + a[j] == b:
                return [i, j]
            else:
                continue
    return None

if __name__ == "__main__":
    print(SumTwo([2, 7, 11, 15], 9))
    print(SumTwo([3, 2, 4], 6))
    print(SumTwo([3, 3], 6))
