import sys
import time
import concurrent.futures
import asyncio
import math
import numpy as np
from decimal import Decimal, getcontext

sys.set_int_max_str_digits(10**9)

start = 0 
time_limit = 180 
highest_prime = None 
MAX_PRIME = 1000000
FIB_LIMIT = 10000000

getcontext().prec = 1000  # Set decimal precision for large numbers

phi = Decimal((1 + math.sqrt(5)) / 2)  # Use Decimal for phi
sqrt_5 = Decimal(math.sqrt(5))

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def calculate_highest_prime(method_name, start_time):
    global highest_prime
    num = start
    highest_prime = None

    while True:
        if time.time() - start_time > time_limit:
            break
        if is_prime(num):
            highest_prime = num
        num += 1

        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {int(elapsed_time)}s", end="\r")
    print(f"{method_name}: {highest_prime}")
    return highest_prime

# Matrix multiplication using Decimal for precision
def matrix_mult(A, B):
    return np.array([[Decimal(A[0][0]) * Decimal(B[0][0]) + Decimal(A[0][1]) * Decimal(B[1][0]),
                      Decimal(A[0][0]) * Decimal(B[0][1]) + Decimal(A[0][1]) * Decimal(B[1][1])],
                     [Decimal(A[1][0]) * Decimal(B[0][0]) + Decimal(A[1][1]) * Decimal(B[1][0]),
                      Decimal(A[1][0]) * Decimal(B[0][1]) + Decimal(A[1][1]) * Decimal(B[1][1])]])

# Matrix exponentiation for Fibonacci numbers with Decimal precision
def matrix_power(matrix, n):
    result = np.array([[Decimal(1), Decimal(0)], [Decimal(0), Decimal(1)]])  # Identity matrix
    base = matrix
    while n > 0:
        if n % 2 == 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        n //= 2
    return result

# Function to compute Fibonacci number using matrix exponentiation
def fibonacci(n):
    if n == 0:
        return 0
    F = np.array([[Decimal(1), Decimal(1)], [Decimal(1), Decimal(0)]], dtype=object)  # Fibonacci Q-matrix
    result_matrix = matrix_power(F, n - 1)  # Power of the Fibonacci matrix
    return result_matrix[0][0]  # The top left corner contains the Fibonacci number

def factorial(n):
    if n > MAX_PRIME:
        return math.factorial(n)
    else:
        n_decimal = Decimal(n)
        approx_factorial = math.sqrt(2 * math.pi * n_decimal) * (n_decimal / math.e) ** n_decimal
        return approx_factorial

def factorial_stirling(n):
    if n <= 1:
        return 1
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n

def multiprocessing(start_time):
    global highest_prime
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.submit(calculate_highest_prime, "Multi-core", start_time)
        try:
            return result.result(timeout=time_limit)
        except concurrent.futures.TimeoutError:
            print("Multi-core calculation exceeded the time limit.")
        return None
        
def threaded(start_time):
    global highest_prime
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.submit(calculate_highest_prime, "Threaded", start_time)
        try:
            return result.result(timeout=time_limit)
        except concurrent.futures.TimeoutError:
            print("Threaded calculation exceeded the time limit") 
        return None
    
async def asynchronous(start_time):
    return await asyncio.get_event_loop().run_in_executor(None, calculate_highest_prime, "Async", start_time)

async def calculate_fib_and_factorial(highest_prime):
    print(f"Calculating Fibonacci and Factorial for prime: {highest_prime}")
    
    # Run Fibonacci and Factorial calculations concurrently
    fib_res = None
    fact_res = None
    if highest_prime > FIB_LIMIT:
        fib_res = fibonacci(highest_prime)
        fact_res = factorial_stirling(highest_prime)
    else:
        # Calculate Fibonacci using matrix exponentiation
        F = np.array([[1, 1], [1, 0]], dtype=object)
        Fn = matrix_power(F, highest_prime - 1)
        fib_res = Fn[0][0]
        fact_res = factorial(highest_prime)

    print(f"Fibonacci({highest_prime}) = {fib_res}\nFactorial({highest_prime}) = {fact_res}")

async def main():
    global highest_prime
    start_time = time.time()
 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        multi_future = executor.submit(multiprocessing, start_time)
        thread_future = executor.submit(threaded, start_time) 
        highest_prime_async = await asynchronous(start_time)
    
    highest_prime_multi = multi_future.result()
    highest_prime_thread = thread_future.result()

    valid_primes = [highest_prime_multi, highest_prime_thread, highest_prime_async]
    valid_primes = {p for p in valid_primes if p is not None}

    if valid_primes:
        highest_prime = max(valid_primes)
        print(f"Highest prime found: {highest_prime}")
        await calculate_fib_and_factorial(highest_prime)
    else:
        print("No prime found")

if __name__ == "__main__":
    print("Starting calculations...")
    asyncio.run(main())

