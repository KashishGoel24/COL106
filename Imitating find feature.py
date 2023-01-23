import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	'''
	let A != B be two strings. let f(A) - f(B) = x; now if we want that this should come in false positive then q should be chosen from among the primes of x.
	There are at most log2(x) primes for x. so,
									probability of choosing them is =  log2(x) / pi(N)   < eps 
									by the way 26-ary representation has been defined, x < 26**m
									=> log2(x) / pi(N) < mlog2(26)/ pi(N) < mlog2(26)*(2*log2(N)) / N       (using the upper bound of N)
									=>  N/log2(N) < 2*(m/eps)*log2(26)
									using that N/log2(N) > N/root(N) = root(N):
									we impose that root(N) > 2*(m/eps)*log2(26)
									=> N > (2*(m/eps)*log2(26))**2
									HENCE, WE GET THE VALUE OF N
	'''
	return int(((m/eps)**2)*88.376)

# returns the 26-ary representation of a single alphabet
def alphabet_code(letter):                                 #O(1) time and O(1) space
    code = ord(letter) - 65
    return code 

# Return sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):
    m = len(p)
    n = len(x)                                  #O(1) time and O(logn) space             
    valid_indices = []
    #calculating f(p) mod q using horner's rule
    f_p = 0
    var = 1                                     #variable used to store (26**m)%q
    for i in range (0,m):                       #O(m*log(q)) time and O(logq) space
        f_p = (((26%q)*(f_p%q))%q + alphabet_code(p[i])%q)%q                   # adding the alphabet code for next letter and multiplying the initial value by 26 and ensuring that everytime I work on logq bits
        var = (var*(26%q))%q

    f_y = 0      #calculating f() for substrings of x of length m each
    i = pointer = 0
    while i < n:                                #O(n*log(q)) time and O(logq + k) space   (k : no of valid indices)          (the loop runs exactly n times and within the loop operations are performed on logq bit numbers, logq bit numbers are only stored along with the storing the indices in the list whoch taked k space )
        if pointer == m - 1:                                               #calculates f(y) as we traverse through the first substring of x of length m
            if pointer == i:
                f_y = (((26%q)*(f_y%q))%q + alphabet_code(x[i])%q)%q
                if f_y == f_p:                                             #comparing f_y and f_p and appending the index of it is valid
                    valid_indices.append(i - m + 1)
            else:                                                          #calculating f(y) for every subsequent string by eliminating the initial first alphabet and adding the new last alphabet
                f_y = (((26%q)*(f_y%q))%q + alphabet_code(x[i])%q - (var*alphabet_code(x[i-m])%q)%q)%q
                if f_y == f_p:                                             #comparing f_y and f_p and appending the index of it is valid
                    valid_indices.append(i - m + 1)
        else:                                                              #calculates f(y) as we traverse through the first substring of x of length m
            f_y = (((26%q)*(f_y%q))%q + alphabet_code(x[i])%q)%q
            pointer += 1

        i += 1

    return valid_indices

#TOTAL TIME COMPLEXITY - O((m+n)*logq)                TOTAL SPACE COMPLEXITY - O(k + logq + logn)

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q, p, x):
    m = len(p)
    n = len(x)                                  #O(1) time and O(logn) space
    valid_indices = []
    #calculating f(p) mod q using horner's rule
    f_p = 0
    var1 = (26%q)                               #var1 is (26**m)%q
    var2 = 1                                    #var2 is (26**offset)%q
    offset = 0
    for i in range (0,m):                       #O(m*log(q)) time and O(logq + logm) space    (f_p takes logq space and offset takes logm space)
        if p[i] == '?':                         #checks when the wildcard character appears and doesn't consider its value in calculating f(p)
            f_p = ((26%q)*(f_p%q))%q
            offset = m-1-i                      #O(logm) space         #offset is the variable which tells as to how far the wildcard character is from the last letter of the string p
            continue
        else:
            f_p = (((26%q)*f_p)%q + alphabet_code(p[i])%q)%q           # adding the alphabet code for next letter and multiplying the initial value by 26 and ensuring that everytime I work on logq bits
            var1 = (var1*(26%q))%q
            if offset != 0:
                var2 = (var2*(26%q))%q

    var3 = (var2*(26%q))%q                     #var3 is (26**(offset+1))%q      #O(logq) space

    f_y = 0      #calculating f() for substrings of x of length m each
    i = pointer = 0

    while i < n:                               #O(n*log(q)) time and O(logq + k) space   (k : no of valid indices)          (the loop runs exactly n times and within the loop operations are performed on logq bit numbers, logq bit numbers are only stored along with the storing the indices in the list whoch taked k space )
        if pointer == m - 1:                                               #calculates f(y) as we traverse through the first substring of x of length m
            if pointer == i:                                        
                f_y = (((26%q)*f_y)%q + alphabet_code(x[i])%q - (var2*(alphabet_code(x[i - offset]))%q)%q)%q          #besides what I did earlier, removing the value of the letter at wildcard spot
                if f_y == f_p:                                             #comparing f_y and f_p and appending the index of it is valid
                    valid_indices.append(i - m + 1)
            else:                                                          #calculating f(y) for every subsequent string by eliminating the initial first alphabet and adding the new last alphabet, removing the value of the letter at wildcard spot and adding the old letter at wilcard spot
                f_y = (((26%q)*f_y)%q + alphabet_code(x[i])%q - (var1*alphabet_code(x[i-m])%q)%q - (var2*(alphabet_code(x[i - offset]))%q)%q + (var3*(alphabet_code(x[i - offset - 1]))%q)%q)%q
                if f_y == f_p:                                             #comparing f_y and f_p and appending the index of it is valid
                    valid_indices.append(i - m + 1)
        else:                                                              #calculates f(y) as we traverse through the first substring of x of length m
            f_y = (((26%q)*f_y)%q + alphabet_code(x[i])%q)%q
            pointer += 1
        i += 1 

    return valid_indices

#TOTAL TIME COMPLEXITY - O((m+n)*logq)                TOTAL SPACE COMPLEXITY - O(k + logq + logn)