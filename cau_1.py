"""
    Bài toán tìm dãy con lớn nhất
    Cho dãy số nguyên a1, a2, . . . , aN với N ≥ 1000. Hãy tìm trọng lượng lớn nhất của
    dãy con liên tiếp trong dãy đã cho.
    Định nghĩa
    • Dãy con liên tiếp: là dãy các phần tử nằm liền kề nhau trong dãy ban đầu.
    • Trọng lượng: là tổng giá trị các phần tử trong dãy con đó.
    Yêu cầu
    • Viết giải pháp bằng một trong các ngôn ngữ: Python, C/C++, hoặc JavaScript.
    • Trình bày mã giả (pseudo-code) nếu có thể.
    • Phân tích rõ độ phức tạp thuật toá

"""
def find_max_subarray(arr):
    if not arr:
        return 0

    max_current = max_global = arr[0]

    for i in range(1, len(arr)):
        max_current = max(arr[i], max_current + arr[i])
        max_global = max(max_global, max_current)

    return max_global

if __name__ == "__main__":
    arr = [1, -2, 3, 5, -1, 2]
    result = find_max_subarray(arr)
    print(f"Trọng lượng lớn nhất của dãy con liên tiếp: {result}")
