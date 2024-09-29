#import random

"""
sRandom = ""
for _ in range(500):
    n = random.randint(1,4)
    if n == 1 : sRandom += 'A'
    elif n == 2 : sRandom += 'T'
    elif n == 3 : sRandom += 'G'
    elif n == 4 : sRandom += 'C'

print(sRandom)
"""

ref = ""
alt = ""

f = open('input/ref.txt','r')
ref = f.read()
print('ref: ', ref)
f.close()

print()

f = open('input/alt.txt','r')
alt = f.read()
print('alt: ', alt)
f.close()

print()

#ref = "CCATTGA"
#alt = "ATCG"

m = len(alt)
n = len(ref)
dp = [[0] * (n + 1) for _ in range(m + 1)]


for i in range(1, m + 1):
    for j in range(1, n + 1):
        if ref[j - 1] == alt[i - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])


lcs = ""
i, j = m, n
while i > 0 and j > 0:
    if ref[j - 1] == alt[i - 1]:
        lcs = ref[j - 1] + lcs
        if i > 0 : i -= 1
        if j > 0 : j -= 1
        if i == 0 and j>1:
            print("POS 1~%d, DEL : %s -> _" % (j, ref[:j]))
        if j == 0 and i>1:
            print("POS %d, INS : _ -> %s" % (0, alt[:i]))

    elif dp[i - 1][j] > dp[i][j - 1]: # INS
        print("POS %d, INS : _ -> %c" % (j, alt[i-1]))
        if i > 0 : i -= 1
    elif dp[i - 1][j] < dp[i][j - 1]: # DEL
        print("POS %d, DEL : %c -> _" % (j, ref[j-1]))
        if j > 0 : j -= 1
    elif dp[i - 1][j] == dp[i][j - 1]: # SNV
        print("POS %d, SNV : %c -> %c" % (j, ref[j-1], alt[i-1]))
        if i > 0 : i -= 1
        if j > 0 : j -= 1


print()

"""
for i in range(1,m+1):
    print(dp[i][1:])
"""

print()
print("n=%d" %(dp[m][n]))
print("LCS:", lcs)