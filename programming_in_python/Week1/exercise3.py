num_list = [33, 42, 5, 66, 77, 22, 16, 79,
            36, 62, 78, 43, 88, 39, 53, 67, 89, 11]
count = 0
for idx, num in enumerate(num_list):
    count += 1
    if num > 45:
        print(f"Over 45")
    else:
        print(f"Under 45")
    if num == 36:
        print(f"Number found at position: {idx}")
        break

print(count)